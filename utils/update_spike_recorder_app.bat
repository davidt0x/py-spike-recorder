@ECHO OFF
rem This script will update the spike recorder app. It will also trigger a pip install of the package again
rem to rebuild the pybind11 module.

rem Pull the latest version of Spike-Recorder application from its repo
cd extern\Spike-Recorder
git pull origin master
cd ..\..\

rem Clean out the last _skbuild directory, eggs, and targets from editable
rem install.
rd /s /q  _skbuild
rd /s /q "spike_recorder.egg-info"
rd /s /q "src\spike_recorder.egg-info"
del /s /q /f src\spike_recorder\server\*.pyd
del /s /q /f src\spike_recorder\server\*.dll

rem Re-run pip install
pip install -v -e .[test]



