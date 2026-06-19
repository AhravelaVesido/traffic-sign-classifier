# Traffic Sign Classifier - Backend

from flask import Flask, request, jsonify, render_template   # Flask server, request handles uploads, jsonify sends JSON
from flask_cors import CORS                                  # Allows frontend to talk to Flask even if on different ports
from flask_socketio import SocketIO                          # Keeps live connection open between Flask, website, and Wokwi
import tflite_runtime.interpreter as tflite                  # Lightweight TFLite runtime about 5MB instead of  400MB for full TensorFlow for Render deployment
import numpy as np                                           # Converts image into numbers for the model
from PIL import Image                                        # Opens, converts, and resizes uploaded images
import io                                                    # Handles raw image bytes from uploads
import os                                                    # Used to check environment variables

app = Flask(__name__)                                        # Create the Flask server
CORS(app)                                                    # Allow cross-origin requests (frontend can connect)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")  # Attach WebSocket, * means any address can connect, gevent library so python can handle many tasks at once

interpreter = tflite.Interpreter(model_path="model/model.tflite")  # Load the lightweight TFLite model
interpreter.allocate_tensors()                               # Allocate memory for model input/output tensors
input_details = interpreter.get_input_details()             # Get input tensor info (shape, dtype)
output_details = interpreter.get_output_details()           # Get output tensor info (confidence scores)
labels = open("model/labels.txt").read().splitlines()       # Read labels.txt and split into list

CONFIDENCE_THRESHOLD = 0.90                                  # Reject results below 90% confidence

latest_result = {"label": "Unknown", "recognized": False}    # Store last classification result for Wokwi polling

@app.route("/classify", methods=["POST"])                    # Route: classify uploaded image
def classify():
    file = request.files["image"]                            # Receive uploaded image
    img = Image.open(io.BytesIO(file.read())).convert("RGB").resize((224, 224))  # Convert to RGB, resize to 224x224
    img_array = np.expand_dims(np.array(img, dtype=np.float32) / 255.0, axis=0)  # Normalize pixels, wrap in batch

    interpreter.set_tensor(input_details[0]['index'], img_array)  # Feed image into model input tensor
    interpreter.invoke()                                           # Run inference
    predictions = interpreter.get_tensor(output_details[0]['index'])[0]  # Get confidence scores from output tensor

    top_index = np.argmax(predictions)                       # Find index of highest confidence
    top_confidence = float(predictions[top_index])           # Get confidence value
    top_label = labels[top_index].split(" ", 1)[1]           # Strip number from label (e.g. "2 Stop" → "Stop")

    if top_confidence < CONFIDENCE_THRESHOLD:                # If confidence too low, return Unknown
        result = {"label": "Unknown", "confidence": top_confidence, "recognized": False}
    else:                                                    # Else return label + all scores
        result = {
            "label": top_label,
            "confidence": top_confidence,
            "recognized": True,
            "all": [
                {"label": l.split(" ", 1)[1], "confidence": float(c)}  # Pair each label with its score
                for l, c in zip(labels, predictions)                    # zip() combines labels and predictions
            ],
        }

    global latest_result                                     # Save result for Wokwi polling
    latest_result = result

    socketio.emit("sign_detected", result)                   # Send result to frontend + Wokwi via WebSocket
    return jsonify(result)                                   # Return result to frontend as JSON

@app.route("/")                                              # Route: root URL
def index():
    return render_template("index.html")                     # Serve index.html from templates folder

@app.route("/latest")                                        # Route: Wokwi polls latest result
def latest():
    try:
        return jsonify(latest_result)                        # Return the current global result (updated in /classify)
    except Exception:
        return jsonify({                                     # Fallback if latest_result is missing or invalid
            "label": "Unknown",
            "recognized": False
        })

# NOTE: Removed ngrok and /url route since Render provides a permanent public domain

if __name__ == "__main__":                                   # Run only if executed directly
    port = int(os.environ.get("PORT", 5000))                 # Render's assigned port for deployment
    socketio.run(app, host="0.0.0.0", port=port)             # use socketio.run