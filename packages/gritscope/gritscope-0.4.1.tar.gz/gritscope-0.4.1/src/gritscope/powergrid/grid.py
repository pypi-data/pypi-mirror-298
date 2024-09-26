from __future__ import annotations # Default behavior pending PEP 649

from collections.abc import Hashable, Mapping, Collection, Iterator
from typing import Type, Self, Any, TypeVar, Generic

import os
from dataclasses import dataclass, asdict
from math import sqrt, pi
from cmath import exp, phase

import numpy as np
import numpy.typing as npt

import pandas as pd

import yaml

from .protocol import GridData, GridTopo, GridProfs, GridParams

# Types for connection, load and generator encodings

C = Hashable
L = Hashable
G = Hashable

E = C | L | G
N = Hashable

# Dataclass implementations of power grid objects

@dataclass
class Grid(GridData):
    """Power grid dataclass with topology, parameters, profiles."""
    
    topo: Topo
    params: Params
    profs: Profs
    
    @classmethod
    def load(cls: Type[Self], path: str, form: str = 'parquet') -> Self:
        """Return power grid object loaded from path."""
        
        topo = Topo.load(path + '/topology.yaml')
        params = Params.load(path + '/parameters.yaml')
        profs = Profs.load(path + '/profiles', form)
        
        return cls(topo, params, profs)
    
    def save(self, path: str, form: str = 'parquet') -> None:
        """Save power grid object to path."""
        
        os.mkdir(path)
        os.mkdir(path + '/profiles')
        
        self.topo.save(path + '/topology.yaml')
        self.params.save(path + '/parameters.yaml')
        self.profs.save(path + '/profiles', form)
    
    @classmethod
    def from_pp(cls: Type[Grid], net: Any) -> Grid:
        """Return power grid object from Pandapower network object."""
        
        from .pandapower import gs_grid
        
        return gs_grid(net)
    
    def to_pp(self, timestamp: int = 0) -> Any:
        """Return Pandapower network object from power grid object."""
        
        from .pandapower import pp_net
        
        return pp_net(self, timestamp)

@dataclass
class Topo(GridTopo):
    """Grid topology dataclass with connections, loads, generators."""
    
    cn: dict[C, tuple[N, N]]
    ln: dict[L, tuple[N]]
    gn: dict[G, tuple[N]]
    
    @classmethod
    def load(cls: Type[Self], path: str) -> Self:
        """Return grid topology object loaded from path."""
        
        data: dict[str, dict[E, list[N]]] = load_yaml(path)
        
        cn = {c: (ns[0], ns[1]) for c, ns in data['connections'].items()}
        ln = {l: (ns[0],) for l, ns in data['loads'].items()}
        gn = {g: (ns[0],) for g, ns in data['generators'].items()}
        
        return cls(cn, ln, gn)
    
    def save(self, path: str) -> None:
        """Save grid topology object to path."""
        
        data = {'connections': list_amap(self.cn),
                'loads': list_amap(self.ln),
                'generators': list_amap(self.gn)}
        
        save_yaml(data, path)

@dataclass
class Params(GridParams):
    """Grid parameter dataclass with y, s, v, l, pb."""
    
    y: dict[C, complex]
    yg: dict[C, complex]
    n: dict[C, complex]
    s: dict[G, float]
    v: dict[N | L | G | C, float]
    l: dict[C, float]
    pb: float
    co: dict[N, tuple[float, float]]
    
    @classmethod
    def load(cls: Type[Self], path: str, pb: float = 1000000.) -> Self:
        """Return grid paramater object loaded from path."""
        
        data: dict[str, dict[E, float]] = load_yaml(path)
        
        x = data['x_ohm']
        r = data['r_ohm']
        b = data['b_siemens']
        g = data['g_siemens']
        
        w = data['w_ratio']
        p = data['ps_degrees']
        
        s = data['s_weight']
        v = {e: 1000./sqrt(3)*q for e, q in data['v_kv'].items()}
        l = {e: 1000.*q for e, q in data['l_ka'].items()}
        co = {n: (data['long'][n], data['lat'][n]) for n in data['long']}
        
        cz: dict[C, complex] = {}
        for c in x:
            cz[c] = x[c]*1j
        for c in r:
            cz[c] = cz.get(c, 0j) + r[c]
        
        y = {c: (1./z) for c, z in cz.items()}
        
        yg: dict[C, complex] = {}
        for c in b:
            yg[c] = b[c]*1j
        for c in g:
            yg[c] = yg.get(c, 0j) + g[c]
        
        n: dict[C, complex] = {}
        for c in w:
            n[c] = w[c]
        for c in p:
            n[c] = n.get(c, 1 + 0j)*exp(p[c]*2.*pi*1j/360.)
        
        return cls(y, yg, n, s, v, l, pb, co)
    
    def save(self, path: str) -> None:
        """Save grid parameter object to path."""
        
        data = {'x_ohm': {c: (1./y).imag for c, y in self.y.items()},
                'r_ohm': {c: (1./y).real for c, y in self.y.items()},
                'b_siemens': {c: yg.imag for c, yg in self.yg.items()},
                'g_siemens': {c: yg.real for c, yg in self.yg.items()},
                'w_ratio': {c: abs(n) for c, n in self.n.items()},
                'ps_degrees': {c: phase(n)*360./(2.*pi) for c, n in self.n.items()},
                's_weight': self.s,
                'v_kv': {e: sqrt(3)/1000.*q for e, q in self.v.items()},
                'l_ka': {e: q/1000. for e, q in self.l.items()},
                'long': {n: x for n, (x, y) in self.co.items()},
                'lat': {n: y for n, (x, y) in self.co.items()}}
        
        save_yaml(data, path)

@dataclass
class Profs(GridProfs):
    """Grid profile dataclass with p, q, v."""
    
    p: ProfileFrame[L | G]
    q: ProfileFrame[L]
    v: ProfileFrame[L]
    
    @classmethod
    def load(cls: Type[Self], path: str, form: str = 'parquet') -> Self:
        """Return grid profile object loaded from path."""
        
        match form:
            case 'parquet':
                loader = load_parquet
            case 'csv':
                loader = load_csv
            case _:
                raise ValueError(f'unsupported file format: {form}')
        
        p = loader(path + '/p_mw.' + form).scale(1000000./3.)
        q = loader(path + '/q_mvar.' + form).scale(1000000./3.)
        v = loader(path + '/vm_kv.' + form).scale(1000./sqrt(3))
        
        return cls(p, q, v)
    
    def save(self, path: str, form: str = 'parquet') -> None:
        """Save grid profile object to path."""
        
        match form:
            case 'parquet':
                saver = save_parquet
            case 'csv':
                saver = save_csv
            case _:
                raise ValueError(f'unsupported file format: {form}')
        
        saver(self.p.scale(3./1000000.), path + '/p_mw.' + form)
        saver(self.q.scale(3./1000000.), path + '/q_mvar.' + form)
        saver(self.v.scale(sqrt(3)/1000.), path + '/vm_kv.' + form)

# Pandas DataFrame wrapper for protocol compatibility

LGN = TypeVar('LGN', L, G, N)

class ProfileFrame(Generic[LGN], Mapping[LGN, npt.NDArray[np.float64]]):
    """Protocol-compliant wrapper for DataFrames of grid profiles."""
    
    def __init__(self, frame: pd.DataFrame):
        
        self.f = frame.astype(np.float64)
    
    def __getitem__(self, key: E) -> npt.NDArray[np.float64]:
        
        return np.asarray(self.f[key], dtype=np.float64) # type: ignore
    
    def __iter__(self) -> Iterator[LGN]:
        
        return iter(self.f.columns)
    
    def __len__(self) -> int:
        
        return len(self.f.columns)
    
    def scale(self, factor: float) -> ProfileFrame:
        """Return ProfileFrame scaled by factor."""
        
        return ProfileFrame(factor*self.f)

# Save and load functions

def save_yaml(data: dict[str, Any], path: str) -> None:
    """Save dictionary to path in YAML format."""
    
    assert_file_not_existing(path) # FileExistsError if failed
    
    with open(path, 'w') as f:
        yaml.dump(data, f)

def load_yaml(path: str) -> dict[Any, Any]:
    """Return dictionary loaded from YAML file on path."""
    
    with open(path) as f:
        data = yaml.safe_load(f)
    
    return data

def save_parquet(data: ProfileFrame[L | G], path: str) -> None:
    """Save ProfileFrame to path in Parquet format."""
    
    assert_file_not_existing(path) # FileExistsError if failed
    data.f.to_parquet(path)

def load_parquet(path: str) -> ProfileFrame[L | G]:
    """Return ProfileFrame loaded from Parquet file on path."""
    
    return ProfileFrame(pd.read_parquet(path))

def save_csv(data: ProfileFrame[L | G], path: str) -> None:
    """Save ProfileFrame to path in CSV format."""
    
    assert_file_not_existing(path) # FileExistsError if failed
    data.f.to_csv(path)

def load_csv(path: str) -> ProfileFrame[L | G]:
    """Return ProfileFrame loaded from CSV file on path."""
    
    return ProfileFrame(pd.read_csv(path, index_col=0))

# Helper functions

def assert_file_not_existing(path: str) -> None:
    """Raise FileExistsError file already exists on path."""
    
    if os.path.isfile(path):
        raise FileExistsError(f'file "{path}" already exists')

def list_amap(amap: Mapping[E, Collection[N]]) -> dict[E, list[N]]:
    """Return adjacency map from edges to lists of nodes."""
    
    return {e: list(ns) for e, ns in amap.items()}
