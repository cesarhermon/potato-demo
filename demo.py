"""
Potato Size Classifier — Demo
==============================
Runs the classifier on synthetic sample images.
Saves annotated output to samples/output/ and prints results to console.

Usage:
    python demo.py

NOTE: This is a portfolio demo using synthetic images.
Full version includes:
  - Live camera feed (USB, Pi Camera, IP camera)
  - Conveyor belt tracking (no duplicate counting)
  - Camera calibration tool
  - CSV report export per shift
  - Web dashboard for remote monitoring
"""

import os
import cv2
from generate_samples import generate_sample, POTATO_COLORS
from classifier import detect_potatoes, draw_results, build_summary

SAMPLES = {
    "samples/sample1.jpg": [
        ( 80, 100,  60, 45,  15, POTATO_COLORS[0]),
        (200, 100,  80, 55,   0, POTATO_COLORS[1]),
        (340, 100,  55, 40,  30, POTATO_COLORS[2]),
        (460, 100,  75, 50, -20, POTATO_COLORS[3]),
        (590, 100,  65, 48,  45, POTATO_COLORS[0]),
        (710, 100,  70, 52,  10, POTATO_COLORS[1]),
    ],
    "samples/sample2.jpg": [
        (100, 100, 110, 70,   0, POTATO_COLORS[2]),
        (280, 100,  95, 65,  25, POTATO_COLORS[3]),
        (460, 100, 120, 80, -30, POTATO_COLORS[0]),
        (650, 100, 100, 68,  45, POTATO_COLORS[1]),
    ],
    "samples/sample3.jpg": [
        ( 70, 100,  45, 35,   0, POTATO_COLORS[0]),
        (180, 100,  75, 55,  20, POTATO_COLORS[1]),
        (320, 100, 105, 70, -15, POTATO_COLORS[2]),
        (490, 100, 130, 85,  35, POTATO_COLORS[3]),
        (660, 100,  60, 45, -25, POTATO_COLORS[0]),
        (760, 100,  85, 60,  10, POTATO_COLORS[1]),
    ],
}


def run_demo():
    os.makedirs("samples/output", exist_ok=True)

    print("=" * 50)
    print("   POTATO SIZE CLASSIFIER — Demo")
    print("=" * 50)

    for path, data in SAMPLES.items():
        # Generate synthetic image
        generate_sample(path, data)
        frame = cv2.imread(path)

        # Detect and measure
        potatoes = detect_potatoes(frame)
        summary  = build_summary(potatoes)

        # Save annotated output
        out      = draw_results(frame, potatoes, summary)
        out_path = f"samples/output/{os.path.basename(path)}"
        cv2.imwrite(out_path, out)

        # Print results
        print(f"\nImage : {path}")
        print(f"  Detected : {summary['total']} potato(es)")
        for p in potatoes:
            flag = " ⚠ possible overlap" if p.overlapping else ""
            print(f"    {p.category:<13} "
                  f"length={p.length_cm}cm  "
                  f"width={p.width_cm}cm  "
                  f"angle={p.angle_deg}°{flag}")
        print(f"  Avg length : {summary['avg_length']:.1f} cm")
        print(f"  Categories : " +
              "  ".join(f"{k}={v}" for k, v in summary['categories'].items() if v > 0))
        print(f"  Saved → {out_path}")

    print("\n" + "=" * 50)
    print("Annotated images saved to samples/output/")
    print("=" * 50)


if __name__ == "__main__":
    run_demo()
