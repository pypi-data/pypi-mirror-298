from __future__ import annotations # Default behavior pending PEP 649

from abc import ABC, abstractmethod
from collections.abc import Iterable, Iterator, Hashable
from typing import Self, TypeVar, Generic
from itertools import chain

from pygrates.abc import DAGCoords

# Generic types for topology coordinate implementations

ECoord = TypeVar('ECoord', bound=Hashable)
NCoord = TypeVar('NCoord', bound=Hashable)

# Base topology coordinate class to implement for using topology functions

class TopoCoords(DAGCoords, Generic[ECoord, NCoord], ABC):
    """Base class for possible alterations to a graph topology."""
    
    __slots__ = ()
    
    @abstractmethod
    def e_children(self) -> Iterable[Self]:
        """Return iterable containing children in the edge dimension."""
        
        raise NotImplementedError
    
    @abstractmethod
    def n_children(self) -> Iterable[Self]:
        """Return iterable containing children in the node dimension."""
        
        raise NotImplementedError
    
    @abstractmethod
    def e_parents(self) -> Iterable[Self]:
        """Return iterable containing parents in the edge dimension."""
        
        raise NotImplementedError
    
    @abstractmethod
    def n_parents(self) -> Iterable[Self]:
        """Return iterable containing parents in the node dimension."""
        
        raise NotImplementedError
    
    @abstractmethod
    def contingencies(self) -> Iterable[Self]:
        """Return iterable containing contingencies of topology."""
        
        raise NotImplementedError
    
    @property
    @abstractmethod
    def e_coord(self) -> ECoord: 
        """Return the set of edge changes to the topology."""
        
        raise NotImplementedError
    
    @property
    @abstractmethod
    def n_coord(self) -> NCoord: 
        """Return the set of node changes to the topology."""
        
        raise NotImplementedError
    
    def children(self) -> Iterator[Self]:
        """Return iterator containing children."""
        
        return chain(self.e_children(), self.n_children())
    
    def parents(self) -> Iterator[Self]:
        """Return iterator containing parents."""
        
        return chain(self.e_parents(), self.n_parents())
    
    def is_e_child(self, other: Self) -> bool:
        """Return True if self is a edge-child of other."""
        
        e_parents: Iterable[Self] = self.e_parents()
        return any(coords == other for coords in e_parents)
    
    def is_n_child(self, other: Self) -> bool:
        """Return True if self is a node-child of other."""
        
        n_parents: Iterable[Self] = self.n_parents()
        return any(coords == other for coords in n_parents)
    
    def is_e_parent(self, other: Self) -> bool:
        """Return True if self is a edge-parent of other."""
        
        e_children: Iterable[Self] = self.e_children()
        return any(coords == other for coords in e_children)
    
    def is_n_parent(self, other: Self) -> bool:
        """Return True if self is a node-parent of other."""
        
        n_children: Iterable[Self] = self.n_children()
        return any(coords == other for coords in n_children)
    
    def __eq__(self, other: object) -> bool:
        
        if isinstance(other, type(self)):
            return (self.e_coord == other.e_coord
                    and self.n_coord == other.n_coord)
        else:
            return NotImplemented
    
    def __hash__(self) -> int:
        
        return hash(self.e_coord) ^ hash(self.n_coord)
