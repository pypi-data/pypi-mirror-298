#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This code is distributed under the terms and conditions
# from the Apache License, Version 2.0
#
# http://opensource.org/licenses/apache2.0.php

"""
Run with:

python ./setup.py install
"""

import os
import io
import subprocess

import setuptools.command.develop
from setuptools import setup


def read(fname):
    path = os.path.join(os.path.dirname(__file__), fname)
    return io.open(path, encoding='utf8').read()


class SetupDevelop(setuptools.command.develop.develop):
    """Docstring is overwritten."""

    def run(self):
        """
        Prepare environment for development.

        - Ensures 'nose' and 'coverage.py' are installed for testing.
        - Call super()'s run method.
        """
        subprocess.check_call(('pip', 'install', 'nose', 'coverage'))

        # Call super() (except develop is an old-style class, so we must call
        # directly). The effect is that the development egg-link is installed.
        setuptools.command.develop.develop.run(self)


SetupDevelop.__doc__ = setuptools.command.develop.develop.__doc__


setup(
    name='restricted-sqlitedict',
    version='1.0.0',
    description='Fork of sqlitedict with restricted pickle loading.',
    long_description=read('README.rst'),

    py_modules=['sqlitedict'],

    # there is a bug in python2.5, preventing distutils from using any non-ascii characters :(
    # http://bugs.python.org/issue2562
    author='Radim Rehurek, Victor R. Escobar, Andrey Usov, Prasanna Swaminathan, Jeff Quast, Maciek Stopa',
    author_email="me@radimrehurek.com",
    maintainer='Radim Rehurek',
    maintainer_email='me@radimrehurek.com',

    url='https://github.com/mstopa/restricted-sqlitedict',
    download_url='http://pypi.python.org/pypi/restricted-sqlitedict',

    keywords='sqlite, persistent dict, multithreaded',

    license='Apache 2.0',
    platforms='any',

    classifiers=[  # from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Database :: Front-Ends',
    ],
    cmdclass={'develop': SetupDevelop},
)
