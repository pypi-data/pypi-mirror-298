from __future__ import annotations # Default behavior pending PEP 649

from itertools import starmap

from typing import Hashable, Callable

import numpy as np
import numpy.typing as npt

import pandas as pd

import pandapower as pp # type: ignore
from pandapower.auxiliary import pandapowerNet as Net # type: ignore

from gritscope.powergrid.grid import Grid
from gritscope.powergrid.fdpf import FDPFInit, FDPFState, fdpf
from gritscope.powergrid.flow import ang_diffs, flows, loadings
from gritscope.powergrid.pandapower import rename_elements, trafo_ratios

# Type for connection encoding

C = Hashable

# Power flow computation and results collection

def gs_results(grid: Grid, tol: float) -> pd.DataFrame:
    """Return DataFrame with power flow results."""
    
    # Dimensionless = VA/VA
    max_error = tol/grid.params.pb
    
    init = FDPFInit.build(grid)
    start = FDPFState.build(grid, init, grid.profs.p.f.index[0:1].to_numpy())
    final = fdpf(start, init, max_iter=100, max_error=max_error)
    
    assert final.conv
    
    edge_results = [f(final, init, grid) for f in (ang_diffs, flows, loadings)]
    ad, fl, lo = starmap(edge_result_series, edge_results)
    
    return pd.concat({'ang_diff': ad, 'flow': fl, 'loading':lo}, axis=1)

def pp_results(net: Net, tol: float) -> pd.DataFrame:
    """Return DataFrame with power flow results from Pandapower."""
    
    # MVA = VA*(MVA/VA)
    tol = tol*1e-6
    
    net = Net(net)
    pp.runpp(net, trafo_model='pi', distributed_slack=True, tolerance_mva=tol,
             calculate_voltage_angle=True, voltage_depend_loads=False)
    
    lines = pd.concat([net.line, net.res_line], axis=1).set_index('name')
    trafos = pd.concat([net.trafo, net.res_trafo], axis=1).set_index('name')
    trafos = pd.merge(trafos, net.bus, how='left', left_on='lv_bus',
                      right_index=True)
    trafos = pd.merge(trafos, net.bus, how='left', left_on='hv_bus',
                      right_index=True, suffixes=['_lv_bus', '_hv_bus'])
    
    # Dimensionless = kV/kV
    windings = trafos['vn_kv_hv_bus']/trafos['vn_kv_lv_bus']
    
    # Degrees = Degrees
    phaseshifts = np.angle(trafo_ratios(trafos), deg=True)
    
    # Degrees = Degrees
    lines['ang_diff'] = (lines['va_to_degree']
                         - lines['va_from_degree']).abs()
    trafos['ang_diff'] = (trafos['va_hv_degree']
                          - trafos['va_lv_degree']
                          - phaseshifts).abs()
    
    # A = kA*(A/kA)
    lines['flow'] = lines['i_ka']*1e3
    trafos['flow'] = np.maximum(trafos['i_lv_ka']/windings,
                                trafos['i_hv_ka'])*1e3
    
    # Dimensionless = Percent*(1/Percent)
    lines['loading'] = lines['loading_percent']*1e-2
    trafos['loading'] = trafos['loading_percent']*1e-2

    results = pd.concat([lines, trafos])
    
    return results.loc[:, ['ang_diff', 'flow', 'loading']]

def compare_powerflows(grid: Grid, net: Net, tol: float) -> pd.DataFrame:
    """Return DataFrame with differences in power flow edge results."""
    
    return (gs_results(grid, tol) - pp_results(net, tol)).abs()

# Helper functions

def edge_result_series(vals: npt.NDArray[np.float_],
                       idx: dict[C, int]) -> pd.Series[float]:
    """Return Series from edge result values and index."""
    
    return pd.Series(vals[0, np.array(list(idx.values()), np.int_)].T,
                     index=np.array(list(idx.keys())))
