# coding: utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os

from collections import defaultdict

import sys
from pypeg2 import compose
from thriftpy2 import load
from thriftpy2.thrift import TType
from yapf.yapflib.yapf_api import FormatCode

from thrift2pyi.peg import PYI, Struct, Init, Parameter, Annotations, Parameters, Annotation, Structs, \
    Imports, Services, Modules, Import, Service, Methods, Method, Enums, KeyValue, KeyValues, Enum


class Thrift2pyi(object):
    def __init__(self, filename):
        self.thrift = load(filename)
        if not hasattr(self.thrift, "__thrift_meta__"):
            sys.exit(0)
        self.meta = self.thrift.__thrift_meta__

        self.pyi = PYI()
        self.pyi.imports = Imports()
        self.pyi.services = Services()
        self.pyi.structs = Structs()
        self.pyi.enums = Enums()
        self.filename = filename

        self._imports = defaultdict(set)
        self._module2file = {}

    def _get_type(self, args):
        if not isinstance(args, tuple):
            thrift_type = args
            if thrift_type == TType.BOOL:
                return "bool"
            elif thrift_type in [TType.BYTE, TType.I08, TType.I16, TType.I32, TType.I64]:
                return "int"
            elif thrift_type in [TType.STRING, TType.UTF7]:
                return "str"
            elif thrift_type in [TType.DOUBLE]:
                return "float"
            else:
                raise Exception("do not type support %s" % thrift_type)
        else:
            thrift_type, nest = args
            if thrift_type == TType.STRUCT:
                if nest.__module__ in self._module2file:
                    name = nest.__module__
                    self._imports[name].add("_Thrift2Pyi_" + nest.__name__)
                return "_Thrift2Pyi_" + nest.__name__
            elif thrift_type == TType.LIST:
                self._imports["typing"].add("List")
                return "List[%s]" % self._get_type(nest)
            elif thrift_type == TType.MAP:
                self._imports["typing"].add("Dict")
                return "Dict[%s,%s]" % (self._get_type(nest[0]), self._get_type(nest[1]))
            elif thrift_type == TType.SET:
                self._imports["typing"].add("Set")
                return "Set[%s]" % self._get_type(nest)
            elif thrift_type == TType.I32:
                return nest.__name__
            else:
                raise Exception("do not type support %s" % thrift_type)

    def _spec2type(self, spec):
        if len(spec) == 3:
            return self._get_type(spec[0])
        elif len(spec) == 4:
            return self._get_type((spec[0], spec[2]))
        else:
            raise Exception("invalid spec, length is %d" % len(spec))

    def _2v(self, v):
        if v == "":
            return "''"
        elif v is None:
            return "None"
        elif isinstance(v, int) or isinstance(v, float) or isinstance(v, list) or isinstance(v, dict):
            return str(v)
        elif isinstance(v, str):
            return "'%s'" % v
        else:
            raise Exception("%s do not support" % v)

    def _spec2params(self, default_spec, thrift_spec) -> (Parameters, Annotations):
        default_dict = {}
        for k, v in default_spec:
            p_param = Parameter()
            p_param.__name__ = k
            default_dict[k] = self._2v(v)

        p_annotations = Annotations()
        p_params = Parameters()

        for filed_id, spec in thrift_spec.items():
            p_annotation = Annotation()
            p_annotation.name = spec[1]
            p_annotation.type = self._spec2type(spec)

            p_annotations[spec[1]] = p_annotation
            p_param = Parameter()
            p_param.annotation = p_annotation
            p_param.default = default_dict[spec[1]]
            p_params.append(p_param)

        return p_params, p_annotations

    def _struct2pyi(self, struct):
        p_struct = Struct()
        p_struct.name = struct.__name__
        p_init = Init()
        p_init.params, p_struct.annotations = self._spec2params(struct.default_spec, struct.thrift_spec)
        p_struct.init = p_init
        return p_struct

    def _structs2pyi(self):
        for struct in self.meta["structs"]:
            self.pyi.structs.append(self._struct2pyi(struct))

    def _scan_includes(self):
        for include in self.meta["includes"]:
            thrift_file = include.__thrift_file__
            module = thrift_file.split("/")[-1].split(".")[0]
            name = include.__thrift_file__.replace(".thrift", "_thrift")
            name = name.replace("/", ".")
            self._module2file[module] = name

            if not os.path.exists(name):
                Thrift2pyi(include.__thrift_file__).output()

    def _includes2pyi(self):
        p_imports = self.pyi.imports
        for k, v in self._imports.items():
            if k not in p_imports:
                p_imports[k] = Import()
            p_modules = Modules()
            p_modules.extend(v)
            p_imports[k].modules = p_modules

    def _service2pyi(self, service):
        p_service = Service()
        p_service.name = service.__name__
        p_methods = Methods()
        for method in service.thrift_services:
            p_method = Method()
            p_method.name = method
            args = getattr(service, "%s_args" % method)
            p_method.params, _ = self._spec2params(args.default_spec, args.thrift_spec)
            result = getattr(service, "%s_result" % method)
            if 0 not in result.thrift_spec:
                p_method.response = 'None'
            else:
                p_method.response = self._spec2type(result.thrift_spec[0])
            p_methods[method] = p_method
        p_service.methods = p_methods
        return p_service

    def _services2pyi(self):
        for service in self.meta["services"]:
            self.pyi.services.append(self._service2pyi(service))

    def _enum2pyi(self, enum):
        self._imports["enum"].add("Enum")
        p_kvs = KeyValues()

        for k, v in enum._NAMES_TO_VALUES.items():
            p_kv = KeyValue()
            p_kv.name = k
            p_kv.value = self._2v(v)
            p_kvs.append(p_kv)

        p_enum = Enum()
        p_enum.name = enum.__name__
        p_enum.kvs = p_kvs

        return p_enum

    def _enums2pyi(self):
        for enum in self.meta["enums"]:
            self.pyi.enums.append(self._enum2pyi(enum))

    def _thrift2pyi(self):
        self._scan_includes()
        self._structs2pyi()
        self._services2pyi()
        self._enums2pyi()
        self._includes2pyi()

    def output(self):
        self._thrift2pyi()
        o = FormatCode(compose(self.pyi))
        with open("%s.pyi" % self.filename.replace(".thrift", "_thrift"), "w") as f:
            f.write(o[0])


if __name__ == "__main__":
    Thrift2pyi("tests/example.thrift").output()
