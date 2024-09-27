/* Based on https://github.com/audacity/audacity/blob/master/src/effects/ClickRemoval.h
 * */
#pragma once


#include "audacity_mock.h"


class EffectClickRemoval final {
public:

    EffectClickRemoval(int mThresholdLevel, int mClickWidth);

    virtual ~EffectClickRemoval();

    bool ProcessOne(int count, WaveChannel &track, sampleCount start, sampleCount len, bool throw_exception = false);

    bool RemoveClicks(size_t len, float *buffer);


private:
    bool mbDidSomething; // This effect usually does nothing on real-world data.
    size_t windowSize;
    int mThresholdLevel;
    int mClickWidth;
    int sep;
};
