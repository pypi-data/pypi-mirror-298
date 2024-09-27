#include <filesystem>
#include <chrono>
#include <iostream>
//#include <omp.h>
#include "src/AudioFile.h"


int main(int argc, char *argv[]) {

    std::cout << "Test program:\n\rStep 1. Make mono\n\rStep 2. Declick\n\rStep 3. Normalize" << std::endl;

    if (argc != 3) {
        std::cout << "Usage: AudioToolsLib <source file> <destination file>" << std::endl;
        return 1;
    }

    auto input_file = std::filesystem::path(argv[1]);
    auto output_file = std::filesystem::path(argv[2]);


    int mThresholdLevel = 200;
    int mClickWidth = 20;

//    std::cout << "Threads " << omp_get_max_threads() << std::endl;

    std::cout << "Input file: " << input_file.string() << std::endl;
    std::cout << "Output file: " << output_file.string() << std::endl;


    std::chrono::steady_clock::time_point begin_read = std::chrono::steady_clock::now();
    std::unique_ptr<AudioFile> audioFile;
    try {
        audioFile = std::make_unique<AudioFile>(input_file);
    }
    catch (std::exception &exc) {
        std::cout << exc.what() << std::endl;
        return 1;
    }
    std::chrono::steady_clock::time_point end_read = std::chrono::steady_clock::now();
    std::cout << "Reading = "
              << std::chrono::duration_cast<std::chrono::milliseconds>(end_read - begin_read).count()
              << " ms | RMS " << audioFile->rms_db() << " bD" << std::endl;


    std::chrono::steady_clock::time_point begin_processing = std::chrono::steady_clock::now();
    audioFile
            ->to_mono()
            .remove_clicks(mThresholdLevel, mClickWidth)
            .normalize(-0.1, true, false);
    std::chrono::steady_clock::time_point end_processing = std::chrono::steady_clock::now();
    std::cout << "Processing = "
              << std::chrono::duration_cast<std::chrono::milliseconds>(end_processing - begin_processing).count()
              << " ms | RMS " << audioFile->rms_db() << " bD" << std::endl;


    std::chrono::steady_clock::time_point begin_save = std::chrono::steady_clock::now();
    try {
        audioFile->save(output_file);
    }
    catch (std::exception &exc) {
        std::cout << exc.what() << std::endl;
        return 1;
    }
    std::chrono::steady_clock::time_point end_save = std::chrono::steady_clock::now();
    std::cout << "Saving = "
              << std::chrono::duration_cast<std::chrono::milliseconds>(end_save - begin_save).count()
              << " ms" << std::endl;


    std::cout << "Total = "
              << std::chrono::duration_cast<std::chrono::milliseconds>(end_read - begin_read).count()
                 + std::chrono::duration_cast<std::chrono::milliseconds>(end_processing - begin_processing).count()
                 + std::chrono::duration_cast<std::chrono::milliseconds>(end_save - begin_save).count()
              << " ms" << std::endl;

    return 0;

}
