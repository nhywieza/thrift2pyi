#! /usr/bin/env bash
#set -e

PROJECT_ROOT=$(cd $(dirname ${BASH_SOURCE[0]}); pwd)
cd ${PROJECT_ROOT}

export PYTHONPATH=$PYTHONPATH:$PROJECT_ROOT/thrift2pyi

check() {
    if [[ "0" -ne $? ]]; then
        exit
    fi
}
for thrift in `find tests -name "*.thrift"`
do
    echo "${thrift} start"
    python3 thrift2pyi ${thrift}
    check
    echo "${thrift} done"
done