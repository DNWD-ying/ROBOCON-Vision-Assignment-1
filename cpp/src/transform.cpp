#include "transform.hpp"

#include <algorithm>
#include <vector>

#include <Eigen/Dense>
#include <opencv2/imgproc.hpp>

TransformResult transformFrame(const cv::Mat& bgr_frame) {
    if (bgr_frame.empty()) {
        return {};
    }

    cv::Mat gray;
    cv::cvtColor(bgr_frame, gray, cv::COLOR_BGR2GRAY);
    cv::GaussianBlur(gray, gray, cv::Size(5, 5), 0.0);

    // Use Eigen to calculate an approximate scene luma from the mean BGR color.
    const cv::Scalar mean_bgr = cv::mean(bgr_frame);
    const Eigen::Vector3d mean_color(mean_bgr[0], mean_bgr[1], mean_bgr[2]);
    const Eigen::Vector3d bgr_to_luma(0.114, 0.587, 0.299);
    const double luma = bgr_to_luma.dot(mean_color);

    cv::Mat binary;
    cv::threshold(
        gray,
        binary,
        0,
        255,
        cv::THRESH_BINARY | cv::THRESH_OTSU
    );

    const double low_threshold = std::clamp(0.66 * luma, 30.0, 150.0);
    const double high_threshold = std::clamp(
        1.33 * luma,
        low_threshold + 20.0,
        240.0
    );

    cv::Mat edges;
    cv::Canny(gray, edges, low_threshold, high_threshold);

    return {binary, edges, luma};
}

cv::Mat composePreview(const cv::Mat& original, const TransformResult& result) {
    cv::Mat binary_bgr;
    cv::Mat edges_bgr;
    cv::cvtColor(result.binary, binary_bgr, cv::COLOR_GRAY2BGR);
    cv::cvtColor(result.edges, edges_bgr, cv::COLOR_GRAY2BGR);

    const std::vector<cv::Mat> panels{original, binary_bgr, edges_bgr};
    cv::Mat combined;
    cv::hconcat(panels, combined);
    return combined;
}
