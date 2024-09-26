from __future__ import annotations # Default behavior pending PEP 649

from abc import ABC, abstractmethod
from collections.abc import Hashable, Iterable, Iterator, Set, Mapping
from typing import Self, Type, Callable, Any

from itertools import product, chain
from functools import reduce

from pygrates.collections import NamedFrozenSet, NamedFrozenDict

from .abc  import TopoCoords

# Types for edge and node encodings

E = Hashable
N = Hashable
Split = tuple[frozenset[E], ...] | frozenset[frozenset[E]]
NSplit = tuple[N, Split]

class ESpace(NamedFrozenSet[E]):
    """Space of all possible edge switches."""
    
    __slots__ = ()

class NSpace(NamedFrozenDict[N, frozenset[NSplit]]):
    """Space of all possible node splits."""
    
    __slots__ = ()

class ECoord(NamedFrozenSet[E]):
    """Edges that are switched."""
    
    __slots__ = ()
    
    def __repr__(self) -> str:
        
        return 'ECoord(' + sorted_set_repr(self) + ')'

class NCoord(NamedFrozenDict[N, NSplit]):
    """Nodes that are split."""
    
    __slots__ = ()
    
    def __repr__(self) -> str:
        
        split_repr = lambda s: [sorted_set_repr(es, frozen=True) for es in s]
        tuple_repr = lambda s: 'tuple(' + ', '.join(split_repr(s)) + ')'
        frozenset_repr = lambda s: sorted_set_repr(set(split_repr(s)),
                                                   f=str, frozen=True)
        
        splits = {n: '('
                  + repr(s[0])
                  + ', '
                  + (frozenset_repr(s[1])
                     if isinstance(s[1], frozenset)
                     else tuple_repr(s[1]))
                  + ')'
                  for n, s in self.items()}
        
        return 'NCoord(' + sorted_dict_repr(splits, fv=str) + ')'

# Topology coordinate implementation as a tuple

class TopoTuple(tuple[ECoord, NCoord], TopoCoords[ECoord, NCoord], ABC):
    """Coordinate class for possible alterations to a graph topology."""
    
    __slots__ = ()
    
    coupled = True
    
    @property
    @abstractmethod
    def e_space(self) -> ESpace:
        """Return the space of possible edge changes to the topology."""
        
        raise NotImplementedError
    
    @property
    @abstractmethod
    def n_space(self) -> NSpace:
        """Return the space of possible node changes to the topology."""
        
        raise NotImplementedError
    
    @property
    @abstractmethod
    def c_space(self) -> ESpace:
        """Return the space of possible contingencies."""
        
        raise NotImplementedError
    
    @property
    def e_coord(self) -> ECoord:
        """Return the set of edge changes to the topology."""
        
        return self[0]
    
    @property
    def n_coord(self) -> NCoord:
        """Return the set of node changes to the topology."""
        
        return self[1]
    
    @classmethod
    def factory(cls: Type[Self], 
                e_coords: Iterable[ECoord], 
                n_coords: Iterable[NCoord]) -> Iterator[Self]:
        """Return iterator with cartesian product of coordinates."""
        
        return map(cls, product(e_coords, n_coords))
    
    def e_children(self: Self, contingencies: bool = False) -> Iterator[Self]:
        """Return iterator containing children in the edge dimension."""
        
        space = self.c_space if contingencies else self.e_space
        unswitched = (e for e in space if e not in self.e_coord)
        e_coords = (ECoord(self.e_coord | {switch})
                    for switch in unswitched)
        
        if self.coupled:
            enss = (self.factory([e_coord], [self.e_remove(e_coord)])
                    for e_coord in e_coords)
            return chain.from_iterable(enss)
        
        else:
            return self.factory(e_coords, [self.n_coord])
    
    def e_parents(self: Self) -> Iterator[Self]:
        """Return iterator containing parents in the edge dimension."""
        
        switches = tuple(self.e_coord)
        e_coords = (ECoord(e for e in self.e_coord if not e == switch)
                    for switch in switches)
        
        if self.coupled:
            enss = (self.factory([e_coord], self.e_add(switch))
                    for switch, e_coord in zip(switches, e_coords))
            return chain.from_iterable(enss)
        
        else:
            return self.factory(e_coords, [self.n_coord])
    
    def n_children(self: Self) -> Iterator[Self]:
        """Return iterator containing children in the node dimension."""
        
        unsplit = (n for n in self.n_space if n not in self.n_coord)
        splits = (split for n in unsplit for split in self.n_space[n])
        n_coords = (NCoord(self.n_coord | {split[0]: split}) 
                    for split in splits)
        
        if self.coupled:
            ns = (n_coord_clean(n_coord, self.e_coord) for n_coord in n_coords)
            return self.factory([self.e_coord], ns)
        
        else:
            return self.factory([self.e_coord], n_coords)
    
    def n_parents(self: Self) -> Iterator[Self]:
        """Return iterator containing parents in the node dimension."""
        
        n_coords = (NCoord((n, self.n_coord[n]) 
                           for n in self.n_coord
                           if not n == split)
                    for split in self.n_coord)
        
        return self.factory([self.e_coord], n_coords)
    
    def contingencies(self: Self) -> Iterator[Self]:
        """Return iterator containing contingencies of topology."""
        
        return self.e_children(contingencies=True)
    
    def e_remove(self: Self, es: Set[E]) -> NCoord:
        """Return node coordinate with passed edges removed."""
        
        return n_coord_clean(self.n_coord, es)
    
    def e_add(self: Self, e: E) -> Iterator[NCoord]:
        """Return possible node coordinates with passed edge added."""
        
        union = lambda x, y: x | y
        return (NCoord({n: split}) for n in self.n_coord
                for split in self.n_space[n]
                if e in reduce(union, split[1]))
    
    def __repr__(self) -> str:
        
        name = type(self).__name__
        
        return f'{name}({tuple.__repr__(self)})'

# Coordinate logic helper functions

def n_coord_clean(n_coord: NCoord, es: Set[E]) -> NCoord:
    """Return passed node coordinate with passed edges removed."""
    
    cleaned = (split_clean(s, es) for s in n_coord.values())
    filtered = filter(lambda split: len(split[1]) > 1, cleaned)
    
    return NCoord({split[0]: split for split in filtered})

def split_clean(split: NSplit, switches: Set[E]) -> NSplit:
    """Return node split with passed edges removed."""
    
    n, ess = split
    filtered = type(ess)(frozenset(e for e in es if not e in switches)
                         for es in ess)
    
    return (n, filtered)

# Serialization helper functions

def sorted_set_repr(xs: Set,
                    f: Callable[[Any], str] = repr,
                    frozen: bool = False) -> str:
    """Return sorted string representation of set."""
    
    r = '{' + ', '.join(sorted(map(f, xs))) + '}'
    if frozen:
        return 'frozenset(' + r + ')'
    else:
        return r

def sorted_dict_repr(xs: Mapping,
                     fk: Callable[[Any], str] = repr,
                     fv: Callable[[Any], str] = repr) -> str:
    """Return sorted string representation of dict."""
    
    items = [fk(k) + ': ' + fv(v) for k, v in xs.items()]
    return '{' + ', '.join(sorted(items)) + '}'
