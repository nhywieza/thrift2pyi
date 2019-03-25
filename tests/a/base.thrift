namespace py base

struct E {
    1: bool A = false,
    2: string B = "",
}

struct Base {
    1: string A = "",
    2: string B = "",
    3: string C = "",
    4: string D = "",
    5: optional E E,
    6: optional map<string, string> F,
}
