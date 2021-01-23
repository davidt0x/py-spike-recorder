#include <pybind11/pybind11.h>

#define STRINGIFY(x) #x
#define MACRO_STRINGIFY(x) STRINGIFY(x)

#include "widgets/Application.h"
#include "Game.h"
#include "Log.h"
#include <SDL.h>
#include <cstring>
#include <string>
#include <cerrno>
#include <ctime>
#include <exception>

#ifdef __WIN32__
#include <direct.h>
#else
#include <unistd.h>
#endif

namespace py = pybind11;

int run()
{
    pybind11::gil_scoped_release release;

	time_t t;
	time(&t);
	BackyardBrains::Log::msg("BYB SpieRecorder started on %s", ctime(&t));

	BackyardBrains::Game game;

	game.run();

	BackyardBrains::Log::msg("BYB SpikeRecorder exited normally.");

	pybind11::gil_scoped_acquire acquire;

	return 0;
}

PYBIND11_MODULE(_core, m) {
    m.doc() = R"pbdoc(
        Spike-Recorder Application Module
        -----------------------

        .. currentmodule:: spike_recorder_mod

        .. autosummary::
           :toctree: _generate

           run
    )pbdoc";

    m.def("run", &run, R"pbdoc(
        Run the SpikeRecorder application. This launches the complete recording GUI.

    )pbdoc");

#ifdef VERSION_INFO
    m.attr("__version__") = MACRO_STRINGIFY(VERSION_INFO);
#else
    m.attr("__version__") = "dev";
#endif
}