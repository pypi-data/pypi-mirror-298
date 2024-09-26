from __future__ import annotations # Default behavior pending PEP 649

from collections.abc import Hashable, Collection, Iterator, Mapping, Set
from typing import Type

from itertools import repeat

from pygrates.itertools import unique
from pygrates.graphs import inverse, compound, degrees, subsources

from .graphs import node_degrees, edge_degree_filter, assert_minimum_degree
from .coords import ESpace, NSpace, ECoord, NCoord, TopoTuple
from .itertools import splits, attach, distribute, flatset

# Types for edge and node encodings

E = Hashable
N = Hashable

ENS = Mapping[E, Collection[N]]

Split = tuple[frozenset[E], ...] | frozenset[frozenset[E]]
NSplit = tuple[N, Split]

# Main functions for creating edge switch and node split coordinate spaces

def edge_space(switchables: Collection[E],
               connected: Mapping[E, Collection[N]],
               min_deg: int = 2,
               exclude: Set[E] = frozenset()) -> ESpace:
    """Return edge coordinate space from passed switchable edges."""
    
    nds = node_degrees(connected, min_deg)
    
    assert_minimum_degree(nds, min_deg) # ValueError if failed
    
    at_min = {e for e in connected if any(nds[n] == min_deg
                                          for n in connected[e])}
    
    return ESpace({e for e in switchables if not e in exclude | at_min})

def node_space(splittables: Mapping[N, Collection[Collection[E]]],
               connected: Mapping[E, Collection[N]],
               ens: Mapping[E, Collection[N]],
               min_deg: int = 2,
               max_splits: int | Collection[int] = 2) -> NSpace:
    """Return node coordinate space from passed splittable nodes."""
    
    nes = inverse(ens)
    nds = node_degrees(connected, min_deg)
    ncs = inverse(edge_degree_filter(connected, (2,)))
    
    assert_minimum_degree(nds, min_deg) # ValueError if failed
    
    ms = repeat(max_splits) if isinstance(max_splits, int) else max_splits
    
    return NSpace({n: frozenset(node_splits(n, splittables[n],
                                            ncs.get(n, []),
                                            nes[n], min_deg, m))
                   for n, m in zip(splittables, ms)})

def topo_space(switchables: Collection[E],
               splittables: Mapping[N, Collection[Collection[E]]],
               contingencies: Collection[E],
               connected: Mapping[E, Collection[N]],
               ens: Mapping[E, Collection[N]],
               coord_name: str = 'Coords',
               min_deg: int = 2,
               max_splits: int = 2,) -> Type[TopoTuple]:
    """Return topology coordinate space as a coordinate class."""
    
    def root(cls: Type[TopoTuple]):
        return cls([ECoord(), NCoord()])
    
    return type(coord_name,
                (TopoTuple,),
                {'root': classmethod(root),
                 'e_space': edge_space(switchables, connected,  min_deg),
                 'c_space': edge_space(contingencies, ens, min_deg=0),
                 'n_space': node_space(splittables, connected, ens,
                                       min_deg, max_splits)})

def root(switchables: Collection[E],
         splittables: Mapping[N, Collection[Collection[E]]],
         contingencies: Collection[E],
         connected: Mapping[E, Collection[N]],
         ens: Mapping[E, Collection[N]],
         min_deg: int = 2,
         max_splits: int = 2) -> TopoTuple:
    
    class Coords(TopoTuple):
        e_space = edge_space(switchables, connected,  min_deg)
        n_space = node_space(splittables, connected, ens, min_deg, max_splits)
        c_space = edge_space(contingencies, ens, min_deg=0)
    
    return Coords([ECoord(), NCoord()])

# Helper functions

def node_splits(n: N,
                flex: Collection[Collection[E]],
                con: Collection[E],
                full: Collection[E],
                min_deg: int = 2,
                max_splits: int = 2,
                ordered: bool = False) -> Iterator[NSplit]:
    """Return possible node splits satistying minimum degree."""
    
    con_flex = set(frozenset(e for e in es if e in con) for es in flex)
    con_fix = set(con) - flatset(flex)
    other_flex = set(frozenset(e for e in es if e not in con) for es in flex)
    other_fix = set(full) - flatset(flex) - set(con)
    
    con_splits = splits(con_flex, min_deg, max_splits, con_fix)
    fix_splits = attach(other_fix, con_splits)
    full_splits = distribute(other_flex, fix_splits)
    
    if ordered:
        return ((n, tuple(s)) for s in full_splits)
    else:
        return unique((n, frozenset(s)) for s in full_splits)
