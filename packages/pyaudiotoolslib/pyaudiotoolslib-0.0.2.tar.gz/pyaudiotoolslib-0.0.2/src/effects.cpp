#include "effects.h"

#include "AudioFile.h"

void remove_clicks_from_file(
        const std::filesystem::path &input_file,
        const std::filesystem::path &output_file,
        int mThresholdLevel,
        int mClickWidth,
        bool throw_exception
) {
    AudioFile(input_file)
            .remove_clicks(mThresholdLevel, mClickWidth, throw_exception)
            .save(output_file);
}


void normalize_from_file(
        const std::filesystem::path &input_file,
        const std::filesystem::path &output_file,
        double mPeakLevel,
        bool mRemoveDC,
        bool mStereoIndependent
) {
    AudioFile(input_file)
            .normalize(mPeakLevel, mRemoveDC, mStereoIndependent)
            .save(output_file);
}


float measure_rms_linear_from_file(const std::filesystem::path &input_file) {
    return AudioFile(input_file).rms_linear();
}

float measure_rms_db_from_file(const std::filesystem::path &input_file) {
    return AudioFile(input_file).rms_db();
}