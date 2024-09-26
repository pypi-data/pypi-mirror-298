from __future__ import annotations # Default behavior pending PEP 649

from collections.abc import Hashable, Mapping
from typing import Protocol, Self, TypeVar

import numpy as np
import numpy.typing as npt

from gritscope.topology.abc import TopoCoords

# Types for connection, load and generator encodings

C = Hashable
L = Hashable
G = Hashable

E = C | L | G
N = Hashable

# Protocols for power grid data and interaction with topology coordinates

class GridData(Protocol):
    """Protocol for storing power grid data."""
    
    topo: GridTopo
    params: GridParams
    profs: GridProfs
    
    def __init__(self: Self,
                 topo: GridTopo,
                 params: GridParams,
                 profs: GridProfs) -> None: ...
    
    def apply_coords(self: Self, coords: TopoCoords) -> Self:
        """Return grid data with topology changes from coordinates."""
        
        topo = self.topo.apply_coords(coords)
        
        return type(self)(topo, self.params, self.profs)

class GridTopo(Protocol):
    """Protocol for storing a grid topology."""
    
    cn: dict[C, tuple[N, N]]
    ln: dict[L, tuple[N]]
    gn: dict[G, tuple[N]]
    
    def __init__(self: Self,
                 cn: dict[C, tuple[N, N]],
                 ln: dict[L, tuple[N]],
                 gn: dict[G, tuple[N]]) -> None: ...
    
    def apply_coords(self: Self, coords: TopoCoords) -> Self:
        """Return grid topology with changes from coordinates."""
        
        splits = n_splits(coords)
        
        cn = cn_update(self.cn, coords.e_coord, splits)
        ln = lgn_update(self.ln, coords.e_coord, splits)
        gn = lgn_update(self.gn, coords.e_coord, splits)
        
        return type(self)(cn, ln, gn)

class GridParams(Protocol):
    """Protocol for storing grid parameters."""
    
    y: dict[C, complex]
    yg: dict[C, complex]
    n: dict[C, complex]
    s: dict[G, float]
    v: dict[N | L |G | C, float]
    l: dict[C, float]
    pb: float
    co: dict[N, tuple[float, float]]

class GridProfs(Protocol):
    """Protocol for storing grid profiles."""
    
    p: Mapping[L | G, npt.NDArray[np.float64]]
    q: Mapping[L, npt.NDArray[np.float64]]
    v: Mapping[G, npt.NDArray[np.float64]]

# Functions for updating adjacency maps from topology coordinates

LGNMap = TypeVar('LGNMap', dict[L, tuple[N]], dict[G, tuple[N]])

def lgn_update(lgn: LGNMap,
               switches: set[E],
               splits: dict[N, dict[E, N]]) -> LGNMap:
    """Return load-generator-node map with switches and splits."""
    
    return {lg: (splits[ns[0]][lg] if ns[0] in splits else ns[0],)
            for lg, ns in lgn.items() if not lg in switches}

def cn_update(cn: dict[C, tuple[N, N]],
              switches: set[E],
              splits: dict[N, dict[E, N]]) -> dict[C, tuple[N, N]]:
    """Return connection-node map with switches and splits."""
    
    return {c: (splits[ns[0]][c] if ns[0] in splits else ns[0],
                splits[ns[1]][c] if ns[1] in splits else ns[1])
            for c, ns in cn.items() if not c in switches}

# Helper functions

def n_splits(coords: TopoCoords) -> dict[N, dict[E, N]]:
    """Return map of split nodes to maps of elements to sub-nodes."""
    
    return {n: {e: sub_node(n, i)
                for i, es in enumerate(coords.n_coord[n][1])
                for e in es if not e in coords.e_coord}
            for n in coords.n_coord}

def sub_node(node: N, number: int) -> N:
    """Return sub-node from a node and an integer."""
    
    return (node, number)

def sub_node_idx(node: N) -> int:
    """Return index from sub-node"""
    
    return node[1] if isinstance(node, tuple) else 0

def super_node(node: N) -> N:
    """Return super-node from sub-node."""
    
    return node[0] if isinstance(node, tuple) else node
