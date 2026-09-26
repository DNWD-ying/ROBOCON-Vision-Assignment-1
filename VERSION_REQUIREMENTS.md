# Version Requirements

以下版本范围是本 Assignment 的约束，而不是要求学生把所有软件升级到最新版本。

## Python Project A

- Python: `>=3.9,<3.11`
- NumPy: `>=1.26,<2.0`
- OpenCV Python: `>=4.9,<5.0`

推荐 Conda 环境使用 Python 3.10。

Project A 必须能够访问本机摄像头，并需要桌面图形会话以显示 OpenCV 窗口。

## Python Project B

- Python: `>=3.12,<3.14`
- NumPy: `>=2.0,<3.0`
- ImageIO: `>=2.36,<3.0`
- imageio-ffmpeg: `>=0.5,<1.0`
- scikit-image: `>=0.24,<0.27`

推荐 Conda 环境使用 Python 3.12 或 3.13。

Project B 不依赖 OpenCV。它读取 Project A 生成的 MP4，并通过 ImageIO/FFmpeg 写出处理后视频。

## C++ Task

- Language standard: C++17
- GCC: 建议 `>=9`
- Clang: 建议 `>=10`
- OpenCV C++: `>=4.5,<5.0`
- Eigen: `>=3.3,<4.0`
- CMake: 建议 `>=3.16`，但仓库中不会提供 `CMakeLists.txt`

Ubuntu 中通常需要 OpenCV 和 Eigen 的 development package，而不仅仅是 Python 包：

```text
libopencv-dev
libeigen3-dev
```

Python 环境里的 `opencv-python` 不能替代 C++ 编译所需的 OpenCV 头文件和链接库。

## 视频格式

三个项目默认都使用 MP4：

- Project A: `mp4v`
- Project B: FFmpeg / H.264
- C++ Task: `mp4v`

不同 Linux 安装中的视频编码支持可能略有区别。如果 OpenCV 能打开视频但不能写 MP4，应优先检查系统/发行版中的 OpenCV 视频编码支持，而不是修改图像处理逻辑。
