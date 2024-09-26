from __future__ import annotations # Default behavior pending PEP 649

from typing import Any

import os
import tomllib
import json

# Types for input data

Row = dict[str, str | float]
Data = list[Row]

def graphplot(nodes: Data,
              edges: Data,
              width: float = 400,
              height: float = 400,
              nsize: float = 150,
              ewidth: float = 4,
              clength: float = 12,
              cwidth: float = 5,
              colrange: tuple[float, float] = (-2, 2)) -> dict[str, Any]:
    """Return specification of Vega graph plot."""
    
    path = os.path.dirname(os.path.abspath(__file__))
    with open(path + '/graphplot.toml', 'rb') as f:
        spec = tomllib.load(f)
    spec['data'][0]['values'] = nodes
    spec['data'][1]['values'] = edges
    spec['width'] = width
    spec['height'] = height
    spec['signals'][0]['value'] = nsize
    spec['signals'][1]['value'] = ewidth
    spec['signals'][2]['value'] = clength
    spec['signals'][3]['value'] = cwidth
    spec['scales'][0]['domain'] = colrange
    
    return spec

def savespec(spec: dict[str, Any], path: str) -> None:
    """Save specification as JSON to path."""
    
    with open(path, 'w') as f:
        json.dump(spec, f)
