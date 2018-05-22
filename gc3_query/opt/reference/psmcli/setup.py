#!/usr/bin/env python
# Copyright (c) 2015 Oracle and/or its affiliates. All rights reserved.
# created by abhijit.jere

""" Oracle Platform as a Service CLI Kit : setup.py"""

import os
from setuptools import setup, find_packages
import opaascli

CURDIR = os.path.abspath(os.path.dirname(__file__))
NAME = "psmcli"
DESCRIPTION = "Oracle Platform Service Manager Command Line Interface"
LICENSE = "License :: OSI Approved :: Common Public License", # ** Check with Oracle Legal! **
URL = "https://cloud.oracle.com"
INSTALL_REQUIRES = ["requests>=2.8.1,<=2.18.4", "keyring>=5.4,<=5.6", "colorama==0.3.3", "PyYAML==3.11"]
KEYWORDS = ["opc", "psmcli","psm", "paas", "oracle", "cloud"]
PACKAGES = ["opaascli", "opaascli/internal"]
PACKAGE_DATA={'opaascli': ['help/*.json']}
CLASSIFIERS = [
    "Natural Language :: English",
     # ** Check with Oracle Legal! **
    "License :: OSI Approved :: Common Public License",
    "Operating System :: POSIX :: Linux",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5"
]
SCRIPTS = ["psm", "psm.cmd"]
AUTHOR="Oracle"
AUTHOR_EMAIL="oraclesales_us@oracle.com"

setup_options = dict(
    name=NAME,
    description=DESCRIPTION,
    long_description=open(CURDIR+"/README.rst").read(),
    version=opaascli.__version__,
    license=LICENSE,
    url=URL,
    install_requires=INSTALL_REQUIRES,
    keywords=KEYWORDS,
    packages=PACKAGES,
    package_data=PACKAGE_DATA,
    include_package_data=True,
    zip_safe=False,
    classifiers=CLASSIFIERS,
    scripts=SCRIPTS,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
)

setup(**setup_options)
