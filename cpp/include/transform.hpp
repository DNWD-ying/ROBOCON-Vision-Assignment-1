#pragma once

#include <opencv2/core.hpp>

struct TransformResult {
    cv::Mat binary;
    cv::Mat edges;
    double scene_luma = 0.0;
};

TransformResult transformFrame(const cv::Mat& bgr_frame);
cv::Mat composePreview(const cv::Mat& original, const TransformResult& result);
