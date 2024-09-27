#pragma once

#include "audacity_mock.h"


class EffectNormalize final {
public:

    explicit EffectNormalize(double mPeakLevel, bool mDC= true, bool mStereoIndependent= false);

    virtual ~EffectNormalize();

    bool ProcessOne(std::vector<std::vector<float>> &track, sampleCount start, sampleCount len) const;


private:
    double mPeakLevel;
    bool mDC;
    bool mStereoIndependent;
};

