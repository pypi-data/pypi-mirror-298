#include "Normalize.h"

#include <cmath>

//#include <omp.h>

#include "../utils.h"


EffectNormalize::EffectNormalize(double mPeakLevel, bool mDC, bool mStereoIndependent) : mDC(mDC), mStereoIndependent(
        mStereoIndependent) {
    this->mPeakLevel = DB_TO_LINEAR(mPeakLevel);
}


EffectNormalize::~EffectNormalize() = default;

inline float get_peak_level(const std::vector<float> &channel, sampleCount start, sampleCount end) {

    float peakLevel = 0;

    for (decltype(start) i = start; i < end; ++i) {
        peakLevel = std::max(peakLevel, std::abs(channel[i]));
    }

    return peakLevel;
}

inline void multiply_volume(std::vector<float> &channel, sampleCount start, sampleCount end, float factor) {
//#if _MSC_VER && !__INTEL_COMPILER
//#pragma omp parallel for
//#else
//#pragma omp parallel for simd
//#endif
    for (decltype(start) i = start; i < end; ++i) {
        channel[i] *= factor;
    }
}

struct ChannelInfo {
    float signalMax = -1;
    float signalMin = 1;

    float dc_offset = 0;
};


inline ChannelInfo get_channel_info(const std::vector<float> &channel, sampleCount start, sampleCount end) {
    float signalMax = -1;
    float signalMin = 1;

    double dc_offset_double = 0;

//#if _MSC_VER && !__INTEL_COMPILER
//#pragma omp parallel for reduction(max:signalMax) reduction(min:signalMin) reduction(+:dc_offset_double)
//#else
//#pragma omp parallel for simd reduction(max:signalMax) reduction(min:signalMin) reduction(+:dc_offset_double)
//#endif
    for (decltype(start) i = start; i < end; ++i) {
        signalMax = std::max(signalMax, channel[i]);
        signalMin = std::min(signalMin, channel[i]);
        dc_offset_double += static_cast<double>(channel[i]);
    }

    auto dc_offset = -static_cast<float>(dc_offset_double / static_cast<double >(end - start));

    signalMax += dc_offset;
    signalMin += dc_offset;

    return {
            signalMax,
            signalMin,
            dc_offset,
    };
}

inline void
shift_and_multiply_volume(std::vector<float> &channel, sampleCount start, sampleCount end, float shift, float factor) {
//#if _MSC_VER && !__INTEL_COMPILER
//#pragma omp parallel for
//#else
//#pragma omp parallel for simd
//#endif
    for (decltype(start) i = start; i < end; ++i) {
        channel[i] = (channel[i] + shift) * factor;
    }
}

bool EffectNormalize::ProcessOne(std::vector<std::vector<float>> &track, sampleCount start, sampleCount len) const {


//    float *buffer = track.GetBufferPtr();
    auto end = start + len;

//    float currentPeakLevel = 0;

    if (mDC) {
        if (mStereoIndependent) {
            for (auto &channel: track) {
                auto channel_info = get_channel_info(channel, start, end);
                float currentPeakLevel = std::max(channel_info.signalMax, -channel_info.signalMin);
                auto ratio = static_cast<float >(mPeakLevel) / currentPeakLevel;
                shift_and_multiply_volume(channel, start, end, channel_info.dc_offset, ratio);
            }
        } else {

            float signalMax = -1;
            float signalMin = 1;
            float dc_offset = 0;
            for (auto &channel: track) {
                auto channel_info = get_channel_info(channel, start, end);
                signalMin = std::min(signalMin, channel_info.signalMin);
                signalMax = std::min(signalMax, channel_info.signalMax);
                dc_offset += channel_info.dc_offset;
            }
            dc_offset /= static_cast<float >(track.size());

            auto ratio = static_cast<float >(mPeakLevel) / std::max(signalMax, -signalMin);

            for (auto &channel: track) {
                shift_and_multiply_volume(channel, start, end, dc_offset, ratio);
            }
        }
    } else {
        if (mStereoIndependent) {
            for (auto &channel: track) {
                float currentPeakLevel = std::max(currentPeakLevel, get_peak_level(channel, start, end));

                auto ratio = static_cast<float >(mPeakLevel) / currentPeakLevel;

                multiply_volume(channel, start, end, ratio);
            }
        } else {
            float currentPeakLevel;
            for (const auto &channel: track) {
                currentPeakLevel = std::max(currentPeakLevel, get_peak_level(channel, start, end));
            }

            auto ratio = static_cast<float >(mPeakLevel) / currentPeakLevel;

            for (auto &channel: track) {
                multiply_volume(channel, start, end, ratio);
            }
        }
    }

    return true;
}