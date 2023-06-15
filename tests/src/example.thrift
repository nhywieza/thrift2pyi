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
    18: bytes R = ""
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
