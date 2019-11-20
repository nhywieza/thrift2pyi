# coding:utf-8
from typing import Set, Dict, List
from a import _Thrift2Pyi_A
from enum import Enum


class ExampleEnum(Enum):
    A = 0
    B = 1
    C = 2


class ErrCode(Enum):
    ERR_SUCCESS = 0
    ERR_REQ_PARAM_INVALID = 4000
    ERR_UNKNOWN = 5000
    ERR_SYSTEM_INNER_EXCEPTION = 5001
    ERR_LIMIT_EXCEEDED = 5002


class Example(object):
    A: Dict[Dict[_Thrift2Pyi_A, _Thrift2Pyi_A], _Thrift2Pyi_A]
    B: int
    C: int
    D: int
    E: bool
    F: int
    G: float
    H: str
    I: _Thrift2Pyi_A
    J: Dict[_Thrift2Pyi_A, Dict[_Thrift2Pyi_A, _Thrift2Pyi_A]]
    K: Dict[_Thrift2Pyi_A, _Thrift2Pyi_A]
    L: Dict[str, bool]
    M: Dict[str, List[Dict[str, _Thrift2Pyi_A]]]
    N: List[_Thrift2Pyi_A]
    O: List[str]
    P: Set[int]
    Q: List[Dict[str, _Thrift2Pyi_A]]

    def __init__(
            self,
            A: Dict[Dict[_Thrift2Pyi_A, _Thrift2Pyi_A], _Thrift2Pyi_A] = None,
            B: int = None,
            C: int = None,
            D: int = None,
            E: bool = True,
            F: int = None,
            G: float = 0.1,
            H: str = 'hello',
            I: _Thrift2Pyi_A = None,
            J: Dict[_Thrift2Pyi_A, Dict[_Thrift2Pyi_A, _Thrift2Pyi_A]] = None,
            K: Dict[_Thrift2Pyi_A, _Thrift2Pyi_A] = None) -> None:
        ...


_Thrift2Pyi_Example = Example


class ExampleService(object):
    def Get(self, rq: _Thrift2Pyi_A = None,
            xx: int = None) -> _Thrift2Pyi_Example:
        ...

    def Pull(self, name: str = '', xxx: Dict[str, str] = None) -> int:
        ...

    def Test(self, ) -> None:
        ...
