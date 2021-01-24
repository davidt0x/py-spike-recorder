@ECHO OFF
rem This script will update the spike recorder app. It will also trigger a pip install of the package again
rem to rebuild the pybind11 module.

rem Pull the latest version of Spike-Recorder application from its repo
cd extern\Spike-Recorder
git pull origin master
cd ..\..\

rem Clean out the last _skbuild directory, eggs, and targets from editable
rem install.
set CMAKE_BUILD_DIR=_skbuild\win-amd64-3.8\cmake-build
rd /s /q  "%CMAKE_BUILD_DIR%\bass"
rd /s /q  "%CMAKE_BUILD_DIR%\data"
rd /s /q  "%CMAKE_BUILD_DIR%\CMakeFiles"
del /s /q /f "%CMAKE_BUILD_DIR%\CMakeCache.txt"

rd /s /q "spike_recorder.egg-info"
rd /s /q "src\spike_recorder.egg-info"
del /s /q /f src\spike_recorder\server\*.pyd
del /s /q /f src\spike_recorder\server\*.dll

rem Re-run pip install
pip install -v -e .[test]



