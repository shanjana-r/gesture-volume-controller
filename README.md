# 🤏🔊 Gesture Volume Controller

> **Your hand is the volume knob.** Pinch to mute. Spread to max. No mouse, no keyboard—just your webcam.

This repository features a lightweight, real-time computer vision application that transforms hand gestures into precise system volume controls. Built using **Python**, **MediaPipe**, and **OpenCV**, it bridges real-time human-computer interaction (HCI) natively with the operating system's audio architecture.

---

## 🚀 The Core Challenge: Signal vs. Noise

Most basic computer vision projects map raw pixel distance directly to system values. In real-world environments, this creates a horribly jittery user experience due to camera noise, shifting lighting conditions, and natural hand tremors.

To solve this, this pipeline implements an **Exponential Smoothing Filter (α = 0.7)**.

\[\text{Volume}_{\text{smoothed}} = (\alpha \times \text{Volume}_{\text{target}}) + ((1 - \alpha) \times \text{Volume}\_{\text{previous}})\]

By tuning α to `0.7`, the system strikes the optimal mathematical balance between **low latency (responsiveness)** and **signal stability (fluid control)**.

---

## 🛠️ System Architecture & Workflow

```text
[ Webcam Feed ]
       │
       ▼
[ MediaPipe Hands ] ──► Extracts 21-point 3D Landmark coordinates
       │
       ▼
[ Euclidean Distance ] ──► Measures pixel span between Thumb (Pt 4) & Index (Pt 8)
       │
       ▼
[ Linear Interpolation ] ──► Maps pixel delta dynamically to a 0-100% scalar range
       │
       ▼
[ Exponential Smoothing ] ──► Filters out high-frequency sensor jitter (α = 0.7)
       │
       ▼
[ OS Audio API Layer ] ──► Direct volume execution (AppleScript for macOS / Pycaw for Windows)
```

---

## 📦 Features & Project Structure

- **Cross-Platform Compatibility:** Dedicated modules for both macOS and Windows architectures.
- **Visual Feedback Overlay:** Real-time on-screen HUD rendering displaying tracking status and volume metrics.
- **Resource Efficient:** Leverages MediaPipe's optimized machine learning pipeline to run smoothly on standard laptops without requiring a dedicated GPU.

```text
├── src/
│   ├── volume_control_mac.py      # Native AppleScript audio controller for macOS
│   └── volume_control_win.py      # Pycaw Core Audio API controller for Windows
├── requirements.txt               # Unified project dependencies
└── README.md
```

---

## ⚡ Quick Start

### 1. Prerequisites

Ensure you are running **Python 3.8+**.

### 2. Installation

Clone the repository and install the standard computer vision dependencies inside an isolated virtual environment:

```bash
# Clone the repository
git clone https://github.com
cd gesture-volume-controller

# Setup a clean virtual environment
python3 -m venv env
source env/bin/activate

# Install requirements
pip install -r requirements.txt
```

> **Note for Apple Silicon Users (M1/M2/M3/M4):** If you run into architecture architecture mismatch errors with global environments, force your installation using your direct virtual path: `./env/bin/python3 -m pip install -r requirements.txt`

### 3. Execution

Launch the module corresponding to your operating system:

**For macOS:**

```bash
python3 src/volume_control_mac.py
```

**For Windows:**

```bash
python3 src/volume_control_win.py
```

_Press **'q'** while focusing on the video frame pop-up window to exit the application cleanly._

---

## 🔮 Future Enhancements

- [ ] **Dynamic Space Calibration:** Implement auto-calibration loops to automatically adjust pixel thresholds based on the user's distance from the camera.
- [ ] **Multi-Gesture Command Matrix:** Expand mapping to include custom triggers (e.g., fist gesture for dynamic media playback toggles).
