# 🥔 Potato Size Classifier — Portfolio Demo

Real-time potato detection, measurement, and classification on a conveyor belt using Raspberry Pi and OpenCV.

> **This is a portfolio demo** using synthetic images.
> Full working version (live camera, belt tracking, calibration, CSV export, web dashboard) delivered upon project completion.

---

## Demo Output

Run `python demo.py` to generate these annotated images locally:

**sample1.jpg** — Mixed medium/large potatoes at various rotation angles

**sample2.jpg** — Extra large potatoes

**sample3.jpg** — Full size range: Small → Extra Large

### Console output example
```
==================================================
   POTATO SIZE CLASSIFIER — Demo
==================================================

Image : samples/sample3.jpg
  Detected : 6 potato(es)
    Medium        length=5.1cm  width=3.8cm  angle=90.0°
    Large         length=7.1cm  width=5.1cm  angle=65.6°
    Large         length=8.8cm  width=6.3cm  angle=110.2°
    Extra Large   length=10.2cm width=7.0cm  angle=99.2°
    Extra Large   length=12.7cm width=8.4cm  angle=75.2°
    Extra Large   length=15.8cm width=10.1cm angle=124.9°
  Avg length : 9.9 cm
  Categories : Medium=1  Large=2  Extra Large=3
  Saved → samples/output/sample3.jpg
```

---

## Features (Demo)

- ✅ Detects and measures each potato — length + width in cm
- ✅ Works at any rotation angle
- ✅ Configurable size categories
- ✅ Real-time summary overlay on output image
- ✅ Overlap detection and flagging

## Full Version (delivered on project)

- 🎥 Live camera feed — USB, Pi Camera Module, IP camera
- 🔁 Conveyor belt tracking — line-crossing logic, no duplicate counting
- 📐 Camera calibration tool — click-based, outputs exact pixels/cm factor
- 📊 CSV report export per shift
- 🌐 Web dashboard — monitor from any device on local network
- ⚙️ Configurable categories, thresholds, and alert rules

---

## Quick Start

```bash
pip install opencv-python numpy
python demo.py
```

Annotated images are saved to `samples/output/`.

---

## How It Works

1. **Preprocessing** — grayscale → Gaussian blur → Otsu thresholding
2. **Contour detection** — isolates individual potato shapes
3. **Ellipse fitting** — `cv2.fitEllipse` extracts major/minor axes at any angle
4. **Measurement** — converts pixels to cm using calibration factor
5. **Classification** — assigns size category based on real length
6. **Overlay** — draws results on frame

---

## Hardware (Full Version)

- Raspberry Pi 3B+ or 4
- Pi Camera Module v2, USB webcam, or IP camera
- Optional: 7" RPi touchscreen or HDMI monitor

---

## Size Categories

Fully configurable in `classifier.py`:

| Category    | Length       |
|-------------|--------------|
| Small       | < 4.0 cm     |
| Medium      | 4.0 – 7.0 cm |
| Large       | 7.0 – 10.0 cm|
| Extra Large | > 10.0 cm    |

---

## License

MIT
