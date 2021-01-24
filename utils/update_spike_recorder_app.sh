#!/bin/bash
# This script will update the spike recorder app. It will also trigger a pip install of the package again
# to rebuild the pybind11 module.

# Pull the latest version of Spike-Recorder application from its repo
cd extern/Spike-Recorder
git pull origin master
cd ../../

# Clean out the last _skbuild directory, eggs, and targets from editable
# install.
CMAKE_BUILD_DIR=`find _skbuild -name cmake-build`
rm -rf  "${CMAKE_BUILD_DIR}/bass"
rm -rf  "${CMAKE_BUILD_DIR}/data"
rm -rf  "${CMAKE_BUILD_DIR}/CMakeFiles"
rm -f "${CMAKE_BUILD_DIR}/CMakeCache.txt"

rm -rf spike_recorder.egg-info
rm -rf src/spike_recorder.egg-info
rm src/spike_recorder/server/*.so
rm src/spike_recorder/server/*.dylib

# Re-run pip install
pip install -v -e ".[test]"

