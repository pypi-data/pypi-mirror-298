from __future__ import annotations # Default behavior pending PEP 649

from collections.abc import Hashable
from typing import Protocol, Type, Self, Literal

from itertools import chain

import numpy as np
import numpy.typing as npt

from scipy.sparse import coo_array, dia_array # type: ignore

from pygrates.itertools import unique

from .protocol import GridData, GridTopo, GridParams, GridProfs, super_node

# To do:
# - Generator limits
# - Voltage determination for multiple generators on a bus
# - Power flow initialization using previous results
# - Fallback to parameters for missing profiles

# Types for bus and connection encodings

B = Hashable
C = Hashable

# Protocols for storing power flow initialization and state

class PFInit(Protocol):
    """Protocol for storing power initialization object."""
    
    bus: dict[B, int]
    pv: npt.NDArray[np.bool_]
    pq: npt.NDArray[np.bool_]
    
    @classmethod
    def build(cls: Type[Self], grid: GridData) -> Self: ...

class PFState(Protocol):
    """Protocol for storing power flow state object."""
    
    p: npt.NDArray[np.float_]
    q: npt.NDArray[np.float_]
    ang: npt.NDArray[np.float_]
    mag: npt.NDArray[np.float_]
    slack: npt.NDArray[np.float_]
    conv: npt.NDArray[np.bool_]
    
    @classmethod
    def build(cls: Type[Self],
              grid: GridData,
              init: PFInit,
              batch: npt.NDArray[np.int_]) -> Self: ...

# Functions for initializing power flow from grid data

def slack_factors(topo: GridTopo,
                  params: GridParams) -> dict[B, float]:
    """Return dictionary from buses to slack participation factors."""
    
    s: dict[B, float] = {}
    for g, bs in topo.gn.items():
        b = bs[0]
        s[b] = s.get(b, 0) + params.s[g]
    
    return s

def admittances(topo: GridTopo,
                params: GridParams,
                ratios: None | Literal[1] | Literal[2] = None,
                shunt: bool = False) -> dict[tuple[B, B], complex]:
    """Return dictionary from bus pairs to per-unit admittances."""
    
    data = params.yg if shunt else params.y
    n = windings(topo, params)
    
    y: dict[tuple[B, B], complex] = {}
    for c, ns in topo.cn.items():
        val = (data[c]*(params.v[c]**2/params.pb) if c in data
               else 0.)
        
        match ratios:
            case 1:
                vf = val*n[c].conjugate()
                vt = val*n[c]
            case 2:
                vf = val*n[c].conjugate()*n[c]
                vt = val
            case _:
                vf = vt = val
                
        y[ns] = y.get(ns, 0) + vf
        y[ns[::-1]] = y.get(ns[::-1], 0) + vt
    
    return y

def buses(topo: GridTopo) -> tuple[dict[B, int],
                                   npt.NDArray[np.bool_],
                                   npt.NDArray[np.bool_]]:
    """Return tuple of bus index, PV mask, PQ mask."""
    
    pv = pv_buses(topo)
    pq = pq_buses(topo)
    
    bus = {b: n for n, b in enumerate(pv + pq)}
    pv_mask = np.concatenate([np.ones(len(pv), np.bool_),
                              np.zeros(len(pq), np.bool_)])
    pq_mask = np.concatenate([np.zeros(len(pv), np.bool_),
                              np.ones(len(pq), np.bool_)])
    
    return bus, pv_mask, pq_mask

def pv_buses(topo: GridTopo) -> tuple[B, ...]:
    """Return tuple of buses with at least one generator."""
    
    return tuple(unique([ns[0] for ns in topo.gn.values()]))

def pq_buses(topo: GridTopo) -> tuple[B, ...]:
    """Return tuple of buses without any generator."""
    
    return tuple(unique(chain.from_iterable(topo.cn.values()),
                        exclude=set([ns[0] for ns in topo.gn.values()])))

def connections(topo: GridTopo,
                bus: dict[B, int]) -> tuple[dict[C, int],
                                            npt.NDArray[np.int_],
                                            npt.NDArray[np.int_]]:
    """Return tuple of connection index, from index, to index."""
    
    con = {c: k for k, c in enumerate(topo.cn)}
    fb, tb = zip(*[(bus[f], bus[t]) for f, t in topo.cn.values()])
    
    return con, np.array(fb), np.array(tb)

def windings(topo: GridTopo,
             params: GridParams) -> dict[C, complex]:
    """Return complex winding ratios in per unit."""
    
    n: dict[C, complex] = {}
    for c, (f, t) in topo.cn.items():
        vf, vt = params.v[super_node(f)], params.v[super_node(t)]
        n[c] = params.n.get(c, complex(1.))/(vt/vf)
    
    return n

def adjacency(topo: GridTopo,
              params: GridParams,
              bus: dict[B, int],
              ratios: None | Literal[1] | Literal[2] = None,
              shunt: bool = False) -> coo_array:
    """Return sparse bus adjacency matrix weighted by admittance."""
    
    yb = admittances(topo, params, ratios, shunt)
    
    elements: list[tuple[int, int, complex]] = []
    for bp, y in yb.items():
        elements.append((bus[bp[0]], bus[bp[1]], y))
    
    row, col, data = zip(*elements)
    
    return coo_array((data, (row, col)), shape=2*[len(bus)])

def laplacian(topo: GridTopo,
              params: GridParams,
              bus: dict[B, int],
              ratios: bool = False,
              shunt: bool = False) -> coo_array:
    """Return sparse bus laplacian matrix weighted by admittance."""
    
    if ratios:
        a = adjacency(topo, params, bus, 1, False)
        ad = adjacency(topo, params, bus, 2, False)
        d = dia_array((ad.sum(axis=1),[0]), shape=a.shape)
    else:
        a = adjacency(topo, params, bus, None, False)
        d = dia_array((a.sum(axis=1), [0]), shape=a.shape)
    
    if shunt:
        s = adjacency(topo, params, bus, 2 if ratios else None, True)
        ds = dia_array((s.sum(axis=1),[0]), shape=a.shape)
        d = d + ds/2
    
    return coo_array(d - a)

def slack_array(topo: GridTopo,
                params: GridParams,
                bus: dict[B, int]) -> npt.NDArray[np.float_]:
    """Return dense array of bus slack participation factors."""
    
    s = slack_factors(topo, params)
    
    return np.array([s.get(b, 0) for b in bus])

def p_profs(grid: GridData,
            init: PFInit,
            batch: npt.NDArray[np.int_]) -> npt.NDArray[np.float_]:
    """Return dense array of per-unit real power bus profiles."""
    
    lgb = grid.topo.ln | grid.topo.gn
    
    p = {b: np.zeros(len(batch), np.float_) for b in init.bus}
    for lg, bs in lgb.items():
        b = bs[0]
        profs = np.asarray(grid.profs.p[lg][batch], np.float_)
        base = np.float_(grid.params.pb)
        p[b] = p[b] + profs/base
    
    return np.stack(tuple(p.values()), axis=-1)

def q_profs(grid: GridData,
            init: PFInit,
            batch: npt.NDArray[np.int_]) -> npt.NDArray[np.float_]:
    """Return dense array of per-unit reactive power bus profiles."""
    
    q = {b: np.zeros(len(batch), np.float_) for b in init.bus}
    for lg, bs in grid.topo.ln.items():
        b = bs[0]
        profs = np.asarray(grid.profs.q[lg][batch], np.float_)
        base = np.float_(grid.params.pb)
        q[b] = q[b] + profs/base
    
    return np.stack(tuple(q.values()), axis=-1)

def mag_profs(grid: GridData,
              init: PFInit,
              batch: npt.NDArray[np.int_]) -> npt.NDArray[np.float_]:
    """Return dense array of per-unit voltage magnitude bus profiles."""
    
    mag = {b: np.ones(len(batch), np.float_) for b in init.bus}
    for lg, bs in grid.topo.gn.items():
        b = bs[0]
        profs = np.asarray(grid.profs.v[lg][batch], np.float_)
        base = np.float_(grid.params.v[lg])
        mag[b] = np.maximum(mag[b], profs/base)
    
    return np.stack(tuple(mag.values()), axis=-1)

def ang_profs(init: PFInit,
              batch: npt.NDArray[np.int_]) -> npt.NDArray[np.float_]:
    """Return dense array of flat-start bus voltage angles."""
    
    return np.zeros([len(batch), len(init.bus)], np.float_)

def slack_profs(batch: npt.NDArray[np.int_]) -> npt.NDArray[np.float_]:
    """Return dense array of flat-start slack power."""
    
    return np.zeros([len(batch), 1], np.float_)

# Functions for computing result quantities from power flow state

def complex_currents(state: PFState,
                     init: PFInit,
                     grid: GridData) -> tuple[npt.NDArray[np.complex_],
                                              npt.NDArray[np.complex_],
                                              npt.NDArray[np.complex_],
                                              npt.NDArray[np.complex_],
                                              npt.NDArray[np.float_],
                                              dict[C, int]]:
    """Return dense array of complex connection currents in per-unit."""
    
    con, fb, tb = connections(grid.topo, init.bus)
    win = windings(grid.topo, grid.params)
    y = np.array([grid.params.y[c] for c in con])
    yg = np.array([grid.params.yg[c] for c in con])
    vb = np.array([grid.params.v[c] for c in con])
    n = np.array([win[c] for c in con])
    
    v = state.mag*(np.cos(state.ang) + 1j*np.sin(state.ang))
    vf, vt = v[..., fb]*n, v[..., tb]
    vdiff = vf - vt
    
    jf, jt, = y*vdiff + vf*yg/2, y*vdiff - vt*yg/2
    
    return jf, jt, vdiff, y, vb, con

def flows(state: PFState,
          init: PFInit,
          grid: GridData) -> tuple[npt.NDArray[np.float_],
                                   dict[C, int]]:
    """Return dense array of connection current flows."""
    
    jf, jt, _, _, vb, con = complex_currents(state, init, grid)
    
    fs = vb*np.maximum(np.abs(jf), np.abs(jt))
    
    mask = np.expand_dims(np.where(state.conv, 0., np.inf), axis=1)
    
    return fs + mask, con

def loadings(state: PFState,
             init: PFInit,
             grid: GridData) -> tuple[npt.NDArray[np.float_],
                                      dict[C, int]]:
    """Return dense array of connection loadings relative to limits."""
    
    f, con = flows(state, init, grid)
    
    l = np.array([grid.params.l[c] for c in con])
    
    return f/l, con

def ang_diffs(state: PFState,
              init: PFInit,
              grid: GridData) -> tuple[npt.NDArray[np.float_],
                                       dict[C, int]]:
    """Return dense array of connection voltage angle differences."""
    
    con, fb, tb = connections(grid.topo, init.bus)
    ps = np.angle(np.array([grid.params.n.get(c, 1. + 0j) for c in con]))
    
    ads = np.abs(state.ang[..., tb] - state.ang[..., fb] - ps)/(2.*np.pi)*360.
    
    mask = np.expand_dims(np.where(state.conv, 0., np.inf), axis=1)
    
    return ads + mask, con

def diff_loadings(state: PFState,
                  init: PFInit,
                  grid: GridData,
                  lim: float = 30.) -> tuple[npt.NDArray[np.float_],
                                             dict[C, int]]:
    """Return dense array of connection angles relative to limits."""
    
    d, con = ang_diffs(state, init, grid)
    
    return d/lim, con

def real_flows(state: PFState,
               init: PFInit,
               grid: GridData) -> tuple[npt.NDArray[np.complex_],
                                        dict[C, int]]:
    """Return dense array of connection real power flows."""
    
    _, _, vdiff, y, vb, con = complex_currents(state, init, grid)
    ang = np.angle(vdiff)
    
    mask = np.expand_dims(np.where(state.conv, 0., np.inf), axis=1)
    
    return np.abs(np.imag(y)*vdiff*vb**2)*3 + mask, con

def reactive_flows(state: PFState,
                    init: PFInit,
                    grid: GridData) -> tuple[npt.NDArray[np.complex_],
                                             dict[C, int]]:
    """Return dense array of connection reactive power flows."""
    
    _, _, vdiff, y, vb, con = complex_currents(state, init, grid)
    ang = np.angle(vdiff)
    
    mask = np.expand_dims(np.where(state.conv, 0., np.inf), axis=1)
    
    return np.abs(np.real(y)*vdiff*vb**2)*3 + mask, con
