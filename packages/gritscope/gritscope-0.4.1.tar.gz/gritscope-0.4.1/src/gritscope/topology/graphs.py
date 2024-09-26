from __future__ import annotations # Default behavior pending PEP 649

from collections.abc import Hashable, Mapping, Collection
from typing import Optional

from pygrates.graphs import inverse, compound, degrees, subsources, subsinks

import networkx as nx # type: ignore

from .coords import ECoord, NCoord, TopoTuple

# Types for edge and node encodings

E = Hashable
N = Hashable

# General graph utility functions

def node_degrees(ens: Mapping[E, Collection[N]],
                 min_deg: int = 2) -> Mapping[N, int]:
    """Return mapping containing degrees of passed nodes."""
    
    nes = inverse(ens)
    return degrees(compound(nes, ens))

def edge_degree_filter(ens: Mapping[E, Collection[N]],
                       degs: tuple[int, ...] = (2,)) -> Mapping[E, Collection[N]]:
    """Return edge-node adjacency map filtered by edge degree."""
    
    eds = degrees(ens)
    return subsources(ens, lambda e: eds[e] in degs)

def node_degree_filter(ens: Mapping[E, Collection[N]],
                       degs: tuple[int, ...]) -> Mapping[E, Collection[N]]:
    """Return edge-node adjacency map filtered by node degree."""
    
    nds = node_degrees(ens)
    return subsinks(ens, lambda n: nds[n] in degs)

def prune(ens: Mapping[E, Collection[N]],
          n_degs: tuple[int, ...],
          e_degs: tuple[int, ...] = (2,)) -> Mapping[E, Collection[N]]:
    """Return edge-node adjacency map recursively pruned."""
    
    step = edge_degree_filter(node_degree_filter(ens, n_degs), e_degs)
    if any(d not in n_degs for d in node_degrees(step).values()):
        return prune(step, n_degs, e_degs)
    else:
        return step

def group_duplicates(ens: Mapping[E, Collection[N]],
                     ordered: bool = False) -> dict[frozenset[E], set[N]]:
    """Return grouped-edge-node adjacency for duplicate edges."""
    
    nes: dict[frozenset[N] | tuple[N, ...], set[E]] = {}
    
    for f, ts in ens.items():
        ns: frozenset[N] | tuple[N, ...]
        ns = frozenset(ts) if not ordered else tuple(ts)
        nes.setdefault(ns, set()).add(f)
    
    return {frozenset(es): set(ns) for ns, es in nes.items()}

def sub_connections(n: N,
                    coords: TopoTuple,
                    cns: Mapping[E, Collection[N]]) -> list[set[E]]:
    """Return list of edge sets resulting from a node split."""
    
    f = lambda e: (e in cns) and (e not in coords.e_coord)
    return [set(filter(f, es)) for es in coords.n_coord[n][1]]

def number_of_links(ens: Mapping[E, Collection[N]],
                    nes: Mapping[N, Collection[E]]) -> dict[N, dict[N, int]]:
    """Return dict of nodes to neighbors with number of links."""
    
    nns = compound(nes, ens)
    return {f: {t: sum(f in ens[e] for e in nes[t]) for t in ts}
            for f, ts in nns.items()}

# Minimum degree checking functions

def assert_minimum_degree(nds: Mapping[N, int],
                          min_deg: int = 2) -> None:
    """Raise ValueError if smallest degree is below minimum."""
    
    below_min = tuple(n for n in nds if nds[n] < min_deg)
    if len(below_min) > 0:
        raise ValueError(f'minimum degree not satisfied at {below_min}')

def satisfies_minimum_degree(coords: TopoTuple,
                             cns: Mapping[E, Collection[N]],
                             nds: Mapping[N, int],
                             min_deg: int = 2) -> bool:
    """Return True unless topology is below minimum degree."""
    
    nds = dict(nds)
        
    for e in coords.e_coord:
        ds = [(n, nds[n] - 1) for n in cns[e]]
        if any(d < min_deg for _, d in ds):
            return False
        nds.update(ds)
    
    for n in coords.n_coord:
        ess = sub_connections(n, coords, cns)
        if any(len(es) < min_deg for es in ess):
            return False
    
    return True

# K-edge-connectedness functions implemented with NetworkX

def assert_k_edge_connected(cns: Mapping[E, Collection[N]],
                            k: int = 2) -> None:
    """Raise ValueError if graph is not k-edge connected."""
    
    g = nx_graph(cns, store_edge_data=False)
    if not nx.edge_connectivity(g, cutoff=k) >= k:
        raise ValueError(f'not {k}-edge connected')

def is_k_edge_connected(coords: TopoTuple,
                        cns: Mapping[E, Collection[N]],
                        k: int = 2) -> bool:
    """Return True if topology is k-edge connected."""
    
    g = nx_graph(cns, coords, store_edge_data=False)
    
    return nx.edge_connectivity(g, cutoff=k) >= k

def nx_graph(cns: Mapping[E, Collection[N]],
             coords: Optional[TopoTuple] = None,
             store_edge_data: bool = True) -> nx.Graph:
    """Return NetworkX graph from passed adjacency map."""
    
    if coords is None:
        e_coord, n_coord = ECoord(), NCoord()
    else:
        e_coord, n_coord = coords.e_coord, coords.n_coord
    
    ens_sub: dict[E, list[tuple[N, int]]] = {}
    
    graph = nx.Graph()
    
    ncs = inverse(cns)
    
    for n in ncs:
        if n not in n_coord:
            graph.add_node(n)
        else:
            subs = (((n, i), es) for i, es in enumerate(n_coord[n][1]))
            for sn, es in subs:
                graph.add_node(sn)
                for e in es:
                    ens_sub.setdefault(e, []).append(sn)
    
    for c in cns:
        if c not in e_coord:
            t, f = cns[c]
            match (t in n_coord, f in n_coord):
                case (False, False):
                    st, sf = t, f
                case (False, True):
                    st, sf = t, ens_sub[c][0]
                case (True, False):
                    st, sf = ens_sub[c][0], f
                case (True, True):
                    st, sf = ens_sub[c][0], ens_sub[c][1]
            
            if store_edge_data:
                graph.add_edge(st, sf, c=c)
            else:
                graph.add_edge(st, sf)
    
    return graph
