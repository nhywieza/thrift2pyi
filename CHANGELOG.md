# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

## v1.0.1
增加参数 prefix 和 out
-p 用于指定 thrift 文件的前缀，前缀对应的路径不会出现在输出的文件中
-o 用于指定输出文件的路径，输出文件包括 thrift 文件、pyi 文件和 __init__.py
