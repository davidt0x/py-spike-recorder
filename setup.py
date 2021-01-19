#!/usr/bin/env python
# Copyright (c) 2021, David Turner
#
# Distributed under the 3-clause BSD license, see accompanying file LICENSE
# or https://github.com/davidt0x/py-spike-recorder for details.

from setuptools import setup  # isort:skip

# Available at setup time due to pyproject.toml
from pybind11.setup_helpers import Pybind11Extension  # isort:skip

# Note:
#   Sort input source files if you glob sources to ensure bit-for-bit
#   reproducible builds (https://github.com/pybind/python_example/pull/53)

ext_modules = [
    Pybind11Extension(
        "spike_recorder._core",
        ["src/main.cpp"],
        cxx_std=11,
    ),
]


setup(
    ext_modules=ext_modules,
)
