from __future__ import annotations # Default behavior pending PEP 649

from collections.abc import Hashable, Mapping, Collection, Iterator
from typing import Literal, Any, TypeVar, Generic, overload

from collections import Counter
from itertools import chain, repeat

import numpy as np

from pygrates.itertools import unique

from stylet.general import T, RFunc
from stylet.specific import T1, T2, T3

from gritscope.topology.abc import TopoCoords

# Types for profile encodings

P = TypeVar('P', bound=Hashable)

# Types for topology map

TCS = Mapping[TopoCoords, Collection[TopoCoords]]

# Types for tensor labels

class PS(tuple[P, ...], Generic[P]): ...
class TS(tuple[TopoCoords, ...]): ...

def c_reduce(topos: Mapping[TopoCoords, Collection[TopoCoords]],
             metric: T2[Any, PS, TS],
             func: RFunc) -> T2[Any, PS, TS]:
    
    ps = metric.labels[0]
    ts = TS(topos.keys())
    
    vs = np.stack([metric[(ps, TS(topos[t]))].r(TS, func).values for t in ts],
                  axis=-1)
    
    return T2((vs, (ps, ts)))

def select(topos: Mapping[TopoCoords, Collection[TopoCoords]],
           metric: T2[np.float_, PS[P], TS],
           crit: Literal['min', 'max'] = 'min') -> tuple[T1[np.float_, PS],
                                                         dict[P, TopoCoords]]:
    
    match crit:
        case 'min': rfunc, ifunc = np.min, np.argmin
        case 'max': rfunc, ifunc = np.max, np.argmax
    
    ps = metric.labels[0]
    ts = TS(topos.keys())
    m = metric[(ps, ts)]
    
    vs, ix = rfunc(m.values, axis=-1), ifunc(m.values, axis=-1)
    ls = np.fromiter(m.labels[1], dtype=np.object_)[ix]
    
    return (T1((vs, (ps,))), {p: l for p, l in zip(ps, ls)})

# Functions for looking up values for topologies in a metric

DT = TypeVar('DT', bound=np.generic)
E1 = TypeVar('E1', bound=Collection[Hashable])

def lookup(pts: dict[P, TopoCoords],
           metric: T1[DT, TS]) -> T1[DT, PS]:
    
    ps = PS(pts.keys())
    
    vs = [metric.s(TS, t).values for t in pts.values()]
    
    return T1((np.fromiter(vs, dtype=metric.dtype), (ps,)))

@overload
def p_lookup(pts: dict[P, TopoCoords],
             metric: T2[DT, PS, TS]) -> T1[DT, PS]: ...

@overload
def p_lookup(pts: dict[P, TopoCoords],
             metric: T3[DT, PS, TS, E1]) -> T2[DT, PS, E1]: ...

def p_lookup(pts: dict[P, TopoCoords],
             metric: T2[DT, PS, TS] | T3[DT, PS, TS, E1]) -> T[DT, Any]:
    
    ps = PS(pts.keys())
    ix = np.array([metric.idx[1][t] for t in pts.values()], dtype=np.int_)
    
    match metric:
        case T2():
            vs = np.take_along_axis(metric.values,
                                    np.expand_dims(ix, axis=1), axis=1)
            return T1((np.squeeze(vs, axis=1), (ps,)))
        case T3():
            vs = np.take_along_axis(metric.values,
                                    np.expand_dims(ix, axis=(1, 2)), axis=1)
            return T2((np.squeeze(vs, axis=1), (ps, metric.labels[2])))

# Functions for obtaining topology details

def n_switches(pts: dict[P, TopoCoords]) -> T1[np.int_, PS]:
    
    ps = PS(pts.keys())
    vs = np.array([len(t.e_coord) for t in pts.values()], dtype=np.int_)
    
    return T1((vs, (ps,)))

def n_splits(pts: dict[P, TopoCoords]) -> T1[np.int_, PS]:
    
    ps = PS(pts.keys())
    vs = np.array([len(t.n_coord) for t in pts.values()], dtype=np.int_)
    
    return T1((vs, (ps,)))

def count(pts: dict[P, TopoCoords]) -> T1[np.int_, TS]:
    
    cs = Counter(pts.values())
    vs = np.fromiter(cs.values(), dtype=np.int_)
    
    return T1((vs, (TS(cs.keys()),)))

def most_frequent(pts: dict[P, TopoCoords], k: int) -> T1[np.str_, TS]:
    
    cs = count(pts)
    ix = np.argsort(cs.values)[::-1]
    ts = np.fromiter(cs.labels[0], dtype=np.object_)[ix]
    vs = [str(l) for _, l in zip(ts, chain(range(1, k + 1), repeat('Other')))]
    
    return T1((np.array(vs, dtype=np.str_), (TS(ts),))) 

# Helper function to flatten topology-contingency maps

O = TypeVar('O')

def flatten(o_map: Mapping[O, Collection[O]]) -> Iterator[O]:
    """Return iterator of unique objects from nested mapping."""
    
    return unique(chain.from_iterable(chain([o], o_map[o]) for o in o_map))
