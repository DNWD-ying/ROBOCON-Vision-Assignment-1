#include <cstdlib>
#include <iostream>
#include <string>

#include <opencv2/opencv.hpp>

#include "transform.hpp"

int main(int argc, char** argv) {
    if (argc < 2 || argc > 3) {
        std::cerr << "Usage: " << argv[0] << " INPUT.mp4 [OUTPUT.mp4]\n";
        return EXIT_FAILURE;
    }

    const std::string input_path = argv[1];
    const std::string output_path =
        (argc == 3) ? argv[2] : "cpp_processed.mp4";

    cv::VideoCapture capture(input_path);
    if (!capture.isOpened()) {
        std::cerr << "Failed to open input video: " << input_path << "\n";
        return EXIT_FAILURE;
    }

    const int width = static_cast<int>(capture.get(cv::CAP_PROP_FRAME_WIDTH));
    const int height = static_cast<int>(capture.get(cv::CAP_PROP_FRAME_HEIGHT));
    if (width <= 0 || height <= 0) {
        std::cerr << "Invalid input video dimensions.\n";
        return EXIT_FAILURE;
    }

    double fps = capture.get(cv::CAP_PROP_FPS);
    if (!(fps > 1.0 && fps < 240.0)) {
        fps = 30.0;
    }

    const int fourcc = cv::VideoWriter::fourcc('m', 'p', '4', 'v');
    cv::VideoWriter writer(
        output_path,
        fourcc,
        fps,
        cv::Size(width * 3, height)
    );
    if (!writer.isOpened()) {
        std::cerr << "Failed to create output video: " << output_path << "\n";
        return EXIT_FAILURE;
    }

    cv::Mat frame;
    std::size_t frame_count = 0;
    double luma_sum = 0.0;

    while (capture.read(frame)) {
        const TransformResult result = transformFrame(frame);
        writer.write(composePreview(frame, result));
        luma_sum += result.scene_luma;
        ++frame_count;
    }

    capture.release();
    writer.release();

    const double mean_luma =
        (frame_count > 0) ? (luma_sum / static_cast<double>(frame_count)) : 0.0;

    std::cout << "Input: " << input_path << "\n";
    std::cout << "Output: " << output_path << "\n";
    std::cout << "Frames: " << frame_count << "\n";
    std::cout << "Mean scene luma: " << mean_luma << "\n";
    std::cout << "Panels: original | Otsu binary | Canny edges\n";

    return EXIT_SUCCESS;
}
