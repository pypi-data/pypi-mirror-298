"""
Interfaces between nptyping types and array backends
"""

from numpydantic.interface.dask import DaskInterface
from numpydantic.interface.hdf5 import H5Interface
from numpydantic.interface.interface import (
    Interface,
    InterfaceMark,
    JsonDict,
    MarkedJson,
)
from numpydantic.interface.numpy import NumpyInterface
from numpydantic.interface.video import VideoInterface
from numpydantic.interface.zarr import ZarrInterface

__all__ = [
    "DaskInterface",
    "H5Interface",
    "Interface",
    "InterfaceMark",
    "JsonDict",
    "MarkedJson",
    "NumpyInterface",
    "VideoInterface",
    "ZarrInterface",
]
