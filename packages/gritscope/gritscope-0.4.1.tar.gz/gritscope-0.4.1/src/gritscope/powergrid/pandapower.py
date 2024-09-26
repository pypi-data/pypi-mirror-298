from __future__ import annotations # Default behavior pending PEP 649

from typing import Hashable, Literal, Any, TypeVar, Type

from itertools import chain, repeat, starmap
from functools import reduce
import logging

import numpy as np
import pandas as pd

from pygrates.itertools import unique

import pandapower as pp # type: ignore
from pandapower.auxiliary import pandapowerNet as Net # type: ignore

from .grid import Grid, Topo, Params, Profs, ProfileFrame

# To do:
# - Process shunts

# Supported Pandapower elements
ELEMENTS = ['bus', 'line', 'trafo',
            'load', 'sgen', 'storage',
            'gen', 'ext_grid']

# Types for connection, load and generator encodings

C = Hashable
L = Hashable
G = Hashable

N = Hashable

def gs_grid(net: Net) -> Grid:
    """Return Grid object from Pandapower network object."""
    
    if not check_unique_names(net):
        logging.warning("renaming network elements to ensure uniqueness")
        net = rename_elements(net)
    
    merge_df = lambda x, y: pd.merge(x, y, left_index=True, right_index=True)
    merge_two = lambda x, y: x | y if isinstance(x, dict) else merge_df(x, y)
    merge_all = lambda xs: reduce(merge_two, xs)
    collect = lambda *xss: map(merge_all, zip(*xss))
    
    vb, co = process_buses(net)
    cn, v, l, y, yg, n = collect(process_lines(net),
                                 process_trafos(net))
    ln, vl, pl, q = collect(process_loads(net, 'load'),
                            process_loads(net, 'sgen'),
                            process_loads(net, 'storage'))
    gn, vg, s, vm, pg = collect(process_gens(net, 'gen'),
                                process_gens(net, 'ext_grid'),
                                process_dclines(net))
    
    v = v | vl | vg | vb
    p = merge_df(pl, pg)

    # Renormalize slack weights
    s_total = sum(s.values())
    if s_total == 0:
        s = {g: 1./len(s) for g in s}
    else:
        s = {g: v/s_total for g, v in s.items()}
    
    # VA = MVA*(VA/MVA)
    pb = net.sn_mva*1e6
    
    return Grid(Topo(cn, ln, gn), Params(y, yg, n, s, v, l, pb, co),
                Profs(ProfileFrame(p), ProfileFrame(q), ProfileFrame(vm)))

def pp_net(grid: Grid, timestamp: int = 0) -> Net:
    """Return Pandapower network object from Grid object."""
    
    # MVA = VA*(MVA/VA)
    pb = grid.params.pb*1e-6
    
    net = pp.create_empty_network(sn_mva=pb)
    
    net.bus = pd.concat([net.bus, reconstruct_buses(grid)])
    net.line = pd.concat([net.line, reconstruct_lines(grid, net)])
    net.trafo = pd.concat([net.trafo, reconstruct_trafos(grid, net)])
    net.load = pd.concat([net.load, reconstruct_loads(grid, net, timestamp)])
    net.gen = pd.concat([net.gen, reconstruct_gens(grid, net, timestamp)])
    
    for e in ('bus', 'line', 'trafo', 'load', 'gen'):
        net[e]['in_service'] = True
    
    return net

# Processing functions from Pandapower to Gritscope

Load = Literal['load'] | Literal['sgen'] | Literal['storage']
Gen = Literal['gen'] | Literal['ext_grid']

def process_buses(net: Net) -> tuple[dict[N, float],
                                     dict[N, tuple[float, float]]]:
    """Return parameter map from buses."""
    
    buses = pd.merge(net.bus, net.bus_geodata, how='left',
                     left_index=True, right_index=True)
    buses = buses.set_index('name')
    
     # V = kV-phase-to-phase*(V/V-phase-to-phase)*(V/kV)
    vb = param_dict(buses['vn_kv']*(1/np.sqrt(3))*1e3)
    co = dict(zip(buses.index, zip(buses['x'], buses['y'])))
    
    return vb, co

def process_lines(net: Net) -> tuple[dict[C, tuple[N, N]],
                                     dict[C, float],
                                     dict[C, float],
                                     dict[C, complex],
                                     dict[C, complex],
                                     dict[C, complex]]:
    """Return element-node map and parameter maps from lines."""
    
    lines = net.line.set_index('name').fillna(0.)
    lines = pd.merge(lines, net.bus, how='left', left_on='from_bus',
                     right_index=True, suffixes=['_line', ''])
    lines = pd.merge(lines, net.bus, how='left', left_on='to_bus',
                     right_index=True, suffixes=['_from_bus', '_to_bus'])
    lines = lines[(lines['in_service_line'] == True) &
                  (lines['in_service_from_bus'] == True) &
                  (lines['in_service_to_bus'] == True)]
    
    cn = dict(zip(lines.index, zip(lines['name_from_bus'],
                                   lines['name_to_bus'])))
    
    # V = kV-phase-to-phase*(V/V-phase-to-phase)*(V/kV)
    vb = lines['vn_kv_to_bus']*(1/np.sqrt(3))*1e3
    v = param_dict(vb)
    
    # A = kA*(A/kA)*Dimensionless*Dimensionless
    l = param_dict(lines['max_i_ka']*1e3*lines['parallel']*lines['df'])
    
    # Ohm = (Ohm/km)*km
    x = lines['x_ohm_per_km']*lines['length_km']
    r = lines['r_ohm_per_km']*lines['length_km']
    
    # Siemens = 1/Ohm*Dimensionless
    y = param_dict(1./(x*1j + r)*lines['parallel'], complex)
    
    # Siemens = (nF/km)*km*([rad/s]/Hz)*Hz*(Siemens/nSiemens)
    b = lines['c_nf_per_km']*lines['length_km']*(2*np.pi)*net.f_hz*1e-9
    
    # Siemens = (μSiemens/km)*km*(Siemens/μSiemens)
    g = lines['g_us_per_km']*lines['length_km']*1e-6
    
    # Siemens = Siemens*Dimensionless
    yg = param_dict((b*1j + g)*lines['parallel'], complex)
    
    # Dimensionless = Dimensionless
    n = dict(zip(lines.index, repeat(1.)))
    
    return cn, v, l, y, yg, n

def process_trafos(net: Net) -> tuple[dict[C, tuple[N, N]],
                                      dict[C, float],
                                      dict[C, float],
                                      dict[C, complex],
                                      dict[C, complex],
                                      dict[C, complex]]:
    """Return element-node map and parameter maps from transformers."""
    
    trafos = net.trafo.set_index('name')
    trafos = pd.merge(trafos, net.bus, how='left', left_on='lv_bus',
                      right_index=True, suffixes=['_trafo', ''])
    trafos = pd.merge(trafos, net.bus, how='left', left_on='hv_bus',
                      right_index=True, suffixes=['_lv_bus', '_hv_bus'])
    trafos = trafos[(trafos['in_service_trafo'] == True) &
                    (trafos['in_service_lv_bus'] == True) &
                    (trafos['in_service_hv_bus'] == True)]
    
    cn = dict(zip(trafos.index, zip(trafos['name_lv_bus'],
                                    trafos['name_hv_bus'])))
    
    # VA = MVA-three-phase*(VA/VA-three-phase)*(VA/MVA)
    pb = trafos['sn_mva']*(1/3.)*1e6
    
    # V = kV-phase-to-phase*(V/V-phase-to-phase)*(V/kV)
    vb = trafos['vn_kv_hv_bus']*(1/np.sqrt(3))*1e3
    v = param_dict(vb)
    
    # Percent = Percent
    mlp = get_col(trafos, 'max_loading_percent', 100., 'trafo')
    
    # A = VA/V*Percent/Percent*Dimensionless*Dimensionless
    l = param_dict(pb/vb*mlp/100.*trafos['parallel']*trafos['df'])
    
    # Ohm = Percent/Percent*(V**2)/VA
    zm = trafos['vk_percent']/100.*(vb**2)/pb
    r = trafos['vkr_percent']/100.*(vb**2)/pb
    
    # Ohm = Ohm
    x = np.sqrt(zm**2 - r**2)*np.sign(zm)
    
    # Siemens = 1/Ohm*Dimensionless
    y = param_dict(1./(x*1j + r)*trafos['parallel'], complex)
    
    # Siemens = Percent/Percent/(V**2)*VA
    ygm = trafos['i0_percent']/100./(vb**2)*pb
    
    # Siemens = kW-three-phase*(W/W-three-phase)/(V**2)*(Siemens/kSiemens)
    g = trafos['pfe_kw']*(1/3.)/(vb**2)*1e3
    
    # Siemens = Siemens
    b = -np.sqrt(ygm**2 - g**2)*np.sign(ygm)
    
    # Siemens = 1/Ohm*Dimensionless
    yg = param_dict((b*1j + g)*trafos['parallel'], complex)
    
    # Dimensionless = Dimensionless*Dimensionless*Dimensionless
    n = param_dict(trafo_ratios(trafos), complex)
    
    return cn, v, l, y, yg, n

def trafo_ratios(trafos: pd.DataFrame) -> pd.Series:
    """Return Series with complex winding ratios from transformers."""
    
    shifter = trafos['tap_phase_shifter']
    hvtap = trafos['tap_side'] == 'hv'
    lvtap = trafos['tap_side'] == 'lv'
    notap = ~lvtap & ~hvtap
    
    # Dimensionless = kV/kV
    w = trafos['vn_hv_kv']/trafos['vn_lv_kv']
    
    # Radians = Degrees*(Radians/Degrees)
    ps = trafos['shift_degree']*(2*np.pi/360.)
    
    # Steps = Steps
    tp = get_col(trafos, 'tap_pos', 0., 'trafo')
    tn = get_col(trafos, 'tap_neutral', 0., 'trafo')
    steps = tp - tn
    
    # Dimensionless = Steps*(1/Steps)
    dvm = steps*get_col(trafos, 'tap_step_percent', 0., 'trafo')/100.
    
    # Radians = Steps*(Degrees/Steps)*(Radians/Degrees)
    dva = steps*get_col(trafos, 'tap_step_degree', 0., 'trafo')*(2*np.pi/360.)
    
    # Dimensionless = Dimensionless*Dimensionless
    tap = (1 + ~shifter*dvm*np.exp(dva*1j))*np.exp(shifter*dva*1j)
    
    return (hvtap*w*tap + lvtap*w/tap + notap*w)*np.exp(ps*1j)

def process_loads(net: Net, kind: Load = 'load') -> tuple[dict[L, tuple[N]],
                                                          dict[L, float],
                                                          pd.DataFrame,
                                                          pd.DataFrame]:
    """Return element-node map, parameters, profiles from loads."""
    
    data = getattr(net, kind).set_index('name')
    
    loads = pd.merge(data, net.bus, how='left', left_on='bus',
                     right_index=True, suffixes=['_load', '_bus'])
    loads = loads[(loads['in_service_load'] == True) &
                  (loads['in_service_bus'] == True)]
    
    ln = dict(zip(loads.index, [(b,) for b in loads['name']]))
    
    # V = kV-phase-to-phase*(V/V-phase-to-phase)*(V/kV)
    vb = loads['vn_kv']*(1/np.sqrt(3))*1e3
    v = param_dict(vb)
    
    # W = MW-three-phase*(W/W-three-phase)*(W/MW)
    p = pd.DataFrame(loads['p_mw']*(1/3.)*1e6).T.reset_index(drop=True)
    
    # VA = MVA-three-phase*(VA/VA-three-phase)*(VA/MVA)
    q = pd.DataFrame(loads['q_mvar']*(1/3.)*1e6).T.reset_index(drop=True)
    
    if not kind == 'sgen':
        p = -p
        q = -q
    
    # VA = VA*Dimensionless
    p, q = p*loads['scaling'], q*loads['scaling']
    
    return ln, v, p, q

def process_gens(net: Net, kind: Gen = 'gen') -> tuple[dict[G, tuple[N]],
                                                       dict[G, float],
                                                       dict[G, float],
                                                       pd.DataFrame,
                                                       pd.DataFrame]:
    """Return element-node map, parameters, profiles from generators."""
    
    data = getattr(net, kind).set_index('name')
    
    gens = pd.merge(data, net.bus, how='left', left_on='bus',
                    right_index=True, suffixes=['_gen', '_bus'])
    gens = gens[(gens['in_service_gen'] == True) &
                (gens['in_service_bus'] == True)]
    
    gn = dict(zip(gens.index, [(b,) for b in gens['name']]))
    
    # V = kV-phase-to-phase*(V/V-phase-to-phase)*(V/kV)
    vb = gens['vn_kv']*(1/np.sqrt(3))*1e3
    v = param_dict(vb)
    
    # Dimensionless = Dimensionless
    s = param_dict(gens['slack_weight'])
    
    # V = Dimensionless*V
    vm = pd.DataFrame(gens['vm_pu']*vb).T.reset_index(drop=True)
    
    if kind == 'ext_grid':
        
        # W = W
        p = pd.DataFrame(0., index=[0], columns=gens.index)
    
    else:
        
        # W = MW-three-phase*(W/W-three-phase)*(W/MW)
        p = pd.DataFrame(gens['p_mw']*(1/3.)*1e6).T.reset_index(drop=True)
        
        # VA = VA*Dimensionless
        p = p*gens['scaling']
    
    return gn, v, s, vm, p

def process_dclines(net: Net) -> tuple[dict[G, tuple[N]],
                                       dict[G, float],
                                       dict[G, float],
                                       pd.DataFrame,
                                       pd.DataFrame]:
    """Return element-node map, parameters, profiles from DC lines."""
    
    dcs = net.dcline.set_index('name')
    dcs = pd.merge(dcs, net.bus, how='left', left_on='from_bus',
                   right_index=True, suffixes=['_line', ''])
    dcs = pd.merge(dcs, net.bus, how='left', left_on='to_bus',
                   right_index=True, suffixes=['_from_bus', '_to_bus'])
    dcs = dcs[(dcs['in_service_line'] == True) &
              (dcs['in_service_from_bus'] == True) &
              (dcs['in_service_to_bus'] == True)]
    
    dcs_f = dcs.set_index(dcs.index.astype(str) + 'f')
    dcs_t = dcs.set_index(dcs.index.astype(str) + 't')
    
    gn_f = [(b,) for b in dcs_f['name_from_bus']]
    gn_t = [(b,) for b in dcs_t['name_to_bus']]
    gn = dict(zip(dcs_f.index, gn_f)) | dict(zip(dcs_t.index, gn_t))
    
    # V = kV-phase-to-phase*(V/V-phase-to-phase)*(V/kV)
    vb_f = dcs_f['vn_kv_from_bus']*(1/np.sqrt(3))*1e3
    vb_t = dcs_t['vn_kv_to_bus']*(1/np.sqrt(3))*1e3
    v = param_dict(vb_f) | param_dict(vb_t)
    
    # Dimensionless = Dimensionless
    s = dict(zip(gn.keys(), repeat(0.)))
    
    # V = Dimensionless*V
    vm_f = pd.DataFrame(dcs_f['vm_from_pu']*vb_f).T.reset_index(drop=True)
    vm_t = pd.DataFrame(dcs_t['vm_to_pu']*vb_t).T.reset_index(drop=True)
    vm = pd.concat([vm_f, vm_t], axis=1)
    
    # W = MW-three-phase*(W/W-three-phase)*(W/MW)
    p_f = pd.DataFrame(-dcs_f['p_mw']*(1/3.)*1e6).T.reset_index(drop=True)
    p_t = (dcs_t['p_mw'] - dcs_t['loss_mw'])*(1/3.)*1e6
    
    # W = W*(Percent/Percent)
    p_t = p_t*(1 - dcs_t['loss_percent']/100.)
    p = pd.concat([p_f, pd.DataFrame(p_t).T.reset_index(drop=True)], axis=1)
    
    return gn, v, s, vm, p

# Processing functions from Gritscope to Pandapower

def reconstruct_buses(grid: Grid) -> pd.DataFrame:
    """Return DataFrame with bus data from grid."""
    
    ns = unique(chain(chain.from_iterable(grid.topo.cn.values()),
                      chain.from_iterable(grid.topo.ln.values()),
                      chain.from_iterable(grid.topo.gn.values())))
    
    buses = pd.DataFrame(index=list(ns))
    
    # kV-phase-to-phase = V*(V-phase-to-phase/V)*(kV/V)
    buses['vn_kv'] = [grid.params.v[n]*np.sqrt(3)*1e-3 for n in buses.index]
    
    return buses.reset_index(names='name')

def reconstruct_lines(grid: Grid, net: Net) -> pd.DataFrame:
    """Return DataFrame with line data from grid."""
    
    bus_idx = dict(zip(net.bus['name'], net.bus.index))
    
    is_line = lambda c: grid.params.n[c] == 1.
    lines = pd.DataFrame(index=list(filter(is_line, grid.topo.cn.keys())))
    
    lines['from_bus'] = [bus_idx[grid.topo.cn[c][0]] for c in lines.index]
    lines['to_bus'] = [bus_idx[grid.topo.cn[c][1]] for c in lines.index]
    lines['parallel'] = 1
    
    # km = km
    lines['length_km'] = 1.
    
    # Ohm = 1/Siemens
    x = np.array([np.imag(1/grid.params.y[c]) for c in lines.index])
    r = np.array([np.real(1/grid.params.y[c]).real for c in lines.index])
    
    # (Ohm/km) = Ohm/km
    lines['x_ohm_per_km'] = x/lines['length_km']
    lines['r_ohm_per_km'] = r/lines['length_km']
    
    # Siemens = Siemens
    b = np.array([grid.params.yg[c].imag for c in lines.index])
    g = np.array([grid.params.yg[c].real for c in lines.index])
    
    # (nF/km) = Siemens/km/Hz/([rad/s]/Hz)*(nF/F)
    lines['c_nf_per_km'] = b/lines['length_km']/net.f_hz/(2*np.pi)*1e9
    
    # (μSiemens/km) = Siemens/km*(μSiemens/Siemens)
    lines['g_us_per_km'] = g/lines['length_km']*1e6
    
    # kA = A*(kA/A)
    lines['max_i_ka'] = [grid.params.l[c]*1e-3 for c in lines.index]
    
    lines['std_type'] = None
    lines['df'] = 1.
    
    return lines.reset_index(names='name')

def reconstruct_trafos(grid: Grid, net: Net) -> pd.DataFrame:
    """Return DataFrame with transformer data from grid."""
    
    bus_idx = dict(zip(net.bus['name'], net.bus.index))
    
    is_trafo = lambda c: grid.params.n[c] != 1.
    trafos = pd.DataFrame(index=list(filter(is_trafo, grid.topo.cn.keys())))
    
    trafos['lv_bus'] = [bus_idx[grid.topo.cn[c][0]] for c in trafos.index]
    trafos['hv_bus'] = [bus_idx[grid.topo.cn[c][1]] for c in trafos.index]
    trafos['parallel'] = 1
    
    # MVA = V*A*(MVA/VA)
    pb = [grid.params.v[c]*grid.params.l[c]*1e-6 for c in trafos.index]
    
    # Dimensionless = Dimensionless
    w = [np.abs(grid.params.n[c]) for c in trafos.index]
    
    # Radians = Radians
    ps = [np.angle(grid.params.n[c]) for c in trafos.index]
    
    # MVA-three-phase = MVA*(VA-three-phase/VA)
    trafos['sn_mva'] = np.array(pb)*3.
    
    # Degrees = Radians*(Degree/Radians)
    trafos['shift_degree'] = np.array(ps)*(360/(2*np.pi))
    
    # kV = V*(kV/V)
    v_l = [grid.params.v[grid.topo.cn[c][0]]*1e-3 for c in trafos.index]
    v_h = [grid.params.v[grid.topo.cn[c][1]]*1e-3 for c in trafos.index]
    
    # kV-phase-to-phase = kV*(V-phase-to-phase/V)
    trafos['vn_lv_kv'] = np.array(v_l)*np.sqrt(3)
    
    # kV = kV*(V-phase-to-phase/V)*Dimensionless
    trafos['vn_hv_kv'] = np.array(v_l)*np.sqrt(3)*np.array(w)
    
    # Ohm = 1/Siemens
    zm = [np.abs(1/grid.params.y[c]) for c in trafos.index]
    r = [np.real(1/grid.params.y[c]) for c in trafos.index]
    
    # Percent = Ohm*MVA/(kV**2)*Percent
    trafos['vk_percent'] = np.array(zm)*np.array(pb)/(np.array(v_h)**2)*100.
    trafos['vkr_percent'] = np.array(r)*np.array(pb)/(np.array(v_h)**2)*100.
    
    # Siemens = Siemens
    ygm = [np.abs(grid.params.yg[c]) for c in trafos.index]
    g = [np.real(grid.params.yg[c]) for c in trafos.index]
    
    # Percent = Siemens/MVA*(kV**2)*Percent
    trafos['i0_percent'] = np.array(ygm)/np.array(pb)*np.array(v_h)**2*100.
    
    # kW-three-phase = Siemens*(kV**2)*(kW/MW)*(W-three-phase*/W)
    trafos['pfe_kw'] = np.array(g)*np.array(v_h)**2*1e3*3
    
    trafos['std_type'] = None
    trafos['df'] = 1.
    trafos['tap_phase_shifter'] = False
    trafos['tap_step_percent'] = 0.
    trafos['tap_pos'] = 0.
    trafos['max_loading_percent'] = 100.
    
    return trafos.reset_index(names='name')

def reconstruct_loads(grid: Grid, net: Net, ts: int) -> pd.DataFrame:
    """Return DataFrames with load data from grid."""
    
    bus_idx = dict(zip(net.bus['name'], net.bus.index))
    
    loads = pd.DataFrame(index=list(grid.topo.ln.keys()))
    
    loads['bus'] = [bus_idx[grid.topo.ln[c][0]] for c in loads.index]
    
    # MVA-three-phase = MVA*(MVA/VA)*(VA-three-phase/VA)
    loads['p_mw'] = [-grid.profs.p[l][ts]*1e-6*3. for l in loads.index]
    loads['q_mvar'] = [-grid.profs.q[l][ts]*1e-6*3. for l in loads.index]
    
    loads['scaling'] = 1.
    loads['const_z_percent'] = 0.
    loads['const_i_percent'] = 0.
    
    return loads.reset_index(names='name')

def reconstruct_gens(grid: Grid, net: Net, ts: int) -> pd.DataFrame:
    """Return DataFrames with generator data from grid."""
    
    bus_idx = dict(zip(net.bus['name'], net.bus.index))
    
    gens = pd.DataFrame(index=list(grid.topo.gn.keys()))
    
    gens['bus'] = [bus_idx[grid.topo.gn[c][0]] for c in gens.index]
    
    # Weight = Weight
    gens['slack_weight'] = [grid.params.s[g] for g in gens.index]
    
    # MVA-three-phase = MVA*(MVA/VA)*(VA-three-phase/VA)
    gens['p_mw'] = [grid.profs.p[g][ts]*1e-6*3. for g in gens.index]
    
    # Dimensionless = V/V
    gens['vm_pu'] = [grid.profs.v[g][ts]/grid.params.v[g] for g in gens.index]
    
    gens['slack'] = gens['slack_weight'] > 0
    gens['scaling'] = 1.
    
    return gens.reset_index(names='name')

# Preprocessing to ensure unique element names

def check_unique_names(net: Net) -> bool:
    """Return True if all network elements are uniquely named."""
    
    seen: set[Hashable] = set()
    for e in ELEMENTS:
        for n in getattr(net, e)['name'].values:
            if n in seen:
                return False
            else:
                seen.add(n)
    return True

def rename_elements(net: Net) -> Net:
    """Return Pandapower network with uniquely renamed elements."""
    
    net = Net(net)
    for e in ELEMENTS:
        names = e + '_' + getattr(net, e).index.to_series().astype(str)
        getattr(net, e)['name'] = names
    return net

# Helper functions

def get_col(frame: pd.DataFrame,
            key: str,
            default: float,
            name: str) -> pd.Series[float] | float:
    """Return Series or print warning and return default float."""
    
    if key not in frame:
        logging.warning(f"'{key}' not in '{name}' table, using {default}")
        return default
    else:
        if frame[key].hasnans:
            logging.warning(f"missing data in '{name}[{key}]', using {default}")
            return frame[key].fillna(default)
        else:
            return frame[key]

A = TypeVar('A', float, complex)

def param_dict(series: pd.Series, cast: Type[A] = float) -> dict[Hashable, A]:
    """Return parameter dictionary from Series."""
    
    return {k: cast(v) for k, v in zip(series.index, series)}
