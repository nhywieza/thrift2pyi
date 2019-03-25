# coding: utf-8

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse

from thrift2pyi.convert import Thrift2pyi


def main():
    parser = argparse.ArgumentParser(description='convert thrift to pyi')
    parser.add_argument("thrifts", type=str, nargs="+")
    args = parser.parse_args()
    for thrift in args.thrifts:
        Thrift2pyi(thrift).output()
