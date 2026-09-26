#!/usr/bin/env python3
"""Project A: live camera capture, simple image processing, and process observation."""

from __future__ import annotations

import argparse
import os
import sys
import time
from pathlib import Path
from typing import Optional

import cv2
import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Open a camera, display raw/grayscale/contour views, and save the "
            "unprocessed camera stream to MP4."
        )
    )
    parser.add_argument("--camera", type=int, default=0, help="Camera index. Default: 0")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("raw_capture.mp4"),
        help="Output path for the unprocessed camera video.",
    )
    parser.add_argument("--width", type=int, default=1280, help="Requested camera width")
    parser.add_argument("--height", type=int, default=720, help="Requested camera height")
    parser.add_argument("--fps", type=float, default=30.0, help="Requested/fallback FPS")
    return parser.parse_args()


def validated_fps(camera_fps: float, fallback: float) -> float:
    if not np.isfinite(camera_fps) or camera_fps <= 1.0 or camera_fps > 240.0:
        return fallback
    return camera_fps


def create_writer(path: Path, width: int, height: int, fps: float) -> cv2.VideoWriter:
    path.parent.mkdir(parents=True, exist_ok=True)
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    writer = cv2.VideoWriter(str(path), fourcc, fps, (width, height))
    if not writer.isOpened():
        raise RuntimeError(
            "Could not create the MP4 writer. Check the output path and the "
            "video-codec support of your OpenCV installation."
        )
    return writer


def process_frame(frame: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Return a grayscale view and a contour-overlay view."""
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blurred, 70, 140)

    contours, _ = cv2.findContours(
        edges,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE,
    )
    contour_view = frame.copy()
    cv2.drawContours(contour_view, contours, -1, (0, 255, 0), 2)
    return gray, contour_view


def print_runtime_context(args: argparse.Namespace) -> None:
    print("=" * 64)
    print("ROBOCON Vision Assignment 1 - Python Project A")
    print(f"PID:          {os.getpid()}")
    print(f"PPID:         {os.getppid()}")
    print(f"Python:       {sys.executable}")
    print(f"Python ver.:  {sys.version.split()[0]}")
    print(f"Camera index: {args.camera}")
    print(f"Raw output:   {args.output.resolve()}")
    print("Keep this process running and inspect it from another terminal.")
    print("Press q or ESC in an OpenCV window to exit.")
    print("=" * 64, flush=True)


def main() -> int:
    args = parse_args()
    print_runtime_context(args)

    capture = cv2.VideoCapture(args.camera)
    if not capture.isOpened():
        print(f"ERROR: cannot open camera index {args.camera}", file=sys.stderr)
        return 2

    capture.set(cv2.CAP_PROP_FRAME_WIDTH, args.width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, args.height)
    capture.set(cv2.CAP_PROP_FPS, args.fps)

    writer: Optional[cv2.VideoWriter] = None
    frame_count = 0
    start_time = time.monotonic()

    try:
        while True:
            ok, frame = capture.read()
            if not ok or frame is None:
                print("WARNING: failed to read a camera frame; stopping.", file=sys.stderr)
                break

            if writer is None:
                height, width = frame.shape[:2]
                actual_fps = validated_fps(
                    float(capture.get(cv2.CAP_PROP_FPS)),
                    args.fps,
                )
                writer = create_writer(args.output, width, height, actual_fps)
                print(
                    f"Actual stream: {width}x{height}, "
                    f"writer FPS={actual_fps:.2f}",
                    flush=True,
                )

            # Save the raw frame before any processing.
            writer.write(frame)
            frame_count += 1

            gray, contour_view = process_frame(frame)
            cv2.imshow("Project A - Original", frame)
            cv2.imshow("Project A - Grayscale", gray)
            cv2.imshow("Project A - Contours", contour_view)

            key = cv2.waitKey(1) & 0xFF
            if key in (ord("q"), 27):
                break

    except KeyboardInterrupt:
        print("\nInterrupted by Ctrl+C.")
    finally:
        capture.release()
        if writer is not None:
            writer.release()
        cv2.destroyAllWindows()

    elapsed = max(time.monotonic() - start_time, 1e-6)
    print(f"Saved raw video: {args.output.resolve()}")
    print(f"Captured frames: {frame_count}")
    print(f"Elapsed time:    {elapsed:.1f} s")
    print(f"Loop rate:       {frame_count / elapsed:.1f} frame/s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
