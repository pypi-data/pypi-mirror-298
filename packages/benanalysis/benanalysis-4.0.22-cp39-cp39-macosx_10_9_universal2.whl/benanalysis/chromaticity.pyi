from __future__ import annotations
import benanalysis._benpy_core
import typing
__all__ = ['CIE_1931_chromaticity', 'CIExy']
class CIExy:
    """
    CIE 1931 (x,y) chromaticity coordinates
    """
    x: float
    y: float
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    @typing.overload
    def __init__(self) -> None:
        ...
    @typing.overload
    def __init__(self, x: float, y: float) -> None:
        ...
    def __repr__(self) -> str:
        ...
    def __str__(self) -> str:
        ...
def CIE_1931_chromaticity(scan: benanalysis._benpy_core.Scan) -> CIExy:
    """
        Return the CIE 1931 chromaticity (x, y) coordinates for a given scan
    """
