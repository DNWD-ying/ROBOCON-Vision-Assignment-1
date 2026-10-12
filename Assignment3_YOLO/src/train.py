#!/usr/bin/env python3
"""Assignment 3 训练脚本：用 yolo11n 预训练权重在 coco128 上微调。

用法:
    conda activate yolo
    python src/train.py

等价的 CLI 命令（README 里记录的是这条）:
    yolo detect train model=yolo11n.pt data=coco128.yaml epochs=30 imgsz=640 device=0
"""
from pathlib import Path

from ultralytics import YOLO

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    model = YOLO("yolo11n.pt")  # 官方预训练权重，首次运行自动下载
    model.train(
        data="coco128.yaml",  # ultralytics 内置小 COCO：128 张图、80 类，自动下载
        epochs=30,
        imgsz=640,
        device=0,
        project=str(ROOT / "runs"),
        name="train",
        exist_ok=True,
    )


if __name__ == "__main__":
    main()
