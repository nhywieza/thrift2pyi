# coding: utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re

from pypeg2 import blank, name, attr, Namespace, maybe_some, endl, List, optional, csl

Type = re.compile(r"[\w.\[\]]")
Value = re.compile(r"[\w\-'.\"]")


class Annotation:
    grammar = blank, name(), ":", attr("type", Type)


class Annotations(Namespace):
    grammar = maybe_some(Annotation, endl)


class Parameter:
    grammar = attr("annotation", Annotation), "=", attr("default", Value)


class Parameters(List):
    grammar = optional(csl(Parameter))


class Init:
    grammar = blank, "def __init__(self, ", attr("params", Parameters), ") -> None:", endl, "  ...", endl


class Struct:
    grammar = "class ", name(), "(object):", endl, attr("annotations", Annotations), attr("init", Init), endl, \
              "_Thrift2Pyi_", name(), "=", name(), endl


class Structs(List):
    grammar = maybe_some(Struct)


class Method:
    grammar = blank, "def ", name(), "(self, ", attr("params", Parameters), ") ->", attr("response", Type), \
              ":", endl, "  ...", endl


class Methods(Namespace):
    grammar = maybe_some(Method)


class Service:
    grammar = "class ", name(), "(object):", endl, attr("methods", Methods), endl


class Services(List):
    grammar = maybe_some(Service)


class Modules(List):
    grammar = optional(csl(re.compile(r"[\w_*]+")))


class Import:
    grammar = "from", blank, attr("name", re.compile(r"[\w.]*")), blank, "import", \
              blank, attr("modules", Modules), endl


class Imports(Namespace):
    grammar = maybe_some(Import)


class KeyValue:
    grammar = blank, name(), "=", attr("value", Value), endl


class KeyValues(List):
    grammar = maybe_some(KeyValue)


class Enum:
    grammar = "class ", name(), "(Enum):", endl, attr("kvs", KeyValues)


class Enums(List):
    grammar = maybe_some(Enum)


class PYI:
    grammar = "# coding:utf-8", endl, attr("imports", Imports), endl, attr("enums", Enums), endl, \
              attr("structs", Structs), endl, attr("services", Services)
