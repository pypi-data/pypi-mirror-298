"""
pybind ngstd
"""
from __future__ import annotations
import pyngcore.pyngcore
import typing
__all__ = ['Archive', 'DummyArgument', 'HeapReset', 'IntRange', 'LocalHeap', 'TestFlagsConversion']
class Archive:
    def __and__(self, array: pyngcore.pyngcore.Array_I_S) -> Archive:
        ...
    def __init__(self, filename: str, write: bool, binary: bool) -> None:
        ...
class DummyArgument:
    def __bool__(self) -> bool:
        ...
    def __repr__(self) -> str:
        ...
class HeapReset:
    """
    stores heap-pointer on init, and resets it on exit
    """
    def __init__(self, lh: LocalHeap) -> None:
        ...
class IntRange:
    def __contains__(self, arg0: int) -> bool:
        ...
    def __init__(self, arg0: int, arg1: int) -> None:
        ...
    def __iter__(self) -> typing.Iterator[int]:
        ...
    def __str__(self) -> str:
        ...
    @property
    def start(self) -> int:
        ...
    @property
    def step(self) -> int:
        ...
    @property
    def stop(self) -> int:
        ...
class LocalHeap:
    """
    A heap for fast memory allocation
    """
    def __init__(self, size: int = 1000000, name: str = 'PyLocalHeap') -> None:
        ...
class _MemoryView:
    def __getstate__(self) -> tuple:
        ...
    def __setstate__(self, arg0: tuple) -> None:
        ...
def TestFlagsConversion(flags: pyngcore.pyngcore.Flags) -> None:
    ...
def _PickleMemory(pickler: typing.Any, view: ...) -> None:
    ...
def _UnpickleMemory(unpickler: typing.Any) -> None:
    ...
