# coding:utf-8
from typing import Dict, List, Set
from base import _Thrift2Pyi_Base
from enum import Enum


class ExampleEnum(Enum):
    A = 0
    B = 1
    C = 2


class Example(object):
    A: Dict[Dict[_Thrift2Pyi_Base, _Thrift2Pyi_Base], _Thrift2Pyi_Base]
    B: int
    C: int
    D: int
    E: bool
    F: int
    G: float
    H: str
    I: _Thrift2Pyi_Base
    J: Dict[_Thrift2Pyi_Base, Dict[_Thrift2Pyi_Base, _Thrift2Pyi_Base]]
    K: Dict[_Thrift2Pyi_Base, _Thrift2Pyi_Base]
    L: Dict[str, bool]
    M: Dict[str, List[Dict[str, _Thrift2Pyi_Base]]]
    N: List[_Thrift2Pyi_Base]
    O: List[str]
    P: Set[int]
    Q: List[Dict[str, _Thrift2Pyi_Base]]

    def __init__(self,
                 A: Dict[Dict[_Thrift2Pyi_Base, _Thrift2Pyi_Base],
                         _Thrift2Pyi_Base] = None,
                 B: int = 2,
                 C: int = None,
                 D: int = None,
                 E: bool = True,
                 F: int = None,
                 G: float = 0.1,
                 H: str = 'hello',
                 I: _Thrift2Pyi_Base = None,
                 J: Dict[_Thrift2Pyi_Base, Dict[_Thrift2Pyi_Base,
                                                _Thrift2Pyi_Base]] = None,
                 K: Dict[_Thrift2Pyi_Base, _Thrift2Pyi_Base] = None,
                 L: Dict[str, bool] = None,
                 M: Dict[str, List[Dict[str, _Thrift2Pyi_Base]]] = None,
                 N: List[_Thrift2Pyi_Base] = None,
                 O: List[str] = None,
                 P: Set[int] = None,
                 Q: List[Dict[str, _Thrift2Pyi_Base]] = None) -> None:
        ...


_Thrift2Pyi_Example = Example


class ExampleService(object):
    def Get(self, rq: _Thrift2Pyi_Base = None,
            xx: int = None) -> _Thrift2Pyi_Example:
        ...

    def Pull(self, name: str = '', xxx: Dict[str, str] = None) -> int:
        ...

    def Test(self, ) -> None:
        ...
