#include <filesystem>

#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl/filesystem.h>
//#include <omp.h>

#include "../src/AudioFile.h"
#include "../src/effects.h"

namespace py = pybind11;


PYBIND11_MODULE(wavfile, m) {
    py::class_<AudioFile>(m, "WavFile")
            .def(
                    pybind11::init<const std::filesystem::path &>(),
                    py::arg("file")
            )
            .def(
                    "save",
                    &AudioFile::save,
                    py::arg("file")
            )
            .def(
                    "normalize",
                    &AudioFile::normalize,
                    py::arg("peak_level") = -1.0,
                    py::arg("remove_dc") = true,
                    py::arg("stereo_independent") = false
            )
            .def(
                    "remove_clicks",
                    &AudioFile::remove_clicks,
                    py::arg("threshold_level") = 200,
                    py::arg("click_width") = 20,
                    py::arg("throw_exception") = false
            )
            .def(
                    "remove_all_channels_except",
                    &AudioFile::remove_all_channels_except,
                    py::arg("channel")
            )
            .def(
                    "to_mono",
                    &AudioFile::to_mono
            )
            .def("rms_linear", &AudioFile::rms_linear)
            .def("rms_db", &AudioFile::rms_db);
}

PYBIND11_MODULE(utils, m) {

    m.doc() = "Helpers for audio processing";

    m.def("normalize_from_file", &normalize_from_file,
          py::arg("input_file"),
          py::arg("output_file"),
          py::arg("peak_level") = -1.0,
          py::arg("remove_dc") = true,
          py::arg("stereo_independent") = false,
          "Normalize the audio file.");

    m.def("remove_clicks_from_file", &remove_clicks_from_file,
          py::arg("input_file"),
          py::arg("output_file"),
          py::arg("threshold_level") = 200,
          py::arg("click_width") = 20,
          py::arg("throw_exception") = false,
          "Remove clicks from an audio file.");

    m.def("measure_rms_linear_from_file", &measure_rms_linear_from_file, py::arg("input_file"), "Measures linear rms from an audio file");
    m.def("measure_rms_db_from_file", &measure_rms_db_from_file, py::arg("input_file"), "Measures rms in db from an audio file");

//    m.def("omp_get_max_threads", &omp_get_max_threads, "Get maximum number of OpenMP threads");
//    m.def("omp_set_num_threads", &omp_set_num_threads, "Get number of threads for OpenMP");
}

