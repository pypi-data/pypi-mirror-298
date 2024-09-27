#pragma once

#include <filesystem>
#include "AudioFile.h"


void remove_clicks_from_file(
        const std::filesystem::path &input_file,
        const std::filesystem::path &output_file,
        int mThresholdLevel = 200,
        int mClickWidth = 20,
        bool throw_exception = false
);


void normalize_from_file(
        const std::filesystem::path &input_file,
        const std::filesystem::path &output_file,
        double mPeakLevel = -1.0,
        bool mRemoveDC = true,
        bool mStereoIndependent = false
);

float measure_rms_linear_from_file(const std::filesystem::path &input_file);

float measure_rms_db_from_file(const std::filesystem::path &input_file);