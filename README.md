## Traffic Sign Classifier

This project is a **Traffic Sign Classifier** built with **Teachable Machine, Flask, and ESP32 (via Wokwi simulation)**.  
It focuses on a limited set of traffic signs that are **commonly seen in both the Philippines and the USA**.  

The purpose of this project is to demonstrate how AI can classify traffic signs in real time, and how such a system could be integrated into **dashcams, IoT devices, or mobile phones** for future innovation.

---

## Dataset Collected
- Collected **50+ images per class** using Teachable Machine.  
- Classes include:
  - Stop  
  - No Entry  
  - Speed Limit  
  - Pedestrian Crossing  
  - Others (fallback category)  
- Images were sourced from both US and Philippine traffic sign references to ensure shared recognition.

---

##  Tools Utilized
- **Frontend**: HTML, CSS, JavaScript (responsive design for mobile + laptop)  
- **Backend**: Flask + TensorFlow model integration  
- **Model Training**: Teachable Machine (Google)  
- **IoT Simulation**: ESP32 on Wokwi, MicroPython  
- **Deployment**: GitHub + Render (with Gunicorn for production)  

---

## Features
- **Web Interface**: Upload or capture traffic sign images via camera.  
- **Real-Time Classification**: Displays label + confidence score with progress bar.  
- **ESP32 Integration**: LEDs light up based on detected sign (Red = Stop, Blue = No Entry, Green = Pedestrian Crossing, Yellow = Speed Limit).  
- **Responsive Design**: Works on both laptops and mobile phones.  
- **Production Deployment**: Hosted on Render with Gunicorn for scalability.  

---

## Future Applications
- **Dashcam Integration**: Real-time traffic sign recognition for driver assistance.  
- **Mobile Phones**: Lightweight classifier for road safety apps.  
- **IoT Expansion**: Could connect to smart vehicles or traffic management systems.  

---
## Demo

---

## Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/traffic-sign-classifier.git
   cd traffic-sign-classifier
2. Install dependencies
pip install -r requirements.txt
3. Run this locally
python app.py
