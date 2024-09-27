#include "audacity_mock.h"

#include <cmath>

size_t limitSampleBufferSize(size_t lhs, size_t rhs) {
    return std::min(lhs, rhs);
}

bool TrackProgress(size_t count, double progress) {
    return true;
}

WaveChannel::WaveChannel(float *buffer, size_t len) : buffer(buffer), len(len) {}

size_t WaveChannel::GetMaxBlockSize() const {
    return len;
}

void WaveChannel::GetFloats(float *dst_buffer, size_t start, size_t count) const {
    for (auto i = 0; i < count; ++i) {
        dst_buffer[i] = buffer[start + i];
    }
}

bool WaveChannel::SetFloats(const float *const src_buffer, size_t start, size_t count) {
    for (auto i = 0; i < count; ++i) {
        buffer[start + i] = src_buffer[i];
    }

    return true;
}

float *WaveChannel::GetBufferPtr() {
    return buffer;
}
