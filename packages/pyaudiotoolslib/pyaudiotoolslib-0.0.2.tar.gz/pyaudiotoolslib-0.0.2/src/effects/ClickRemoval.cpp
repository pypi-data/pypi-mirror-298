/* Based on https://github.com/audacity/audacity/blob/master/src/effects/ClickRemoval.cpp
 * */

#include "ClickRemoval.h"
#include <vector>
#include <stdexcept>
#include <sstream>


EffectClickRemoval::EffectClickRemoval(int mThresholdLevel, int mClickWidth) :
        mThresholdLevel(mThresholdLevel), mClickWidth(mClickWidth), mbDidSomething(false) {

    windowSize = 8192;
    sep = 2049;
}

EffectClickRemoval::~EffectClickRemoval() = default;


bool EffectClickRemoval::ProcessOne(int count, WaveChannel &track, size_t start, size_t len, bool throw_exception) {
    if (len <= windowSize / 2) {
        if (!throw_exception) return false;
        std::stringstream ss;
        ss << "Selection must be larger than " << windowSize / 2 << " samples";
        throw std::length_error(ss.str());
    }

    auto idealBlockLen = track.GetMaxBlockSize() * 4;
    if (idealBlockLen % windowSize != 0)
        idealBlockLen += (windowSize - (idealBlockLen % windowSize));

    bool bResult = true;
    decltype(len) s = 0;
    Floats buffer(idealBlockLen);
    Floats datawindow(windowSize);
    while ((len - s) > windowSize / 2) {
        auto block = limitSampleBufferSize(idealBlockLen, len - s);
        track.GetFloats(buffer.data(), start + s, block);
        for (decltype(block) i = 0; i + windowSize / 2 < block; i += windowSize / 2) {
            auto wcopy = std::min(windowSize, block - i);
            for (decltype(wcopy) j = 0; j < wcopy; ++j)
                datawindow[j] = buffer[i + j];
            for (auto j = wcopy; j < windowSize; ++j)
                datawindow[j] = 0;
            mbDidSomething |= RemoveClicks(windowSize, datawindow.data());
            for (decltype(wcopy) j = 0; j < wcopy; ++j)
                buffer[i + j] = datawindow[j];
        }

        if (mbDidSomething) {
            // RemoveClicks() actually did something.
            if (!track.SetFloats(buffer.data(), start + s, block)) {
                bResult = false;
                break;
            }
        }
        s += block;
        if (TrackProgress(count, static_cast<double >(s) / static_cast<double >(len))) {
            bResult = false;
            break;
        }
    }
    return bResult;
}


bool EffectClickRemoval::RemoveClicks(size_t len, float *buffer) {
    bool bResult = false; // This effect usually does nothing.
    size_t i;
    size_t j;
    int left = 0;

    float msw;
    int ww;
    int s2 = sep / 2;
    Floats ms_seq(len);
    Floats b2(len);

    for (i = 0; i < len; i++)
        b2[i] = buffer[i] * buffer[i];

    /* Shortcut for rms - multiple passes through b2, accumulating
     * as we go.
     */
    for (i = 0; i < len; i++)
        ms_seq[i] = b2[i];

    for (i = 1; (int) i < sep; i *= 2) {
        for (j = 0; j < len - i; j++)
            ms_seq[j] += ms_seq[j + i];
    }

    /* Cheat by truncating sep to next-lower power of two... */
    sep = i;

    for (i = 0; i < len - sep; i++) {
        ms_seq[i] /= sep;
    }
    /* ww runs from about 4 to mClickWidth.  wrc is the reciprocal;
     * chosen so that integer roundoff doesn't clobber us.
     */
    int wrc;
    for (wrc = mClickWidth / 4; wrc >= 1; wrc /= 2) {
        ww = mClickWidth / wrc;

        for (i = 0; i < len - sep; i++) {
            msw = 0;
            for (j = 0; (int) j < ww; j++) {
                msw += b2[i + s2 + j];
            }
            msw /= ww;

            if (msw >= mThresholdLevel * ms_seq[i] / 10) {
                if (left == 0) {
                    left = i + s2;
                }
            } else {
                if (left != 0 && ((int) i - left + s2) <= ww * 2) {
                    float lv = buffer[left];
                    float rv = buffer[i + ww + s2];
                    for (j = left; j < i + ww + s2; j++) {
                        bResult = true;
                        buffer[j] = (rv * (j - left) + lv * (i + ww + s2 - j)) / (float) (i + ww + s2 - left);
                        b2[j] = buffer[j] * buffer[j];
                    }
                    left = 0;
                } else if (left != 0) {
                    left = 0;
                }
            }
        }
    }
    return bResult;
}