"""
Synthetic sample image generator for demo purposes.
"""
import cv2
import numpy as np

POTATO_COLORS = [
    (80, 180, 210),
    (70, 170, 200),
    (90, 190, 220),
    (75, 175, 205),
]


def generate_sample(filename, potatoes, width=800, height=200):
    img = np.ones((height, width, 3), dtype=np.uint8) * 30
    for i in range(0, width, 40):
        cv2.line(img, (i, 0), (i, height), (25, 25, 25), 1)
    for (cx, cy, largo, ancho, angulo, color) in potatoes:
        axes = (int(largo // 2), int(ancho // 2))
        cv2.ellipse(img, (cx, cy), axes, angulo, 0, 360, color, -1)
        cv2.ellipse(img, (cx, cy), axes, angulo, 0, 360, (30, 50, 60), 2)
        cv2.ellipse(img, (cx, cy),
                    (max(1, axes[0]-8), max(1, axes[1]-6)),
                    angulo, 0, 360,
                    tuple(min(255, c + 30) for c in color), 1)
    cv2.imwrite(filename, img)


if __name__ == "__main__":
    import os
    os.makedirs("samples", exist_ok=True)

    generate_sample("samples/sample1.jpg", [
        (80,  100, 60, 45,  15, POTATO_COLORS[0]),
        (200, 100, 80, 55,   0, POTATO_COLORS[1]),
        (340, 100, 55, 40,  30, POTATO_COLORS[2]),
        (460, 100, 75, 50, -20, POTATO_COLORS[3]),
        (590, 100, 65, 48,  45, POTATO_COLORS[0]),
        (710, 100, 70, 52,  10, POTATO_COLORS[1]),
    ])
    generate_sample("samples/sample2.jpg", [
        (100, 100, 110, 70,   0, POTATO_COLORS[2]),
        (280, 100,  95, 65,  25, POTATO_COLORS[3]),
        (460, 100, 120, 80, -30, POTATO_COLORS[0]),
        (650, 100, 100, 68,  45, POTATO_COLORS[1]),
    ])
    generate_sample("samples/sample3.jpg", [
        ( 70, 100,  45, 35,   0, POTATO_COLORS[0]),
        (180, 100,  75, 55,  20, POTATO_COLORS[1]),
        (320, 100, 105, 70, -15, POTATO_COLORS[2]),
        (490, 100, 130, 85,  35, POTATO_COLORS[3]),
        (660, 100,  60, 45, -25, POTATO_COLORS[0]),
        (760, 100,  85, 60,  10, POTATO_COLORS[1]),
    ])
    print("Sample images generated in samples/")
