#!/usr/bin/env python3
"""Project B: offline video analysis in a Python environment incompatible with Project A."""

from __future__ import annotations

import argparse
from pathlib import Path

import imageio.v2 as imageio
import numpy as np
from skimage import color, exposure, feature, morphology, transform


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Read Project A's raw MP4 and produce a three-panel analysis video: "
            "original, Canny edges, and inter-frame motion."
        )
    )
    parser.add_argument("--input", type=Path, required=True, help="Input MP4 from Project A")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("advanced_analysis.mp4"),
        help="Output analysis MP4",
    )
    parser.add_argument(
        "--max-width",
        type=int,
        default=640,
        help="Maximum width of each panel before processing. Default: 640",
    )
    return parser.parse_args()


def resize_if_needed(frame: np.ndarray, max_width: int) -> np.ndarray:
    if max_width < 2:
        raise ValueError("--max-width must be at least 2")

    height, width = frame.shape[:2]
    if width > max_width:
        scale = max_width / float(width)
        new_height = max(2, int(round(height * scale)))
        frame = transform.resize(
            frame,
            (new_height, max_width),
            preserve_range=True,
            anti_aliasing=True,
        ).astype(np.uint8)

    # Many video encoders prefer even frame dimensions.
    height, width = frame.shape[:2]
    even_height = height - (height % 2)
    even_width = width - (width % 2)
    return frame[:even_height, :even_width]


def mask_to_rgb(mask: np.ndarray) -> np.ndarray:
    mono = mask.astype(np.uint8) * 255
    return np.repeat(mono[:, :, None], 3, axis=2)


def analyze_frame(
    rgb_frame: np.ndarray,
    previous_gray: np.ndarray | None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    gray = color.rgb2gray(rgb_frame)

    # Improve local contrast before edge detection.
    enhanced = exposure.equalize_adapthist(gray, clip_limit=0.02)
    edges = feature.canny(enhanced, sigma=1.5)

    if previous_gray is None:
        motion = np.zeros_like(gray, dtype=bool)
    else:
        motion = np.abs(gray - previous_gray) > 0.08
        motion = morphology.opening(motion, morphology.disk(2))
        motion = morphology.closing(motion, morphology.disk(3))

    return gray, edges, motion


def process_video(input_path: Path, output_path: Path, max_width: int) -> None:
    if not input_path.is_file():
        raise FileNotFoundError(f"Input video does not exist: {input_path}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    reader = imageio.get_reader(str(input_path))
    metadata = reader.get_meta_data()
    fps = float(metadata.get("fps", 30.0) or 30.0)
    if not (1.0 < fps < 240.0):
        fps = 30.0

    writer = imageio.get_writer(
        str(output_path),
        fps=fps,
        codec="libx264",
        quality=7,
        macro_block_size=2,
    )

    previous_gray: np.ndarray | None = None
    frame_count = 0

    try:
        for frame in reader:
            rgb_frame = resize_if_needed(np.asarray(frame), max_width)
            gray, edges, motion = analyze_frame(rgb_frame, previous_gray)
            previous_gray = gray

            edge_view = mask_to_rgb(edges)
            motion_view = mask_to_rgb(motion)
            combined = np.concatenate([rgb_frame, edge_view, motion_view], axis=1)
            writer.append_data(combined)

            frame_count += 1
            if frame_count % 30 == 0:
                print(f"Processed {frame_count} frames...", flush=True)
    finally:
        reader.close()
        writer.close()

    print(f"Input:  {input_path.resolve()}")
    print(f"Output: {output_path.resolve()}")
    print(f"Frames: {frame_count}")
    print("Panels: original | Canny edges | motion mask")


def main() -> int:
    args = parse_args()
    process_video(args.input, args.output, args.max_width)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
