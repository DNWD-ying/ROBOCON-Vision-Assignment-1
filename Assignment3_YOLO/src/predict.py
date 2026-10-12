#!/usr/bin/env python3
"""用自己训出来的权重对一张图推理，打印检测框并保存标注图。

用法:
    conda activate yolo
    python src/predict.py <图片路径>

等价的 CLI 命令（README 里记录的是这条）:
    yolo detect predict model=runs/train/weights/best.pt source=<图片路径>
"""
import shutil
import sys
from pathlib import Path

from ultralytics import YOLO

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    if len(sys.argv) != 2:
        sys.exit(f"用法: python {sys.argv[0]} <图片路径>")
    src = Path(sys.argv[1]).resolve()
    if not src.exists():
        sys.exit(f"[错误] 找不到 {src}")

    model = YOLO(str(ROOT / "runs" / "train" / "weights" / "best.pt"))
    results = model.predict(source=str(src), conf=0.25, save=True,
                            project=str(ROOT / "runs"), name="predict",
                            exist_ok=True)

    # 标注图收进 results/，作为作业要求的提交件
    target = ROOT / "results" / "result.jpg"
    target.parent.mkdir(exist_ok=True)
    shutil.copyfile(ROOT / "runs" / "predict" / src.name, target)

    r = results[0]
    print(f"检出 {len(r.boxes)} 个框")
    print(f"{'类别':<12}{'置信度':>8}   x1, y1, x2, y2")
    for box in r.boxes:
        cls = int(box.cls[0])
        xyxy = ", ".join(f"{v:.0f}" for v in box.xyxy[0].tolist())
        print(f"{r.names[cls]:<12}{float(box.conf[0]):>8.3f}   {xyxy}")
    print(f"\n标注图已存到 {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
