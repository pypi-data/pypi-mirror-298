from __future__ import annotations # Default behavior pending PEP 649

from collections.abc import Hashable
from typing import Type, Self, Optional, Any

from dataclasses import dataclass, astuple, asdict

import numpy as np
import numpy.typing as npt

from scipy.sparse import coo_array, csc_array, csr_array, hstack # type: ignore
from scipy.sparse.linalg import splu, SuperLU # type: ignore

from .protocol import GridData
from .flow import (buses, laplacian, slack_array, PFInit, PFState,
                   p_profs, q_profs, mag_profs, ang_profs, slack_profs)

# Types for bus and connection encodings

B = Hashable
C = Hashable

# Fast decoupled power flow initialization and state objects

@dataclass
class FDPFInit(PFInit):
    """Fast decoupled power flow initizalization class."""
    
    bus: dict[B, int]
    pv: npt.NDArray[np.bool_]
    pq: npt.NDArray[np.bool_]
    
    y: coo_array
    s: npt.NDArray[np.float_]
    bp: Optional[SuperLU]
    bpp: Optional[SuperLU]
    dot: csc_array
    
    @classmethod
    def build(cls: Type[Self], grid: GridData) -> Self:
        """Return initialization object from built from grid object."""
        
        bus, pv, pq = buses(grid.topo)
        
        s = slack_array(grid.topo, grid.params, bus)
        y = laplacian(grid.topo, grid.params, bus, True, True)
        
        bp = bp_mat(laplacian(grid.topo, grid.params, bus, True, False), s)
        bpp = bpp_mat(laplacian(grid.topo, grid.params, bus, False, True), pq)
        
        dot = csc_array((np.ones_like(y.row), (np.arange(len(y.row)), y.row)))
        
        return cls(bus, pv, pq, y, s, bp, bpp, dot)

@dataclass
class FDPFState(PFState):
    """Fast decoupled powerflow state class."""
    
    p: npt.NDArray[np.float_]
    q: npt.NDArray[np.float_]
    ang: npt.NDArray[np.float_]
    mag: npt.NDArray[np.float_]
    slack: npt.NDArray[np.float_]
    conv: npt.NDArray[np.bool_]
    
    a_steps: npt.NDArray[np.int_]
    m_steps: npt.NDArray[np.int_]
    idx: npt.NDArray[np.int_]

    @classmethod
    def build(cls: Type[Self],
              grid: GridData,
              init: PFInit,
              batch: npt.NDArray[np.int_]) -> Self:
        """Return state object from built from grid object."""
        
        p = p_profs(grid, init, batch)
        q = q_profs(grid, init, batch)
        
        ang = ang_profs(init, batch)
        mag = mag_profs(grid, init, batch)
        
        slack = slack_profs(batch)
        
        conv = np.zeros(len(batch), np.bool_)
        a_steps = np.zeros(len(batch), np.int16)
        m_steps = np.zeros(len(batch), np.int16)
        idx = np.arange(len(batch), dtype=np.int32)
        
        return cls(p, q, ang, mag, slack, conv, a_steps, m_steps, idx)
    
    def select(self: Self, mask: npt.NDArray[np.bool_]) -> Self:
        """Return state object batch-selected by boolean mask."""
        
        res = [s[mask] for s in astuple(self)]
        
        return type(self)(*res)
    
    def append(self: Self, other: Self) -> Self:
        """Return state object concatenated with other state object."""
        
        res = [np.concatenate([s, o])
               for s, o in zip(astuple(self), astuple(other))]
        
        return type(self)(*res)
    
    def sort(self: Self) -> Self:
        """Return state object sorted on index."""
        
        idx = np.argsort(self.idx)
        res = [s[idx] for s in astuple(self)]
        
        return type(self)(*res)
    
    def update(self: Self, changes: dict[str, npt.NDArray[Any]]) -> Self:
        """Return state object with quantities updated from changes.."""
        
        res = [changes[k] if k in changes
               else v for k, v in asdict(self).items()]
        
        return type(self)(*res)

# Functions for initializing fast decoupled power flow

def bp_mat(y: coo_array, s: npt.NDArray[np.float_]) -> Optional[SuperLU]:
    """Return sparse LU-decomposition of B' matrix."""
    
    bp = hstack([csc_array(np.expand_dims(-s, -1)),
                 csc_array(np.imag(-y))[:, 1:]])
    
    try:
        return splu(bp)
    except RuntimeError:
        return None

def bpp_mat(y: coo_array, pq: npt.NDArray[np.bool_]) -> Optional[SuperLU]:
    """Return sparse LU-decomposition of B'' matrix."""
    
    bpp = csr_array(np.imag(-y))[pq, :].tocsc()[:, pq]
    
    try:
        return splu(bpp)
    except RuntimeError:
        return None

# Functions for computing real and reactive power

def ang_diff(state: FDPFState,
             init: FDPFInit) -> tuple[npt.NDArray[np.float_],
                                      npt.NDArray[np.float_]]:
    """Return voltage angle differences and magnitudes."""
    
    ang = state.ang[:, init.y.row] - state.ang[:, init.y.col]
    mag = state.mag[:, init.y.col]
    
    return ang, mag

def p(state: FDPFState, init: FDPFInit) -> npt.NDArray[np.float_]:
    """Return real power computed with power flow equations."""
    
    # Dimension (batch, y_elements)
    ang, mag = ang_diff(state, init)
    
    # Dimension (batch, y_elements)
    b = np.imag(init.y.data)*np.sin(ang)
    g = np.real(init.y.data)*np.cos(ang)
    
    return state.mag*(mag*(b + g) @ init.dot)

def q(state: FDPFState, init: FDPFInit) -> npt.NDArray[np.float_]:
    """Return reactive power computed with power flow equations."""
    
    # Dimension (batch, y_elements)
    ang, mag = ang_diff(state, init)
    
    # Dimension (batch, y_elements)
    b = -np.imag(init.y.data)*np.cos(ang)
    g = np.real(init.y.data)*np.sin(ang)
    
    return state.mag*(mag*(b + g) @ init.dot)

def pf_eqs(state: FDPFState,
           init: FDPFInit,
           max_error: float) -> tuple[npt.NDArray[np.float_],
                                      npt.NDArray[np.float_],
                                      npt.NDArray[np.float_],
                                      npt.NDArray[np.float_],
                                      npt.NDArray[np.bool_]]:
    """Return real and reactive power, errors, and convergence flags."""
    
    p_calc = p(state, init)
    q_calc = q(state, init)
    
    p_diff = p_calc - init.s*state.slack - state.p
    q_diff = q_calc - state.q
    
    p_conv = np.all(np.abs(p_diff) < max_error, axis=1)
    q_conv = np.all(np.abs(q_diff[..., init.pq]) < max_error, axis=1)
    
    conv = p_conv*q_conv
    
    return p_calc, q_calc, p_diff, q_diff, conv

# Main functions of the fast decoupled power flow algorithm

def ang_step(state: FDPFState, init: FDPFInit, max_error: float) -> FDPFState:
    """Return iteration of voltage angles and slack power."""
    
    _, _, p_diff, _, conv = pf_eqs(state, init, max_error)
    
    state = state.update({'conv': conv})
    
    if np.all(conv) or not init.bp:
        return state
    
    unconv = state.select(~conv)
    p_diff = p_diff[~conv]
    
    step = init.bp.solve(p_diff.T/unconv.mag.T).T
    count = unconv.a_steps + 1
    
    ang_ref = np.zeros_like(step[..., :1])
    ang_step = np.concatenate((ang_ref, step[..., 1:]), axis=-1)
    slack_step = step[..., :1]
    
    ang = state.select(~conv).ang - ang_step
    slack = state.select(~conv).slack - slack_step
    
    update = unconv.update({'ang': ang, 'slack': slack, 'a_steps': count})
    state = state.select(conv).append(update)
    
    return state

def mag_step(state: FDPFState, init: FDPFInit, max_error: float) -> FDPFState:
    """Return iteration of voltage magnitudes and reactive power."""
    
    _, q_calc, _, q_diff, conv = pf_eqs(state, init, max_error)
    
    state = state.update({'conv': conv})
    
    if np.all(conv) or not init.bpp:
        return state
    
    unconv = state.select(~conv)
    q_calc = q_calc[~conv]
    q_diff = q_diff[~conv]
    
    step = init.bpp.solve(q_diff[..., init.pq].T/unconv.mag[..., init.pq].T).T
    count = unconv.m_steps + 1
    
    mag_pq = unconv.mag[..., init.pq]
    q_pq = unconv.q[..., init.pq]
    
    mag = np.concatenate([unconv.mag[..., init.pv], mag_pq - step], axis=-1)
    q = np.concatenate([q_calc[..., init.pv], q_pq], axis=-1)
    
    update = unconv.update({'mag': mag, 'q': q, 'm_steps': count})
    state = state.select(conv).append(update)
    
    return state

def fdpf(state: FDPFState,
         init: FDPFInit,
         max_iter: int = 10,
         max_error: float = 1e-3) -> FDPFState:
    """Return final state after recursivly iterating FDPF algorithm."""
    
    if max_iter < 1 or not init.bp or not init.bpp:
        return state.sort()
    
    for step in (ang_step, mag_step):
        state = step(state, init, max_error)
        if np.all(state.conv):
            return state.sort()
    
    return fdpf(state, init, max_iter - 1, max_error)
