from __future__ import annotations # Default behavior pending PEP 649

from functools import partial

from collections.abc import Iterator
from typing import Hashable, Mapping, Collection, Callable

import numpy as np
import numpy.typing as npt

from stylet.specific import T2, T3

from gritscope.topology.abc import TopoCoords
from gritscope.search.metrics import PS, TS, flatten, c_reduce

from .protocol import GridData
from .fdpf import FDPFInit, FDPFState, fdpf
from .flow import (PFInit, PFState, loadings, diff_loadings,
                   real_flows, reactive_flows)

# Types for edge and profile encodings

P = int
E = Hashable

# Types for tensor labels

class ES(tuple[E, ...]): ...

# Types for power flow initialization and state storage

Inits = dict[TopoCoords, FDPFInit]
States = dict[tuple[TopoCoords, PS], FDPFState]

# Main function for power flow computation

def pf(topos: Mapping[TopoCoords, Collection[TopoCoords]],
       profs: Collection[P],
       grid: GridData,
       state_cache: States = {},
       init_cache: Inits = {}) -> tuple[States, Inits]:
    """Return topology power flow results and initializations."""
    
    ps = PS(profs)
    
    sc = dict(state_cache)
    ic = dict(init_cache)
    
    for t in flatten(topos):
        if (t, ps) in sc:
            continue
        g = grid.apply_coords(t)
        if t not in ic:
            ic[t] = FDPFInit.build(g)
        sc[(t, ps)] = fdpf(FDPFState.build(g, ic[t], np.array(ps)), ic[t])
    
    return (sc, ic)

# Type for edge result functions

EFunc = Callable[[PFState, PFInit, GridData],
                 tuple[npt.NDArray[np.float_ | np.complex_], dict[E, int]]]

# Main function for collection of edge results

def edge_results(topos: Mapping[TopoCoords, Collection[TopoCoords]],
                 profs: Collection[P],
                 grid: GridData,
                 func: EFunc,
                 state_cache: States = {},
                 init_cache: Inits = {}) -> tuple[T3[np.float_,
                                                     PS, TS, ES],
                                                  States,
                                                  Inits]:
    """Return edge results for topologies using passed function."""
    
    ps = PS(profs)
    ts = TS(flatten(topos))
    es = ES(grid.topo.cn.keys())
    
    sc, ic = pf(topos, profs, grid, state_cache, init_cache)
    
    vss = []
    for t in ts:
        rs, ix = func(sc[(t, ps)], ic[t], grid.apply_coords(t))
        rss = [rs[:, ix[e]] if e in ix else np.zeros(rs.shape[0])
               for e in es]
        vss.append(np.stack(rss, axis=-1))
        
    vs = np.stack(vss, axis=1)
    
    return (T3((vs, (ps, ts, es))), sc, ic)

# Topology metrics

def converged(topos: Mapping[TopoCoords, Collection[TopoCoords]],
              profs: Collection[P],
              grid: GridData,
              state_cache: States = {},
              init_cache: Inits = {}) -> tuple[T2[np.bool_,
                                                  PS, TS],
                                               States,
                                               Inits]:
    """Return converged flag for topologies."""
    
    ps = PS(profs)
    ts = TS(flatten(topos))
    
    sc, ic = pf(topos, profs, grid, state_cache, init_cache)
    
    vs = np.stack([sc[(t, ps)].conv for t in ts], axis=-1)
    
    return (T2((vs, (ps, ts))), sc, ic)

def edge_real_power(topos: Mapping[TopoCoords, Collection[TopoCoords]],
                    profs: Collection[P],
                    grid: GridData,
                    state_cache: States = {},
                    init_cache: Inits = {}) -> tuple[T3[np.float_,
                                                        PS, TS, ES],
                                                     States,
                                                     Inits]:
    """Return edge real power flows for topologies."""
    
    l, sc, ic = edge_results(topos, profs, grid, real_flows,
                             state_cache, init_cache)
    
    return (l, sc, ic)

def edge_reactive_power(topos: Mapping[TopoCoords, Collection[TopoCoords]],
                        profs: Collection[P],
                        grid: GridData,
                        state_cache: States = {},
                        init_cache: Inits = {}) -> tuple[T3[np.float_,
                                                            PS, TS, ES],
                                                         States,
                                                         Inits]:
    """Return edge reactive power flows for topologies."""
    
    l, sc, ic = edge_results(topos, profs, grid, reactive_flows,
                             state_cache, init_cache)
    
    return (l, sc, ic)

def edge_loadings(topos: Mapping[TopoCoords, Collection[TopoCoords]],
                  profs: Collection[P],
                  grid: GridData,
                  state_cache: States = {},
                  init_cache: Inits = {}) -> tuple[T3[np.float_,
                                                      PS, TS, ES],
                                                   States,
                                                   Inits]:
    """Return edge current loadings for topologies."""
    
    l, sc, ic = edge_results(topos, profs, grid, loadings,
                             state_cache, init_cache)
    
    return (l, sc, ic)

def edge_diff_loadings(topos: Mapping[TopoCoords, Collection[TopoCoords]],
                       profs: Collection[P],
                       grid: GridData,
                       state_cache: States = {},
                       init_cache: Inits = {},
                       lim: float = 30.) -> tuple[T3[np.float_,
                                                     PS, TS, ES],
                                                  States,
                                                  Inits]:
    """Return angle-difference loadings for topologies."""
    
    l, sc, ic = edge_results(topos, profs, grid, partial(diff_loadings, lim=lim),
                             state_cache, init_cache)
    
    return (l, sc, ic)

def edge_overloads(topos: Mapping[TopoCoords, Collection[TopoCoords]],
                   profs: Collection[P],
                   grid: GridData,
                   state_cache: States = {},
                   init_cache: Inits = {}) -> tuple[T3[np.float_,
                                                       PS, TS, ES],
                                                    States,
                                                    Inits]:
    """Return edge current overloads for topologies."""
    
    l, sc, ic = edge_loadings(topos, profs, grid,
                              state_cache, init_cache)
    l = T3((np.maximum(l.values - 1., 0), l.labels))
    
    return (l, sc, ic)

def edge_diff_overloads(topos: Mapping[TopoCoords, Collection[TopoCoords]],
                        profs: Collection[P],
                        grid: GridData,
                        state_cache: States = {},
                        init_cache: Inits = {},
                        lim: float = 30.) -> tuple[T3[np.float_,
                                               PS, TS, ES],
                                            States,
                                            Inits]:
    """Return edge angle overloads for topologies."""
    
    l, sc, ic = edge_diff_loadings(topos, profs, grid,
                                   state_cache, init_cache, lim)
    l = T3((np.maximum(l.values - 1., 0), l.labels))
    
    return (l, sc, ic)

def weighted_overload(topos: Mapping[TopoCoords, Collection[TopoCoords]],
                      profs: Collection[P],
                      grid: GridData,
                      state_cache: States = {},
                      init_cache: Inits = {}) -> tuple[T3[np.float_,
                                                          PS, TS, ES],
                                                       States,
                                                       Inits]:
    """Return sum of overloads weighted by real power."""
    
    l, sc, ic = edge_overloads(topos, profs, grid, state_cache, init_cache)
    p, sc, ic = edge_real_power(topos, profs, grid, sc, ic)
    
    l = T3((l.values*p[l.labels].values, l.labels))
    
    return (l, sc, ic)

def weighted_diff_overload(topos: Mapping[TopoCoords, Collection[TopoCoords]],
                           profs: Collection[P],
                           grid: GridData,
                           state_cache: States = {},
                           init_cache: Inits = {},
                           lim: float = 30.) -> tuple[T3[np.float_,
                                                         PS, TS, ES],
                                                      States,
                                                      Inits]:
    """Return sum of angle overloads weighted by real power."""
    
    l, sc, ic = edge_diff_overloads(topos, profs, grid,
                                    state_cache, init_cache, lim)
    p, sc, ic = edge_real_power(topos, profs, grid, sc, ic)
    
    l = T3((l.values*p[l.labels].values, l.labels))
    
    return (l, sc, ic)

def secure(topos: Mapping[TopoCoords, Collection[TopoCoords]],
           profs: Collection[P],
           grid: GridData,
           state_cache: States = {},
           init_cache: Inits = {}) -> tuple[T2[np.bool_,
                                               PS, TS],
                                            States,
                                            Inits]:
    """Return secure flag for topologies."""
    
    c, sc, ic = converged(topos, profs, grid, state_cache, init_cache)
    l, sc, ic = edge_loadings(topos, profs, grid, sc, ic)
    
    vs = (l.r(ES, np.max)[c.labels].values <= 1)*c.values
    
    return (T2((vs, c.labels)), sc, ic)

def diff_secure(topos: Mapping[TopoCoords, Collection[TopoCoords]],
                profs: Collection[P],
                grid: GridData,
                state_cache: States = {},
                init_cache: Inits = {},
                lim: float = 30.) -> tuple[T2[np.bool_,
                                              PS, TS],
                                           States,
                                           Inits]:
    """Return angle-secure flag for topologies."""
    
    c, sc, ic = converged(topos, profs, grid, state_cache, init_cache)
    l, sc, ic = edge_diff_loadings(topos, profs, grid, sc, ic, lim)
    
    vs = (l.r(ES, np.max)[c.labels].values <= 1)*c.values
    
    return (T2((vs, c.labels)), sc, ic)

def c_secure(topos: Mapping[TopoCoords, Collection[TopoCoords]],
             profs: Collection[P],
             grid: GridData,
             state_cache: States = {},
             init_cache: Inits = {}) -> tuple[T2[np.bool_,
                                                 PS, TS],
                                              States,
                                              Inits]:
    """Return contingency-secure flag for topologies."""
    
    s, sc, ic = secure(topos, profs, grid, state_cache, init_cache)
    
    return (c_reduce(topos, s, np.all), sc, ic)

def diff_c_secure(topos: Mapping[TopoCoords, Collection[TopoCoords]],
                  profs: Collection[P],
                  grid: GridData,
                  state_cache: States = {},
                  init_cache: Inits = {},
                  lim: float = 30.) -> tuple[T2[np.bool_,
                                                PS, TS],
                                             States,
                                             Inits]:
    """Return angle-contingency-secure flag for topologies."""
    
    s, sc, ic = diff_secure(topos, profs, grid, state_cache, init_cache, lim)
    
    return (c_reduce(topos, s, np.all), sc, ic)
