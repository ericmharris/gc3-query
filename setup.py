#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import io
import codecs
import os
import sys

import gc3_query


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

here = os.path.abspath(os.path.dirname(__file__))
with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=6.0',
    'colorama',
    'pendulum',
    'requests',
    'requestium',
    'selenium',
    'cookiecutter',
    'beautifulsoup4',
    'sortedcontainers',
    'sortedcontainers',
    'openpyxl',
    'psutil',
    'pycrypto',
    'prettyprinter',
    'deepdiff',
    'dataclasses',
    # 'pywin32',
    # 'keyring',
    # TODO: put package requirements here
]

setup_requirements = [
    'pytest-runner',
    # TODO(emharris_or): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest',
    # TODO: put package test requirements here
]

setup(
    name='gc3_query',
    version='0.1.0',
    description="Oracle Cloud utility for fetching and storing IaaS and PaaS data.",
    long_description=readme + '\n\n' + history,
    author="Eric Harris",
    author_email='eric.harris@oracle.com',
    url='https://github.com/emharris_or/gc3_query',
    packages=find_packages(include=['gc3_query']),
    entry_points={
        'console_scripts': [
            'gc3query=gc3_query.bin.gc3query:cli'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    cmdclass={'test': PyTest},
    license="MIT license",
    zip_safe=False,
    platforms='any',
    keywords='gc3_query',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    extras_require={
        'testing': ['pytest'],
    },
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
