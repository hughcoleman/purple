#!/usr/bin/env python
# -*- coding: utf-8 -*-

# setup.py
# Copyright (c) 2014 Brian Neal
# Copyright (c) 2020 Hugh Coleman
#
# This file is part of hughcoleman/system97, a historically accurate simulator 
# of the "System 97" or Type-B Cipher Machine. It is released under the MIT 
# License (see LICENSE.)

import setuptools
import system97

from pathlib import Path

with open(Path(__file__).parent / "README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="system97",
    version=system97.__version__,
    author="Hugh Coleman",
    author_email="33557709+hughcoleman@users.noreply.github.com",
    url="https://bitbucket.org/bgneal/purple/",
    license="MIT",
    description="A historically accurate simulator of the \"System 97\" or Type-B Cipher Machine.",
    long_description=long_description,
    packages=["system97"],
    # scripts=["scripts/purple"],
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Other Audience",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Communications",
        "Topic :: Security",
        "Topic :: Security :: Cryptography",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8"
)