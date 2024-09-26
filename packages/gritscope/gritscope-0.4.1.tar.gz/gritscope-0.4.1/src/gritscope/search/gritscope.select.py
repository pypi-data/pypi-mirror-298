from __future__ import annotations # Default behavior pending PEP 649

from collections.abc import Collection, Iterable, MutableMapping
from typing import TypeVar, Literal

from itertools import chain

from operator import lt, gt

from shelve import Shelf

import shelve
import dbm.gnu

import numpy as np
import numpy.typing as npt

import xarray as xr

from gritscope.topology.abc import TopoCoords

# Types for topologies, scenarios and metrics

Topo = TypeVar('Topo', bound=TopoCoords, contravariant=True)

TopoName = str
ScenName = str
MetName = str

# Types for result databases

Res = npt.NDArray[np.float_]
ResData = MutableMapping[ScenName, MutableMapping[MetName, Res]]
ResDB = Shelf[ResData]

# Types for result selections

TRes = npt.NDArray[np.str_]
Selection = MutableMapping[MetName, tuple[Res, TRes]]
SelectDB = Shelf[Selection]
SelectK = MutableMapping[MetName, list[tuple[Res, TRes]]]
SelectKDB = Shelf[SelectK]

# Main selection functions

def best(topos: Iterable[TopoName],
         scens: Collection[ScenName],
         mets: Collection[MetName],
         write: SelectDB,
         read: ResDB,
         criterion: Literal['min'] | Literal['max'] = 'min') -> SelectDB:
    
    topos = iter(topos)
    first = next(topos)
    
    for s in scens:
        data: Selection = write.get(s, {})
        for m in mets:
            if not m in data:
                og_vals = read[first][s][m]
                og_topos = np.tile(np.array([first], dtype=object),
                                   og_vals.shape)
                data[m] = (og_vals, og_topos)
        write[s] = data
    
    for t in chain([first], topos):
        for s in scens:
            data = write[s]
            for m in mets:
                og_vals, og_topos = data[m]
                new_vals = read[t][s][m]
                new_topo = np.array([t], dtype=object)
                data[m] = compare(og_vals, og_topos,
                                  new_vals, new_topo,
                                  criterion)
            write[s] = data
    
    return write

def best_k(topos: Iterable[TopoName | TRes],
           scens: Collection[ScenName],
           mets: Collection[MetName],
           write: SelectKDB,
           read: ResDB,
           k: int = 100,
           criterion: Literal['min', 'max'] = 'min') -> SelectKDB:

    cache: dict[ScenName, SelectK] = {}
    for s in scens:
        cache[s] = write.get(s, {})

    for ts in topos:
        for s in scens:
            writeflag = False
            for m in mets:
                data = cache[s].get(m, [])
                if isinstance(ts, TopoName):
                    new_vals = read[ts][s][m]
                    new_topos = np.array([ts], dtype=np.str_)
                else:
                    new_vals = np.zeros(ts.shape[0], dtype=np.float_)
                    new_topos = np.zeros(ts.shape[0], dtype=np.str_)
                    for n, t in enumerate(ts):
                        new_vals[n] = read[t][s][m][n]
                        new_topos[n] = t
                data, changed = insert_k((new_vals, new_topos),
                                          data, k, criterion)
                if changed:
                    cache[s][m] = data
                    writeflag = True
            if writeflag:
                write[s] = cache[s]

    return write

# def best_k(topos: Iterable[TopoName],
#            scens: Collection[ScenName],
#            mets: Collection[MetName],
#            write: SelectKDB,
#            read: ResDB,
#            k: int = 100,
#            criterion: Literal['min', 'max'] = 'min') -> SelectKDB:

#     for t in topos:
#         for s in scens:
#             s_data: SelectK = write.get(s, {})
#             for m in mets:
#                 data = s_data.get(m, [])
#                 new_vals = read[t][s][m]
#                 new_topo = np.array([t], dtype=object)
#                 data = insert_k((new_vals, new_topo), data, k, criterion)
#                 s_data[m] = data
#             write[s] = s_data

#     return write

def insert_k(new: tuple[Res, TRes],
             data: list[tuple[Res, TRes]],
             k: int,
             criterion: Literal['min', 'max']) -> tuple[list[tuple[Res, TRes]],
                                                        bool]:

    negation: Literal['min', 'max']
    match criterion:
        case 'min':
            negation = 'max'
            comp = lt
        case 'max':
            negation = 'min'
            comp = gt

    if len(data) == 0:
        return [new], True

    if np.all(comp(data[-1][0], new[0])):
        if len(data) >= k:
            return data, False
        else:
            return data + [new], True
    else:
        better = compare(*data[-1], *new, criterion)
        if len(data) >= k:
            return insert_k(better, data[:-1], k, criterion)
        else:
            worse = compare(*data[-1], *new, negation)
            return insert_k(better, data[:-1], k, criterion)[0] + [worse], True

# def insert_k(new: tuple[Res, TRes],
#              data: list[tuple[Res, TRes]],
#              k: int,
#              criterion: Literal['min', 'max']) -> list[tuple[Res, TRes]]:

#     negation: Literal['min', 'max']
#     match criterion:
#         case 'min':
#             negation = 'max'
#             comp = lt
#         case 'max':
#             negation = 'min'
#             comp = gt

#     if len(data) == 0:
#         return [new]

#     if np.all(comp(data[-1][0], new[0])):
#         if len(data) >= k:
#             return data
#         else:
#             return data + [new]
#     else:
#         better = compare(*data[-1], *new, criterion)
#         if len(data) >= k:
#             return insert_k(better, data[:-1], k, criterion)
#         else:
#             worse = compare(*data[-1], *new, negation)
#             return insert_k(better, data[:-1], k, criterion) + [worse]

def compare(og_vals: Res,
            og_topos: TRes,
            new_vals: Res,
            new_topos: TRes,
            criterion: Literal['min', 'max']) -> tuple[Res, TRes]:

    match criterion:
        case 'min':
            mask = new_vals < og_vals
        case 'max':
            mask = new_vals > og_vals

    vals = np.where(mask, new_vals, og_vals)
    topos = np.where(mask, new_topos, og_topos)

    return vals, topos

def to_xarray(read: str,
              write: str,
              scenbatch: str,
              chunk: int = 100000,
              topotype: str = 'S1024'):

    with (dbm.gnu.open(read, 'r') as keydb,
          shelve.open(read, 'r') as readdb):

        count = 0
        batch = 0
        firstkey = keydb.firstkey()
        while firstkey is not None:

            print('Processing batch {} of size {}'.format(batch, chunk))

            rdata = readdb[firstkey.decode()][scenbatch]
            num_scens = next(iter(rdata.items()))[1].shape[0]
            num_topos = 1

            key = firstkey
            while (((key := keydb.nextkey(key)) is not None) #type: ignore
                    and num_topos < chunk):
                num_topos += 1

            wdata = {m: xr.DataArray(np.zeros((num_topos, num_scens),
                                     dtype=np.float32),
                                     dims=('toponum', 'scennum'))
                     for m in rdata}
            wdata['topo'] = xr.DataArray(np.zeros((num_topos), dtype=topotype),
                                         dims=('toponum',))

            for m in rdata:
                wdata[m].values[0, :] = rdata[m]

            toponums = np.zeros(num_topos, dtype=np.int32)
            toponums[0] = count

            count += 1
            subcount = 1

            key = firstkey
            while (((key := keydb.nextkey(key)) is not None) #type: ignore
                    and subcount < chunk):

                for m in rdata:
                    wdata[m].values[subcount, :] = rdata[m]
                    toponums[subcount] = count

                count += 1
                subcount += 1

            dataset = xr.Dataset(wdata, coords={'toponum': toponums,
                                                'scennum': range(num_scens)})
            dataset.to_netcdf(write + str(int(batch)) + '.nc')

            firstkey = key
            batch += 1
