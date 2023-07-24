# coding: utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import shutil

from collections import defaultdict

import sys

from six import u, string_types, PY2
from pypeg2 import compose
from thriftpy2 import load
from thriftpy2.thrift import TType
from yapf.yapflib.yapf_api import FormatCode

from thrift2pyi.exceptions import Thrift2pyiException
from thrift2pyi.peg import PYI, Struct, Init, Parameter, Annotations, Parameters, Annotation, Structs, \
    Imports, Services, Modules, Service, Methods, Method, Enums, KeyValue, KeyValues, Enum, Exceptions, Exc, \
    Unions, Union, Consts, Const, FromImport, Module, ModuleAlias


class Thrift2pyi(object):
    def __init__(self, filename, prefix, out):
        if PY2:
            self.thrift = load(filename.encode("utf-8"))
        else:
            self.thrift = load(filename)
        if not hasattr(self.thrift, "__thrift_meta__"):
            sys.exit(0)
        self.meta = self.thrift.__thrift_meta__

        self.pyi = PYI()
        self.pyi.imports = Imports()
        self.pyi.services = Services()
        self.pyi.structs = Structs()
        self.pyi.unions = Unions()
        self.pyi.enums = Enums()
        self.pyi.exceptions = Exceptions()
        self.pyi.consts = Consts()
        self.filename = filename
        self.prefix = prefix
        self.out = out

        self._imports = defaultdict(set)
        self._module2package = {}

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
            elif thrift_type in [TType.BINARY]:
                return "bytes"
            else:
                raise Thrift2pyiException("do not type support %s" % thrift_type)
        else:
            thrift_type, nest = args
            if thrift_type == TType.STRUCT:
                # (12, 'I', <class 'base.Base'>, False)
                if nest.__module__ == self.thrift.__name__:
                    return nest.__name__
                else:
                    module = nest.__module__
                    self._imports[self._module2package[module]].add(("%s_thrift" % module, module))
                    return "%s.%s" % (module, nest.__name__)
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
                return u(nest.__name__)
            else:
                raise Thrift2pyiException("do not type support %s" % thrift_type)

    def _spec2type(self, spec):
        if len(spec) == 3:
            return self._get_type(spec[0])
        elif len(spec) == 4:
            return self._get_type((spec[0], spec[2]))
        else:
            raise Thrift2pyiException("invalid spec, length is %d" % len(spec))

    def _2v(self, v):
        if v == "":
            return "''"
        elif v is None:
            return "None"
        elif isinstance(v, int) or isinstance(v, float) or isinstance(v, list) or isinstance(v, dict):
            return str(v)
        elif isinstance(v, string_types):
            return "'%s'" % v
        else:
            raise Thrift2pyiException("%s do not support" % v)

    def _spec2params(self, default_spec, thrift_spec):
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
        p_struct.name = u(struct.__name__)
        p_init = Init()
        p_init.params, p_struct.annotations = self._spec2params(struct.default_spec, struct.thrift_spec)
        p_struct.init = p_init
        return p_struct

    def _structs2pyi(self):
        for struct in self.meta["structs"]:
            self.pyi.structs.append(self._struct2pyi(struct))

    def _union2pyi(self, union):
        p_union = Union()
        p_union.name = u(union.__name__)
        p_init = Init()
        p_init.params, p_union.annotations = self._spec2params(union.default_spec, union.thrift_spec)
        p_union.init = p_init
        return p_union

    def _unions2pyi(self):
        for union in self.meta["unions"]:
            self.pyi.unions.append(self._union2pyi(union))

    def _scan_includes(self):
        for include in self.meta["includes"]:
            thrift_file = include.__thrift_file__
            module = thrift_file.split(os.sep)[-1].split(".")[0]
            rel_path = os.path.relpath(include.__thrift_file__, os.path.dirname(self.thrift.__thrift_file__))
            rel_dir = os.path.dirname(rel_path)
            self._module2package[module] = "." + rel_dir.replace(".." + os.sep, "..").replace("." + os.sep, ".")

            if not os.path.exists(rel_path):
                Thrift2pyi(include.__thrift_file__, self.prefix, self.out).output()

    def _includes2pyi(self):
        p_imports = self.pyi.imports
        for k, v in self._imports.items():
            if k not in p_imports:
                p_imports[k] = FromImport()
            p_modules = Modules()
            for v_ in v:
                m = Module()
                name, alias = (v_, '') if isinstance(v_, str) else (v_[0], v_[1])
                m.name = name
                a = ModuleAlias()
                a.alias = alias
                m.module_alias = a
                p_modules.append(m)
            p_imports[k].modules = p_modules

    def _service2pyi(self, service):
        p_service = Service()
        p_service.name = u(service.__name__)
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
            p_kv.name = u(k)
            p_kv.value = self._2v(v)
            p_kvs.append(p_kv)

        p_enum = Enum()
        p_enum.name = u(enum.__name__)
        p_enum.kvs = p_kvs

        return p_enum

    def _enums2pyi(self):
        for enum in self.meta["enums"]:
            self.pyi.enums.append(self._enum2pyi(enum))

    def _exc2pyi(self, exc):
        p_exc = Exc()
        p_exc.name = u(exc.__name__)
        p_init = Init()
        p_init.params, p_exc.annotations = self._spec2params(exc.default_spec, exc.thrift_spec)
        p_exc.init = p_init
        return p_exc

    def _excs2pyi(self):
        if not self.meta["exceptions"]:
            return

        self._imports["thriftpy2.thrift"].add("TException")
        for exc in self.meta["exceptions"]:
            self.pyi.exceptions.append(self._exc2pyi(exc))

    def _consts2pyi(self):
        for k, v in self.thrift.__dict__.items():
            # 私有成员跳过
            if k.startswith("__"):
                continue
            kv = Const()
            kv.name = u(k)
            try:
                kv.value = self._2v(v)
                self.pyi.consts.append(kv)
            except Thrift2pyiException:
                continue

    def _thrift2pyi(self):
        self._consts2pyi()
        self._scan_includes()
        self._structs2pyi()
        self._unions2pyi()
        self._excs2pyi()
        self._services2pyi()
        self._enums2pyi()
        self._includes2pyi()

    def output(self):
        self._thrift2pyi()
        try:
            o = FormatCode(compose(self.pyi))[0]
        except:
            o = compose(self.pyi)
            print("format failed")

        if not self.out or self.prefix == self.out:
            with open("%s.pyi" % self.filename.replace(".thrift", "_thrift"), "w") as f:
                f.write(o)
            return

        if self.prefix:
            filename = self.filename.replace(self.prefix, self.out)
        else:
            filename = os.path.join(self.out, self.filename)

        dirname = os.path.dirname(filename)
        if not os.path.exists(dirname):
            os.makedirs(dirname, mode=0o755, exist_ok=True)

        with open("%s/__init__.py" % dirname, "w") as f:
            pass

        shutil.copyfile(self.filename, filename)

        with open("%s.pyi" % filename.replace(".thrift", "_thrift"), "w") as f:
            f.write(o)


if __name__ == "__main__":
    Thrift2pyi("./tests/example.thrift", prefix="", out="").output()
