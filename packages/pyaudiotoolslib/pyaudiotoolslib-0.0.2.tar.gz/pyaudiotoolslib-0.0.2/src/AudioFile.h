#pragma once

#include <filesystem>
#include <vector>
#include "sndfile.h"

class AudioFile {
public:

    explicit AudioFile(const std::filesystem::path &file);

    void save(const std::filesystem::path &file);

    AudioFile& normalize(double mPeakLevel, bool mRemoveDC, bool mStereoIndependent);

    AudioFile& remove_clicks(int mThresholdLevel, int mClickWidth, bool throw_exception = false);

    AudioFile& remove_all_channels_except(int channel);

    AudioFile& to_mono();

    float rms_linear();

    float rms_db();

private:
    SF_INFO sfInfo;

    std::vector<std::vector<float>> channels;
};
