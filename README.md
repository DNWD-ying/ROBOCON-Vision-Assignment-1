# Assignment 1

## 1. System Information

### 1.1 操作系统与内核

```bash
cat /etc/os-release
uname -r
```

```text
PRETTY_NAME="Ubuntu 24.04.5 LTS"
NAME="Ubuntu"
VERSION_ID="24.04"
VERSION="24.04.5 LTS (Noble Numbat)"
VERSION_CODENAME=noble
ID=ubuntu
ID_LIKE=debian
```

```text
7.0.0-34-generic
```

- Ubuntu 版本：**24.04.5 LTS (Noble Numbat)**
- Kernel 版本：**7.0.0-34-generic**

### 1.2 CPU

```bash
lscpu
```

关键字段：

```text
架构：                  x86_64
CPU:                    24
在线 CPU 列表：         0-23
厂商 ID：               GenuineIntel
型号名称：              Intel(R) Core(TM) i7-14650HX
CPU 最大 MHz：          5200.0000
CPU 最小 MHz：          800.0000
每个核的线程数：        2
每个座的核数：          16
座：                    1
L3 缓存：               30 MiB (1 instance)
NUMA 节点：             1
虚拟化：                VT-x
```

- CPU：**Intel(R) Core(TM) i7-14650HX**
- 拓扑：1 socket × 16 core × 2 thread = **24 逻辑处理器**
- 频率范围：800 MHz – 5200 MHz

### 1.3 GPU 与内核驱动

```bash
lspci | grep -Ei 'vga|3d|display'
```

```text
00:02.0 VGA compatible controller: Intel Corporation Raptor Lake-S UHD Graphics (rev 04)
02:00.0 VGA compatible controller: NVIDIA Corporation Device 2f18 (rev a1)
```

```bash
lspci -k | grep -EA3 'VGA|3D|Display'
```

```text
00:02.0 VGA compatible controller: Intel Corporation Raptor Lake-S UHD Graphics (rev 04)
	DeviceName: Onboard - Video
	Subsystem: Tongfang Hongkong Limited Raptor Lake-S UHD Graphics
	Kernel driver in use: i915
--
02:00.0 VGA compatible controller: NVIDIA Corporation Device 2f18 (rev a1)
	Subsystem: Tongfang Hongkong Limited Device 604e
	Kernel driver in use: nvidia
	Kernel modules: nvidiafb, nouveau, nvidia_drm, nvidia
```

本机为**双显卡（混合显卡）**环境：

| GPU | 设备 | 正在使用的内核驱动 |
|---|---|---|
| 集显 | Intel Raptor Lake-S UHD Graphics | `i915` |
| 独显 | NVIDIA GeForce RTX 5070 Ti Laptop GPU | `nvidia` |

注意 `Kernel modules` 一行列出 `nvidiafb, nouveau, nvidia_drm, nvidia` 表示内核中**存在**这些模块，
而 `Kernel driver in use: nvidia` 表示当前**实际生效**的是 NVIDIA 专有驱动，不是开源的 `nouveau`。

### 1.4 图形会话类型

```bash
echo "$XDG_SESSION_TYPE"
echo "$DISPLAY"
echo "$WAYLAND_DISPLAY"
```

```text
XDG_SESSION_TYPE=x11
DISPLAY=:1
WAYLAND_DISPLAY=
```

- 图形会话类型：**X11**（`XDG_SESSION_TYPE=x11`）
- `WAYLAND_DISPLAY` 为空，进一步确认当前不是 Wayland 会话

这一项对 Project A 有实际影响：OpenCV 的 `cv2.imshow` 依赖图形会话才能弹出窗口，
X11 下通过 `DISPLAY=:1` 正常显示。

### 1.5 NVIDIA Driver 与 CUDA Toolkit

```bash
nvidia-smi
```

```text
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 595.91.07              Driver Version: 595.91.07      CUDA Version: 13.2     |
+-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 5070 ...    Off |   00000000:02:00.0 Off |                  N/A |
| N/A   41C    P4             13W /   65W |      15MiB /  12227MiB |     24%      Default |
+-----------------------------------------+------------------------+----------------------+
```

```bash
nvcc --version
```

```text
/bin/bash: 行 76: nvcc: 未找到命令
```

- NVIDIA Driver：**595.91.07**
- CUDA Toolkit：**N/A（未安装）**

**必须区分的两点：**

| 项目 | 值 | 含义 |
|---|---|---|
| NVIDIA Driver 支持的 CUDA 能力 | 13.2 | `nvidia-smi` 右上角显示的 `CUDA Version`，指这个驱动**最高能支持**的 CUDA 运行时版本，是驱动的能力上限 |
| 实际安装的 CUDA Toolkit | 无 | `nvcc` 命令不存在，说明本机**没有安装** CUDA Toolkit |

`nvidia-smi` 里的 `CUDA Version: 13.2` **不能**等价为"本机已经安装了 CUDA 13.2 的 Toolkit"。
前者是驱动自带的能力声明，后者需要实际安装 `cuda-toolkit` 并具备 `nvcc` 编译器；
本机只满足前者。

对本 Assignment 而言，C++ 部分只需要 OpenCV 与 Eigen 的 CPU 版本，
**不依赖 CUDA Toolkit**，因此这一项缺失不影响后续任务。

### 1.6 汇总

```text
Ubuntu 版本:            24.04.5 LTS (Noble Numbat)
Kernel 版本:            7.0.0-34-generic
CPU:                    Intel(R) Core(TM) i7-14650HX, 16 核 / 24 线程
GPU:                    Intel Raptor Lake-S UHD Graphics (集显)
                        NVIDIA GeForce RTX 5070 Ti Laptop GPU (独显)
GPU 正在使用的内核驱动:   i915 (Intel) / nvidia (NVIDIA)
图形会话类型:            X11  (DISPLAY=:1, WAYLAND_DISPLAY 为空)
NVIDIA Driver:          595.91.07
CUDA Toolkit:           N/A (未安装, nvcc 不存在)
内存:                   31 GiB
架构:                   x86_64
```

## 2. Python Project A

### 2.1 准备工作：安装 Conda

本机原本没有 Conda，先安装 Miniconda（用户级安装，不需要 sudo）：

```bash
curl -fL -o /tmp/miniconda.sh \
  https://mirrors.tuna.tsinghua.edu.cn/anaconda/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash /tmp/miniconda.sh -b -p "$HOME/miniconda3"
"$HOME/miniconda3/bin/conda" init bash
```

```text
conda 26.7.1
```

由于到 `repo.anaconda.com` 的速度只有约 17 KB/s，安装包改从清华镜像获取（约 4.6 MB/s）。
conda 频道与 pip 索引也一并通过 `~/.condarc` 和 `~/.config/pip/pip.conf` 指向镜像：

```yaml
# ~/.condarc
channels:
  - conda-forge
channel_alias: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
default_channels: []
show_channel_urls: true
channel_priority: flexible
```

```ini
# ~/.config/pip/pip.conf
[global]
index-url = https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
trusted-host = mirrors.tuna.tsinghua.edu.cn
timeout = 60
```

### 2.2 创建环境

Project A 的 `pyproject.toml` 要求 `requires-python = ">=3.9,<3.11"`，
而本机系统 Python 是 3.12.3，无法满足，因此必须使用 Conda 环境：

```bash
conda create -n robocon_a python=3.10 -y
conda activate robocon_a
python --version
which python
```

```text
Python 3.10.21
/home/szc/miniconda3/envs/robocon_a/bin/python
```

`which python` 指向 conda 环境目录而不是 `/usr/bin/python3`，说明环境已正确激活。

### 2.3 安装依赖

```bash
cd python_A
pip install -r requirements.txt
```

```text
Successfully installed numpy-1.26.4 opencv-python-4.11.0.86
```

版本核对（对照 `VERSION_REQUIREMENTS.md`）：

| 依赖 | 实装版本 | 要求 | |
|---|---|---|---|
| Python | 3.10.21 | `>=3.9,<3.11` | ✅ |
| NumPy | 1.26.4 | `>=1.26,<2.0` | ✅ |
| OpenCV Python | 4.11.0.86 | `>=4.9,<5.0` | ✅ |

### 2.4 运行

```bash
python camera.py --camera 0 --output raw_capture.mp4 --width 640 --height 480 --fps 30
```

程序连续运行约 33 秒后，在 OpenCV 窗口中按 `q` 退出。程序完整输出：

```text
================================================================
ROBOCON Vision Assignment 1 - Python Project A
PID:          86141
PPID:         86133
Python:       /home/szc/miniconda3/envs/robocon_a/bin/python
Python ver.:  3.10.21
Camera index: 0
Raw output:   /home/szc/code/assignment2/ROBOCON-Vision-Assignment-1/python_A/raw_capture.mp4
Keep this process running and inspect it from another terminal.
Press q or ESC in an OpenCV window to exit.
================================================================
Actual stream: 640x480, writer FPS=30.00
Saved raw video: /home/szc/code/assignment2/ROBOCON-Vision-Assignment-1/python_A/raw_capture.mp4
Captured frames: 1000
Elapsed time:    33.3 s
Loop rate:       30.0 frame/s
```

程序启动时打印的 `PID` 与 `PPID` 供第 3 节 Process Observation 核对使用。

### 2.5 输出视频

```text
raw_capture.mp4: 1000 帧, 30.00 fps, 640x480, 时长 33.3 s
```

运行时长 33.3 秒，满足"连续运行至少 30 秒"的要求。

验证该视频确实是**未经处理的原始画面**（而非灰度或轮廓结果）：抽查第 0、500、999 帧的
B/G/R 三通道均值，三通道存在明显差异，说明是彩色帧：

```text
帧   0 可读=True B/G/R=92.4/104.8/104.1 彩差=12.4
帧 500 可读=True B/G/R=117.5/125.6/121.3 彩差=8.1
帧 999 可读=True B/G/R=119.9/127.5/123.0 彩差=7.7
```

若保存的是灰度图或轮廓图，三通道均值会几乎相等（彩差接近 0）。
源码中 `writer.write(frame)` 位于 `process_frame()` 之前，也保证了写入的是原始帧。

视频文件较大（13 MB），按 `.gitignore` 规则未提交到 Git，本地路径为
`python_A/raw_capture.mp4`。

### 2.6 图像结果截图

![Project A 三个窗口](assets/python_a/project_a_windows.png)

`assets/python_a/project_a_windows.png`

三个窗口来自**同一次运行**的 Project A，从左到右分别是：

```text
Project A - Original    原始图像
Project A - Grayscale   灰度图像
Project A - Contours    轮廓处理图像
```

截图说明：OpenCV 窗口默认以层叠方式出现，会互相遮挡，因此运行期间把三个窗口横向平铺
（窗口本身不支持缩放，`WINDOW_AUTOSIZE` 设定了固定尺寸提示，故用 `--width 640 --height 480`
让三个窗口能够并排放下）。

## 3. Process Observation

## 4. Python Project B

## 5. C++ Manual Build

## 6. CMake Build

## 7. Git / GitHub

## 8. Problems and Notes
