# Assignment 1

## 1. System Information

本部分全部通过命令行采集，未使用图形界面。以下命令与输出均为原样复制。

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

## 3. Process Observation

## 4. Python Project B

## 5. C++ Manual Build

## 6. CMake Build

## 7. Git / GitHub

## 8. Problems and Notes
