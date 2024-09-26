from __future__ import annotations # Default behavior pending PEP 649

from typing import Hashable, Any

from itertools import chain

import json

import numpy as np

from pygrates.itertools import unique

from stylet.specific import T1, T2, T3

from gritscope.topology.abc import TopoCoords
from gritscope.plot.vegaplot import graphplot

from .protocol import GridData, n_splits, sub_node, sub_node_idx, super_node
from .metrics import ES

# Types for edge and node encodings

E = Hashable
N = Hashable

# Type for output data

Row = dict[str, str | float]
Data = list[Row]

# Topology plotting function

def topoplot(grid: GridData,
             topo: TopoCoords,
             loadings: T1[np.float_, ES],
             width: float = 400,
             height: float = 400,
             nsize: float = 150,
             ewidth: float = 4,
             clength: float = 12,
             cwidth: float = 5,
             colrange: tuple[float, float] = (-2, 2)) -> dict[str, Any]:
    """Return JSON string of Vega topology plot."""
    
    nodes, edges = topoplot_data(grid, topo, loadings)
    plot = graphplot(nodes, edges,
                     width, height,
                     nsize, ewidth,
                     clength, cwidth,
                     colrange)
    
    return plot

# Preprocessing functions

def topoplot_data(grid: GridData,
                  topo: TopoCoords,
                  loadings: T1[np.float_, ES]) -> tuple[Data, Data]:
    """Return grid topology data formatted for topology plot."""
    
    cn = node_connections(grid.topo.cn, topo)
    
    row: Row
    
    nodes: list[dict[str, str | float]] = []
    for n, (x, y) in grid.params.co.items():
        split = 1. if n in topo.n_coord else 0.
        row = {'name': str(n),
               'long': x,
               'lat': y,
               'split': split}
        nodes.append(row)
    
    edges: list[dict[str, str | float]] = []
    for c, (f, t) in cn.items():
        switch = 1. if c in topo.e_coord else 0.
        row = {'name': str(c),
               'sourcenode': str(super_node(f)),
               'sinknode': str(super_node(t)),
               'subsource': float(sub_node_idx(f)),
               'subsink': float(sub_node_idx(t)),
               'switch': switch,
               'loading': float(loadings.s(ES, c).values)}
        edges.append(row)
    
    return nodes, edges

def node_connections(cn: dict[E, tuple[N, N]],
                     topo: TopoCoords) -> dict[E, tuple[N, N]]:
    """Return edge-node map of edges to subnodes."""
    
    splits = n_splits(topo)
    sub = lambda n, c: splits[n][c] if n in splits else n
    
    return {c: (sub(f, c), sub(t, c)) for c, (f, t) in cn.items()}
