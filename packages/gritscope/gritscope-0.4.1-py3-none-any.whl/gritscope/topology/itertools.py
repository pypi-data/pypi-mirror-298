from __future__ import annotations # Default behavior pending PEP 649

from collections.abc import Hashable, Set, Generator, Iterable, Iterator
from typing import TypeVar

from itertools import chain, combinations, product

# Functions for lazy combinatorial iteration

H = TypeVar('H', bound=Hashable)
Split = tuple[frozenset[H], ...]

def splits(xss: Set[frozenset[H]],
           min_size: int,
           max_splits: int,
           fix: Set[H] = frozenset()) -> Generator[Split[H], None, None]:
    """Iterate ordered splits of xs into disjoint subsets."""
    
    if (len(flatset(xss) | fix) >= 2 * min_size) and (max_splits > 1):
        
        sizes = range(max(0, min_size - len(fix)),
                      len(flatset(xss)) - min_size + 1)
        ysss = (set(c) for n in sizes
                for c in combinations(xss, n)
                if len(flatset(c) | fix) >= min_size)
        
        ps = (product([flatset(yss) | fix],
                      splits(xss - yss, min_size, max_splits - 1))
              for yss in ysss)
        
        yield from ((split, *subsplits) for p in ps
                    for split, subsplits in p)
        
    else:
        yield tuple([flatset(xss) | fix])

def distribute(yss: Iterable[Set[H]],
               xsss: Iterable[Split[H]]) -> Generator[Split[H], None, None]:
    """Iterate distributions of yss over xss for all xss in xsss."""
    
    yss = iter(yss)
    try:
        ys = next(yss)
        zsss = chain.from_iterable(supplement(xss, ys) for xss in xsss)
        yield from distribute(yss, zsss)
    
    except StopIteration:
        yield from xsss

def attach(ys: Iterable[H],
           xsss: Iterable[Split[H]]) -> Generator[Split[H], None, None]:
    """Iterate xsss with ys attached to the first xs in each xss."""
    
    for xss in xsss:
        match len(xss):
            case 0: yield (frozenset(ys),)
            case 1: yield (xss[0] | frozenset(ys),)
            case _: yield (xss[0] | frozenset(ys), *xss[1:])

def supplement(xss: Split[H],
               ys: Set[H]) -> Generator[Split[H], None, None]:
    """Iterate ways to add ys to one xs in xss."""
    
    return ((*xss[:n], xss[n] | ys, *xss[n + 1:]) for n in range(len(xss)))

# Shorthand function for common pattern

def flatset(xss: Iterable[Iterable[H]]) -> frozenset[H]:
    """Return flattened set from iterable of iterables."""
    
    return frozenset(x for xs in xss for x in xs)
