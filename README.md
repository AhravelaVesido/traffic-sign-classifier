# Traffic Sign Classifier

A real-time traffic sign classifier built with Teachable Machine, Flask, and ESP32 (via Wokwi simulation). This project focuses on a limited set of traffic signs commonly seen in both the Philippines and the USA.

The purpose of this project is to demonstrate how AI can classify traffic signs in real time, and how such a system could be integrated into dashcams, IoT devices, or mobile phones for future innovation.

---

## Dataset Collected

- Collected 50+ images per class using Teachable Machine
- Classes include:
  - Stop
  - No Entry
  - Speed Limit
  - Pedestrian Crossing
  - Others (fallback category)
- Images were sourced from both US and Philippine traffic sign references to ensure shared recognition

---

## Tools Utilized

| Layer | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript (responsive for mobile + laptop) |
| Backend | Flask, Flask-SocketIO, Flask-CORS |
| Model Training | Teachable Machine (Google) |
| Model Inference | TFLite Runtime (lightweight, optimized for free-tier deployment) |
| IoT Simulation | ESP32 on Wokwi, MicroPython |
| Deployment | GitHub + Render (Docker + Gunicorn + Gevent) |

---

## Features

- **Web Interface** — Upload or capture traffic sign images via camera
- **Real-Time Classification** — Displays label and confidence score with progress bar
- **ESP32 Integration** — LEDs light up based on detected sign:
  - 🔴 Red = Stop
  - 🔵 Blue = No Entry
  - 🟢 Green = Pedestrian Crossing
  - 🟡 Yellow = Speed Limit
- **WebSocket Support** — Results pushed to frontend and Wokwi instantly via Flask-SocketIO
- **Responsive Design** — Works on both laptops and mobile phones
- **Production Deployment** — Hosted on Render with Gunicorn + Gevent workers

---

## Project Structure

```
Traffic Signs Classifier/
├── model/
│   ├── saved_model/
│   │   └── model.savedmodel/     # Original Teachable Machine export
│   ├── model.tflite              # Converted lightweight model for deployment
│   └── labels.txt                # Class labels
├── static/
│   ├── script.js
│   └── styles.css
├── templates/
│   └── index.html
├── wokwi/
│   ├── diagram.json              # ESP32 wiring layout
│   └── main.py                   # MicroPython code for ESP32
├── app.py                        # Flask backend
├── convert.py                    # One-time script to convert model to .tflite
├── Dockerfile                    # Docker config for Render deployment
├── requirements.txt
└── README.md
```

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/traffic-sign-classifier.git
cd traffic-sign-classifier
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run locally

```bash
python app.py
```

Then open `http://localhost:5000` in your browser.

---

## Deployment (Render)

This project is deployed on Render using Docker. Key deployment decisions made during setup:

### Why Docker?
Docker ensures the exact Python version and system dependencies are consistent between local and production environments.

### Why Gevent instead of Eventlet?
`eventlet` conflicts with TensorFlow at a low level (both patch Python's networking). `gevent` achieves the same async concurrency without the conflict, making it the correct choice when using ML libraries.

### Why TFLite Runtime instead of full TensorFlow?
Full TensorFlow (~400MB) exceeds Render's free tier RAM limit (512MB). Converting the model to `.tflite` and using `tflite-runtime` (~5MB) reduces memory usage to under 100MB, fitting comfortably within the free tier.

### Why NumPy < 2?
`tflite-runtime==2.13.0` was compiled against NumPy 1.x. NumPy 2.0 broke binary compatibility, so `numpy<2` is pinned to avoid import errors.

### Dockerfile

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN apt-get update && apt-get install -y gcc build-essential && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
CMD gunicorn --worker-class gevent -w 1 --timeout 120 --bind 0.0.0.0:$PORT app:app
```

### Requirements

```
flask
flask-cors
flask-socketio
tflite-runtime==2.13.0
pillow
numpy<2
gunicorn
gevent
gevent-websocket
```

---

## Converting the Model (One-Time, Run Locally)

If you need to regenerate the `.tflite` model from the original SavedModel:

```bash
python convert.py
```

This converts `model/saved_model/model.savedmodel` → `model/model.tflite`.
Full TensorFlow must be installed locally to run this script. It is not needed on the server.

---

## Wokwi ESP32 Integration

The ESP32 polls the `/latest` endpoint of the deployed backend every few seconds to get the most recent classification result and light the corresponding LED.

Make sure your `wokwi/main.py` points to your Render URL:

```python
url = "https://traffic-sign-classifier-1-qypn.onrender.com/latest"
```

---

## Future Applications

- **Dashcam Integration** — Real-time traffic sign recognition for driver assistance
- **Mobile Phones** — Lightweight classifier for road safety apps
- **IoT Expansion** — Could connect to smart vehicles or traffic management systems

---

## Live Demo

🌐 [https://traffic-sign-classifier-1-qypn.onrender.com](https://traffic-sign-classifier-1-qypn.onrender.com)

> Note: The app is hosted on Render's free tier and may take 30–60 seconds to wake up after a period of inactivity.