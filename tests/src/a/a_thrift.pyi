# coding:utf-8
from typing import Dict


# noinspection PyPep8Naming, PyShadowingNames
class E(object):
    A: bool
    B: str

    def __init__(self, A: bool = False, B: str = '') -> None:
        ...


_Thrift2Pyi_E = E


# noinspection PyPep8Naming, PyShadowingNames
class A(object):
    A: str
    B: str
    C: str
    D: str
    E: _Thrift2Pyi_E
    F: Dict[str, str]

    def __init__(self,
                 A: str = '',
                 B: str = '',
                 C: str = '',
                 D: str = '',
                 E: _Thrift2Pyi_E = None,
                 F: Dict[str, str] = None) -> None:
        ...


_Thrift2Pyi_A = A
