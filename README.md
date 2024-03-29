# spike-recorder

[![Actions Status][actions-badge]][actions-link]
[![Documentation Status][rtd-badge]][rtd-link]
[![Code style: black][black-badge]][black-link]

[![PyPI version][pypi-version]][pypi-link]
[![Conda-Forge][conda-badge]][conda-link]
[![PyPI platforms][pypi-platforms]][pypi-link]

[![Gitter][gitter-badge]][gitter-link]

This package implements a Python interface for the 
[Backyard Brains Spike Recorder](https://backyardbrains.com/products/spikerecorder), a neural recording application. It
is based off a [fork](https://github.com/davidt0x/Spike-Recorder) of the original C++ code, found 
[here](https://github.com/BackyardBrains/Spike-Recorder). In addition, it contains two psychological experiment 
applications written in Python that control and record events via the SpikeRecorder. 

## Installation

You can install this library from [PyPI](https://pypi.org/project/spike-recorder/) with pip:

```bash
python -m pip install spike-recorder
```

## Usage

To run the SpikeRecorder application simply invoke it on the command line

```bash
spike-recorder
```

If you want to launch the SpikeRecorder application alongside either of the experiments
below then invoke them with the `--spike-reord` option. 

## Iowa Gambling Task

![Iowa Task Screenshot](docs/images/iowa_task_screenshot.png?raw=true "Iowa Task Screenshow")

To launch the Iowa Gambling Task Experiment, run:

```bash
iowa
```

There are some available options and arguments:

```
usage: iowa [-h] [--spike-record] [--total-deck-pulls TOTAL_DECK_PULLS] [--seed SEED]

optional arguments:
  -h, --help            show this help message and exit
  --spike-record        Launch Backyard Brains Spike Recorder in background. Default is do not run.
  --total-deck-pulls TOTAL_DECK_PULLS
                        The total number of deck pulls in the experiment. Default is 100.
  --seed SEED           Seed for the random number generators that control deck randomness. 
                        Default is 0 so behaviour between runs will be random but fixed


```

## Libet Experiment

![Libet Experiment Screenshot](docs/images/libet_task_screenshot.png?raw=true "Iowa Task Screenshow")

To launch the Libet Task Experiment, simply run:

```bash
libet
```

If you wish to adjust the speed of the clock or the number of trials in either phase, see the available options:

```
usage: libet [-h] [--spike-record] [--num-trials-paradigm1 NUM_TRIALS_PARADIGM1] [--num-trials-paradigm2 NUM_TRIALS_PARADIGM2] [--clock-hz-paradigm1 CLOCK_HZ_PARADIGM1] [--clock-hz-paradigm2 CLOCK_HZ_PARADIGM2]

optional arguments:
  -h, --help            show this help message and exit
  --spike-record        Launch Backyard Brains Spike Recorder in background. 
                        Default is do not run.
  --num-trials-paradigm1 NUM_TRIALS_PARADIGM1
                        The number of trials to conduct for paradigm one. Default is 20.
  --num-trials-paradigm2 NUM_TRIALS_PARADIGM2
                        The number of trials to conduct for paradigm two, 
                        in which time of urge is asked. Default is 20.
  --clock-hz-paradigm1 CLOCK_HZ_PARADIGM1
                        The number of full rotations the clock makes per second in paradigm one. 
                        Default is 1 but can be set lower than 1.
  --clock-hz-paradigm2 CLOCK_HZ_PARADIGM2
                        The number of full rotations the clock makes per second in paradigm two. 
                        Default is 1 but can be set lower than 1.

```



[actions-badge]:            https://github.com/davidt0x/py-spike-recorder/workflows/CI/badge.svg
[actions-link]:             https://github.com/davidt0x/py-spike-recorderactions
[black-badge]:              https://img.shields.io/badge/code%20style-black-000000.svg
[black-link]:               https://github.com/psf/black
[conda-badge]:              https://img.shields.io/conda/vn/conda-forge/spike-recorder
[conda-link]:               https://github.com/conda-forge/spike-recorder-feedstock
[gitter-badge]:             https://badges.gitter.im/PrincetonUniversity/py-spike-recorder.svg
[gitter-link]:              https://gitter.im/PrincetonUniversity/py-spike-recorder?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
[pypi-link]:                https://pypi.org/project/spike-recorder/
[pypi-platforms]:           https://img.shields.io/pypi/pyversions/spike-recorder
[pypi-version]:             https://badge.fury.io/py/spike-recorder.svg
[rtd-badge]:                https://readthedocs.org/projects/spike-recorder/badge/?version=latest
[rtd-link]:                 https://spike-recorder.readthedocs.io/en/latest/?badge=latest
[sk-badge]:                 https://scikit-hep.org/assets/images/Scikit--HEP-Project-blue.svg
