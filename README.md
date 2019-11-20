# thrift2pyi
convert thrift to pyi

# How to use
pip install thrift2pyi

thrift2pyi tests/example.thrift

See dir "tests" for details. 

# Example
```thrift
namespace py example

include "a/a.thrift"


const string A = "1";
const i32 B = 1;
const list<i32> C = [];
const list<i32> D = [1,2];
const map<i32,string> E = {};
const double F = 1.1;

struct Example {
    1: map<map<a.A,a.A>, a.A> A
    2: optional i16 B
    3: i32 C
    4: i64 D
    5: bool E = true
    6: byte F
    7: double G = 0.1
    8: string H = "hello"
    9: a.A I
    10: map<a.A, map<a.A,a.A>> J
    11: map<a.A, a.A> K
    12: map<string, bool> L = {}
    13: map<string, list<map<string, a.A>>> M
    14: list<a.A> N
    15: list<string> O
    16: set<i16> P
    17: list<map<string, a.A>> Q
}

enum ExampleEnum {
    A = 0
    B = 1
    C = 2
}


enum ErrCode {
    ERR_SUCCESS = 0
    ERR_REQ_PARAM_INVALID  = 4000
    ERR_UNKNOWN = 5000
    ERR_SYSTEM_INNER_EXCEPTION = 5001
    ERR_LIMIT_EXCEEDED = 5002
}

union ExampleUnion {
    1: i32 A = 1
}

exception ByteException {
    1: i32 ErrorCode = 0,
}

service ExampleService {
    Example Get(1: a.A rq, 2: i64 xx)
    i16 Pull(1: string name = "", 2: map<string,string> xxx) throws (1: ByteException exc)
    void Test()
}

```

generated by thrift2ypi

```python
# coding:utf-8
from typing import List, Dict, Set
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
    def Get(self, rq: _Thrift2Pyi_A = None,
            xx: int = None) -> _Thrift2Pyi_Example:
        ...

    def Pull(self, name: str = '', xxx: Dict[str, str] = None) -> int:
        ...

    def Test(self, ) -> None:
        ...

```