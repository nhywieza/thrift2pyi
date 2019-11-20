# coding: utf-8

import io
import os

from setuptools import find_packages, setup

NAME = 'thrift2pyi'
DESCRIPTION = 'convert thrift to pyi'
EMAIL = 'yanweizhi@bytedance.com'
AUTHOR = 'yanweizhi'

REQUIRES = [
    'six>=1.11.0,<2.0.0',
    'pypeg2>=2.15.2,<3.0.0',
    'thriftpy2>=0.4.2,<1.0.0',
    'yapf>=0.22.0,<1.0.0'
]

DEV_REQURIES = [
    'flake8>=3.5.0,<4.0.0',
    'nose>=1.3.7,<2.0.0',
    'mypy>=0.620; python_version>="3.4"',
    'tox>=3.0.0,<4.0.0',
]

here = os.path.abspath(os.path.dirname(__file__))

try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except IOError:
    long_description = DESCRIPTION

about = {}
with io.open(os.path.join(here, NAME, '__version__.py'), encoding='utf-8') as f:
    exec(f.read(), about)

setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
    ],
    keywords='thrift2pyi',
    packages=find_packages(exclude=['docs', 'tests']),
    test_suite='nose.collector',
    install_requires=REQUIRES,
    tests_require=[
        'nose>=1.3.7,<2.0.0'
    ],
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*',
    extras_require={
        ':python_version<"3.5"': [
            'typing>=3.6.4',
        ],
        'dev': DEV_REQURIES,
    },
    package_data={
        # for PEP484 & PEP561
        NAME: ['py.typed', '*.pyi'],
    },
    entry_points={
        'console_scripts': [
            'thrift2pyi = thrift2pyi.main:main',
        ],
    },
)
