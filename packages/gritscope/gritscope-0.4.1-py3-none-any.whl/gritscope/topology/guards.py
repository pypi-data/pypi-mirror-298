from __future__ import annotations # Default behavior pending PEP 649

from collections.abc import Hashable, Iterable, Callable, Mapping, Collection

from itertools import combinations

from pygrates.graphs import inverse, compound, degrees, subsources

import networkx as nx # type: ignore

from .coords import TopoTuple
from .graphs import (node_degrees, edge_degree_filter,
                     sub_connections, number_of_links,
                     assert_minimum_degree, satisfies_minimum_degree,
                     assert_k_edge_connected, nx_graph)

# Types for edge and node encodings

E = Hashable
N = Hashable

# Main guard classes

class GuardWrapper:
    """Container for composing multiple guard functions."""
    
    def __init__(self, guards: Iterable[Callable[[TopoTuple], bool]]) -> None:
        
        self.guards = guards
        
    def __call__(self, coords: TopoTuple) -> bool:
        
        return all(guard(coords) for guard in self.guards)

class DegreeGuard:
    """Guard that checks minimum degree of the graph."""
    
    def __init__(self, ens: Mapping[E, Collection[N]], min_deg: int = 2):
        
        self.nds = node_degrees(ens, min_deg)
        self.cns = edge_degree_filter(ens, (2,))
        self.d = min_deg
        
        assert_minimum_degree(self.nds, min_deg) # ValueError if failed
    
    def __call__(self, coords: TopoTuple) -> bool:
        """Return True unless topology is below minimum degree."""
        
        return satisfies_minimum_degree(coords, self.cns, self.nds, self.d)
    
class KEdgeGuard:
    """Guard that checks k-edge-connectedness of the graph."""
    
    def __init__(self, ens: Mapping[E, Collection[N]], k: int = 2):
        
        self.cns = edge_degree_filter(ens, (2,))
        self.ncs = inverse(self.cns)
        self.graph = nx_graph(self.cns, store_edge_data=False)
        self.k = k
        
        assert_k_edge_connected(self.cns, self.k) # ValueError if failed
    
    def __call__(self, coords: TopoTuple) -> bool:
        """Return True if topology is k-edge connected."""
        
        g = nx.Graph(self.graph)
        nls = number_of_links(self.cns, self.ncs)
        
        for switch in [e for e in coords.e_coord if e in self.cns]:
            f, t = self.cns[switch]
            if nls[f][t] == 1:
                g.remove_edge(f, t)
            if not nx.edge_connectivity(g, f, t, cutoff=self.k) >= self.k:
                return False
            nls[f][t] -= 1
            nls[t][f] -= 1
        
        for split in [n for n in coords.n_coord.values() if n[0] in self.ncs]:
            g.remove_node(split[0])
            neighbors = [[self.cns[e] for e in es
                          if e in self.cns and e not in coords.e_coord]
                         for es in split[1]]
            for i, nbs in enumerate(neighbors):
                for nb in [n for ns in nbs for n in ns if not n == split[0]]:
                    g.add_edge((split[0], i), nb)
            for pair in combinations(range(len(neighbors)), 2):
                f, t = (split[0], pair[0]), (split[0], pair[1])
                if not nx.edge_connectivity(g, f, t, cutoff=self.k) >= self.k:
                    return False
        
        return True
