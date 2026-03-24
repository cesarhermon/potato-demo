"""
Potato Size Classifier — Public Demo
=====================================
Detects and classifies potatoes from static images.
Full version (live camera, belt tracking, calibration tool,
CSV export, web dashboard) available upon project delivery.
"""

import cv2
import numpy as np
from dataclasses import dataclass
from typing import List

# Calibration factor (pixels per cm)
# Calculated from a reference object in the actual setup.
# Calibration tool included in full version.
PIXELS_PER_CM = 8.0

# Size categories — fully configurable
CATEGORIES = [
    ("Small",       0,    4.0),
    ("Medium",      4.0,  7.0),
    ("Large",       7.0,  10.0),
    ("Extra Large", 10.0, float("inf")),
]

MIN_AREA_PX = 300


@dataclass
class Potato:
    length_cm:   float
    width_cm:    float
    angle_deg:   float
    category:    str
    center:      tuple
    ellipse:     tuple
    overlapping: bool = False


def categorize(length_cm: float) -> str:
    for name, low, high in CATEGORIES:
        if low <= length_cm < high:
            return name
    return "Unknown"


def detect_potatoes(frame: np.ndarray) -> List[Potato]:
    """Detect and measure potatoes in a single frame."""
    gray  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur  = cv2.GaussianBlur(gray, (9, 9), 0)
    _, thresh = cv2.threshold(blur, 0, 255,
                              cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    kernel  = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    cleaned = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    contours, _ = cv2.findContours(cleaned, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    potatoes = []
    for cnt in contours:
        if cv2.contourArea(cnt) < MIN_AREA_PX or len(cnt) < 5:
            continue
        ellipse   = cv2.fitEllipse(cnt)
        cx, cy    = int(ellipse[0][0]), int(ellipse[0][1])
        major_px  = max(ellipse[1])
        minor_px  = min(ellipse[1])
        length_cm = major_px / PIXELS_PER_CM
        width_cm  = minor_px / PIXELS_PER_CM
        overlapping = (length_cm / width_cm) > 2.5 if width_cm > 0 else False
        potatoes.append(Potato(
            length_cm   = round(length_cm, 1),
            width_cm    = round(width_cm, 1),
            angle_deg   = round(ellipse[2], 1),
            category    = categorize(length_cm),
            center      = (cx, cy),
            ellipse     = ellipse,
            overlapping = overlapping,
        ))
    return potatoes


def draw_results(frame: np.ndarray, potatoes: List[Potato],
                 summary: dict) -> np.ndarray:
    """Draw detections and summary overlay."""
    h, w = frame.shape[:2]
    out  = frame.copy()
    colors = {
        "Small":       (255, 200,   0),
        "Medium":      ( 50, 205,  50),
        "Large":       (  0, 140, 255),
        "Extra Large": (  0,   0, 220),
        "Unknown":     (180, 180, 180),
    }
    for p in potatoes:
        color = (0, 80, 220) if p.overlapping else colors.get(p.category, (180,180,180))
        cv2.ellipse(out, p.ellipse, color, 2)
        label = "⚠ overlap" if p.overlapping else f"{p.length_cm}cm {p.category}"
        cv2.putText(out, label,
                    (p.center[0] - 40, p.center[1] - int(max(p.ellipse[1])//2) - 6),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1, cv2.LINE_AA)

    # Summary panel
    panel_w = 260
    overlay = out.copy()
    cv2.rectangle(overlay, (0, 0), (panel_w, h), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.55, out, 0.45, 0, out)

    lines = [
        ("POTATO CLASSIFIER",               (255, 255, 255)),
        ("",                                None),
        (f"Total:      {summary['total']}",         (200, 200, 200)),
        (f"Avg length: {summary['avg_length']:.1f} cm", (200, 200, 200)),
        (f"Avg width:  {summary['avg_width']:.1f} cm",  (200, 200, 200)),
        ("",                                None),
        ("CATEGORIES:",                     (180, 180, 180)),
    ]
    for cat, _, _ in CATEGORIES:
        count = summary["categories"].get(cat, 0)
        pct   = (count / summary["total"] * 100) if summary["total"] else 0
        lines.append((f"  {cat:<13} {count:>3}  {pct:>5.1f}%",
                       colors.get(cat, (180,180,180))))
    if summary.get("overlaps", 0):
        lines.append(("", None))
        lines.append((f"⚠ Overlaps: {summary['overlaps']}", (0, 80, 220)))

    y = 22
    for text, color in lines:
        if color:
            cv2.putText(out, text, (8, y),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, color, 1, cv2.LINE_AA)
        y += 18
    return out


def build_summary(potatoes: List[Potato]) -> dict:
    if not potatoes:
        return {"total": 0, "avg_length": 0, "avg_width": 0,
                "categories": {}, "overlaps": 0}
    cats = {cat: sum(1 for p in potatoes if p.category == cat)
            for cat, _, _ in CATEGORIES}
    return {
        "total":      len(potatoes),
        "avg_length": np.mean([p.length_cm for p in potatoes]),
        "avg_width":  np.mean([p.width_cm  for p in potatoes]),
        "categories": cats,
        "overlaps":   sum(1 for p in potatoes if p.overlapping),
    }
