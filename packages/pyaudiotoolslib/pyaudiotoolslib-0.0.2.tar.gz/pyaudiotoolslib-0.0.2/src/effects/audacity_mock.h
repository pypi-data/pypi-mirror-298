#pragma once

#include <cstddef>
#include <vector>


using sampleCount = size_t;

using Floats = std::vector<float>;

size_t limitSampleBufferSize(size_t lhs, size_t rhs);

bool TrackProgress(size_t count, double progress);

class WaveChannel final {
public:
    explicit WaveChannel(float * buffer, size_t len);

    [[nodiscard]] size_t GetMaxBlockSize() const;

    void GetFloats(float *dst_buffer, size_t start, size_t count) const;

    bool SetFloats(const float *src_buffer, size_t start, size_t count);

    float* GetBufferPtr();

private:
    float * buffer;
    size_t len;
};