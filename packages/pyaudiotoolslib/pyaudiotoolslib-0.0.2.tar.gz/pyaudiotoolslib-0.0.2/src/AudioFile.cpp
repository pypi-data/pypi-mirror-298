#include "AudioFile.h"

#include <sstream>

#include "effects/ClickRemoval.h"
#include "effects/Normalize.h"
#include "effects/audacity_mock.h"
#include "utils.h"


const int mThresholdLevelMin = 0;
const int mThresholdLevelMax = 900;

const int mClickWidthMin = 0;
const int mClickWidthMax = 40;


const double mPeakLevelMin = -145.0;
const double mPeakLevelMax = 0.0;

template<typename Number>
void ensure_in_range(const Number value, const Number lower, const Number upper, const char *name) {

    if (value < lower) {
        std::stringstream ss;
        ss << name << " should be greater or equal " << lower << " got " << value;
        throw std::invalid_argument(ss.str());
    }

    if (value > upper) {
        std::stringstream ss;
        ss << name << " should be less or equal " << upper << " got " << value;
        throw std::invalid_argument(ss.str());
    }
}


AudioFile::AudioFile(const std::filesystem::path &file) {

    if (!exists(file)) {
        std::stringstream ss;
        ss << file.string() << " not found";
        throw std::invalid_argument(ss.str());
    }

    // Открываем WAV файл
    SNDFILE *sndFile = sf_open(file.string().c_str(), SFM_READ, &sfInfo);
    if (!sndFile) {
        std::stringstream ss;
        ss << "Error opening WAV file: " << sf_strerror(sndFile);
        throw std::invalid_argument(ss.str());
    }

    // Нет каналов -> что-то не так с файлом
    if (sfInfo.channels == 0) {
        sf_close(sndFile);
        throw std::invalid_argument("No channels found in WAV file");
    }

    channels.resize(sfInfo.channels);

    // Когда канал один не нужно обрабатывать интерливинг -> никаких временных буферов
    if (sfInfo.channels == 1) {
        channels[0].resize(sfInfo.frames);

        if (sf_read_float(sndFile, channels[0].data(), sfInfo.frames) != sfInfo.frames) {
            sf_close(sndFile);
            throw std::invalid_argument("Error reading samples from WAV file");
        }

        sf_close(sndFile);

        return;
    }

    // Далее можно читать частями, но пока тут без оптимизаций
    // Читаем данные из WAV файла
    // Тут каналы чередуются
    // Например [Левый 1, Правый 1, Левый 2, Правый 2, Левый 3, Правый 3]
    std::vector<float> interleavedBuffer(sfInfo.frames * sfInfo.channels);
    if (sf_read_float(sndFile, interleavedBuffer.data(), sfInfo.frames * sfInfo.channels) !=
        sfInfo.frames * sfInfo.channels) {
        sf_close(sndFile);
        throw std::invalid_argument("Error reading samples from WAV file");
    }
    // Закрываем WAV файл
    sf_close(sndFile);

    for (int ch = 0; ch < sfInfo.channels; ++ch) {
        channels[ch].resize(sfInfo.frames);
    }

    // Если каналов больше одного, то переупаковываем их последовательно
    for (int i = 0; i < sfInfo.frames; ++i) {
        for (int ch = 0; ch < sfInfo.channels; ++ch) {
            channels[ch][i] = interleavedBuffer[i * sfInfo.channels + ch];
        }
    }
}


void AudioFile::save(const std::filesystem::path &file) {

    SF_INFO newSfInfo = sfInfo;
    SNDFILE *sndFile = sf_open(file.string().c_str(), SFM_WRITE, &newSfInfo);

    std::vector<float> interleavedBuffer(sfInfo.frames * sfInfo.channels);
    for (int ch = 0; ch < sfInfo.channels; ++ch) {
        for (int i = 0; i < sfInfo.frames; ++i) {
            interleavedBuffer[i * sfInfo.channels + ch] = channels[ch][i];
        }
    }

    if (sf_write_float(sndFile, interleavedBuffer.data(), sfInfo.frames * sfInfo.channels) !=
        sfInfo.frames * sfInfo.channels) {
        sf_close(sndFile);
        throw std::invalid_argument("Error writing samples to WAV file");
    }

    int saved = sf_close(sndFile);

    if (saved) {
        std::stringstream ss;
        ss << "Failed to close wav file. libsndfile error code " << saved;
        throw std::invalid_argument(ss.str());
    }
}

AudioFile &AudioFile::normalize(double mPeakLevel, bool mRemoveDC, bool mStereoIndependent) {

    ensure_in_range(mPeakLevel, mPeakLevelMin, mPeakLevelMax, "mThresholdLevel");

    EffectNormalize effect_normalize(mPeakLevel, mRemoveDC, mStereoIndependent);

    effect_normalize.ProcessOne(channels, 0, channels[0].size());

    return *this;
}

AudioFile &AudioFile::remove_clicks(int mThresholdLevel, int mClickWidth, bool throw_exception) {


    ensure_in_range(mThresholdLevel, mThresholdLevelMin, mThresholdLevelMax, "mThresholdLevel");
    ensure_in_range(mClickWidth, mClickWidthMin, mClickWidthMax, "mClickWidth");

    EffectClickRemoval effect_click_removal(mThresholdLevel, mClickWidth);

    for (int channel = 0; channel < sfInfo.channels; ++channel) {
        WaveChannel wave_channel(channels[channel].data(), channels[channel].size());
        effect_click_removal.ProcessOne(channel, wave_channel, 0, channels[channel].size(), throw_exception);
    }

    return *this;
}

AudioFile &AudioFile::remove_all_channels_except(int channel) {

    if (channel < 0) {
        std::stringstream ss;
        ss << "Channel should be greater or equal 0, got " << channel;
        throw std::invalid_argument(ss.str());
    }

    if (channel + 1 > sfInfo.channels) {
        std::stringstream ss;
        ss << "There is only " << sfInfo.channels << " channel in audio, got channel " << channel;
        throw std::invalid_argument(ss.str());
    }

    channels.erase(channels.begin() + channel + 1, channels.end());
    channels.erase(channels.begin(), channels.begin() + channel);

    sfInfo.channels = 1;


    return *this;
}

AudioFile &AudioFile::to_mono() {
    if (sfInfo.channels < 2) return *this;

    // Sum
    for (int channel = 1; channel < sfInfo.channels; ++channel) {
        for (int i = 0; i < sfInfo.frames; ++i) {
            channels[0][i] += channels[channel][i];
        }
    }

    // Avg
    for (int i = 0; i < sfInfo.frames; ++i) {
        channels[0][i] /= static_cast<float>(sfInfo.channels);
    }

    channels.erase(channels.begin() + 1, channels.end());

    sfInfo.channels = 1;

    return *this;
}

float AudioFile::rms_linear() {
    double rms = 0.0;

    for (const auto &channel: channels) {
        double channel_rms = 0.0;

        for (const auto amp: channel) {
            channel_rms += static_cast<double>(amp) * static_cast<double>(amp);
        }

        rms += channel_rms;
    }

    return static_cast<float >(std::sqrt(rms / static_cast<double>(sfInfo.channels * sfInfo.frames)));
}

float AudioFile::rms_db() {
    return LINEAR_TO_DB(rms_linear());
}
