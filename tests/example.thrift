namespace py example

include "a/base.thrift"

struct Example {
    1: map<map<base.Base,base.Base>, base.Base> A
    2: i16 B = 2
    3: i32 C
    4: i64 D
    5: bool E = true
    6: byte F
    7: double G = 0.1
    8: string H = "hello"
    9: base.Base I
    10: map<base.Base, map<base.Base,base.Base>> J
    11: map<base.Base, base.Base> K
    12: map<string, bool> L
    13: map<string, list<map<string, base.Base>>> M
    14: list<base.Base> N
    15: list<string> O
    16: set<i16> P
    17: list<map<string, base.Base>> Q
}

enum ExampleEnum {
    A = 0
    B = 1
    C = 2
}

exception ByteException {
    1: i32 ErrorCode = 0,
}

service ExampleService {
    Example Get(1: base.Base rq, 2: i64 xx)
    i16 Pull(1: string name = "", 2: map<string,string> xxx) throws (1: ByteException exc)
    void Test()
}

