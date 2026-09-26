cmake_minimum_required(VERSION 3.16)

project(robocon_vision_cpp
    VERSION 1.0.0
    DESCRIPTION "ROBOCON Vision Assignment 1 - C++ video transform"
    LANGUAGES CXX
)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# 手工编译时 -Iinclude 和 -I/usr/include/eigen3 由命令行给出,
# CMake 中分别由 target_include_directories 和 Eigen3::Eigen 的
# INTERFACE_INCLUDE_DIRECTORIES 提供。
find_package(OpenCV REQUIRED)
find_package(Eigen3 REQUIRED)

add_executable(video_processor
    src/main.cpp
    src/transform.cpp
)

target_include_directories(video_processor
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}/include
)

target_link_libraries(video_processor
    PRIVATE
        ${OpenCV_LIBS}
        Eigen3::Eigen
)
