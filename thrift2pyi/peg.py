# coding: utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import re

from pypeg2 import blank, name, attr, Namespace, maybe_some, endl, List, optional, csl

Type = re.compile(r"[\w.\[\]]")
Value = re.compile(r"[\w\-'.\"\{\}]*")

Identifier = re.compile(r"[A-Za-z_][\w._]*")
Package = re.compile(r"[A-Za-z_.][\w._]*")

cls = "# noinspection PyPep8Naming, PyShadowingNames", endl, "class "


class Annotation(object):
    grammar = blank, name(), ":", attr("type", Type)


class Annotations(Namespace):
    grammar = maybe_some(Annotation, endl)


class Parameter(object):
    grammar = attr("annotation", Annotation), "=", attr("default", Value)


class Parameters(List):
    grammar = optional(csl(Parameter))


class Init(object):
    grammar = blank, "def __init__(self, ", attr("params", Parameters), ") -> None:", endl, "  ...", endl


class Struct(object):
    grammar = cls, name(), "(object):", endl, attr("annotations", Annotations), attr("init", Init), endl


class Structs(List):
    grammar = maybe_some(Struct)


class Union(object):
    grammar = cls, name(), "(object):", endl, attr("annotations", Annotations), attr("init", Init), endl


class Unions(List):
    grammar = maybe_some(Union)


class Exc(object):
    grammar = cls, name(), "(TException):", endl, attr("annotations", Annotations), attr("init", Init), endl


class Exceptions(List):
    grammar = maybe_some(Exc)


class Method(object):
    grammar = blank, "def ", name(), "(self, ", attr("params", Parameters), ") ->", attr("response", Type), \
              ":", endl, "  ...", endl


class Methods(Namespace):
    grammar = maybe_some(Method)


class Service(object):
    grammar = cls, name(), "(object):", endl, attr("methods", Methods), endl


class Services(List):
    grammar = maybe_some(Service)


class ModuleAlias(object):
    grammar = optional(blank, 'as', blank, attr("alias", Identifier))


class Module(object):
    grammar = attr("name", Identifier), attr("module_alias", ModuleAlias)


class Modules(List):
    grammar = optional(csl(Module))


class FromImport(object):
    grammar = "from", blank, attr("name", Package), blank, "import", \
              blank, attr("modules", Modules), endl


class Imports(Namespace):
    grammar = maybe_some(FromImport)


class KeyValue(object):
    grammar = blank, name(), "=", attr("value", Value), endl


class KeyValues(List):
    grammar = maybe_some(KeyValue)


class Const(object):
    grammar = name(), "=", attr("value", Value), endl


class Consts(List):
    grammar = maybe_some(Const)


class Enum(object):
    grammar = cls, name(), "(Enum):", endl, attr("kvs", KeyValues)


class Enums(List):
    grammar = maybe_some(Enum)


class PYI(object):
    grammar = "# coding:utf-8", endl, attr("imports", Imports), endl, attr("consts", Consts), \
              attr("enums", Enums), endl, attr("structs", Structs), endl, attr("unions", Unions), endl, attr(
        "exceptions", Exceptions), endl, attr("services", Services)
