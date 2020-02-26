# coding:utf-8
from typing import Dict, Set, List
from .a.a_thrift import _Thrift2Pyi_A
from thriftpy2.thrift import TException
from enum import Enum

A = '1'
B = 1
C = []
D = [1, 2]
E = {}
F = 1.1


# noinspection PyPep8Naming, PyShadowingNames
class ExampleEnum(Enum):
    A = 0
    B = 1
    C = 2


# noinspection PyPep8Naming, PyShadowingNames
class ErrCode(Enum):
    ERR_SUCCESS = 0
    ERR_REQ_PARAM_INVALID = 4000
    ERR_UNKNOWN = 5000
    ERR_SYSTEM_INNER_EXCEPTION = 5001
    ERR_LIMIT_EXCEEDED = 5002


# noinspection PyPep8Naming, PyShadowingNames
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

    def __init__(self,
                 A: Dict[Dict[_Thrift2Pyi_A, _Thrift2Pyi_A],
                         _Thrift2Pyi_A] = None,
                 B: int = None,
                 C: int = None,
                 D: int = None,
                 E: bool = True,
                 F: int = None,
                 G: float = 0.1,
                 H: str = 'hello',
                 I: _Thrift2Pyi_A = None,
                 J: Dict[_Thrift2Pyi_A, Dict[_Thrift2Pyi_A,
                                             _Thrift2Pyi_A]] = None,
                 K: Dict[_Thrift2Pyi_A, _Thrift2Pyi_A] = None,
                 L: Dict[str, bool] = {},
                 M: Dict[str, List[Dict[str, _Thrift2Pyi_A]]] = None,
                 N: List[_Thrift2Pyi_A] = None,
                 O: List[str] = None,
                 P: Set[int] = None,
                 Q: List[Dict[str, _Thrift2Pyi_A]] = None) -> None:
        ...


_Thrift2Pyi_Example = Example


# noinspection PyPep8Naming, PyShadowingNames
class ByteException(TException):
    ErrorCode: int

    def __init__(self, ErrorCode: int = 0) -> None:
        ...


_Thrift2Pyi_ByteException = ByteException


# noinspection PyPep8Naming, PyShadowingNames
class ExampleService(object):
    def Get(self,
            rq: _Thrift2Pyi_A = None,
            xx: int = None) -> _Thrift2Pyi_Example:
        ...

    def Pull(self, name: str = '', xxx: Dict[str, str] = None) -> int:
        ...

    def Test(self, ) -> None:
        ...
