# Traffic Sign Classifier - Backend

from flask import Flask, request, jsonify, render_template   # Flask server, request handles uploads, jsonify sends JSON
from flask_cors import CORS                                  # Allows frontend to talk to Flask even if on different ports
from flask_socketio import SocketIO                          # Keeps live connection open between Flask, website, and Wokwi
import numpy as np                                           # Converts image into numbers for the model
from PIL import Image                                        # Opens, converts, and resizes uploaded images
import tensorflow as tf                                      # Runs the trained traffic sign model
import io                                                    # Handles raw image bytes from uploads
from pyngrok import ngrok                                    # Creates temporary public tunnel for outside devices
import os                                                    # Used to check environment variables
import time 

app = Flask(__name__)                                        # Create the Flask server
CORS(app)                                                    # Allow cross-origin requests (frontend can connect)
socketio = SocketIO(app, cors_allowed_origins="*")           # Attach WebSocket, * means any address can connect

model = tf.saved_model.load("model/saved_model/model.savedmodel")   # Load the trained TensorFlow model
labels = open("model/labels.txt").read().splitlines()               # Read labels.txt and split into list

CONFIDENCE_THRESHOLD = 0.90                             # Reject results below 75% confidence

latest_result = {"label": "Unknown", "recognized": False}    # Store last classification result for Wokwi polling

@app.route("/classify", methods=["POST"])                    # Route: classify uploaded image
def classify():
    file = request.files["image"]                            # Receive uploaded image
    img = Image.open(io.BytesIO(file.read())).convert("RGB").resize((224, 224))  # Convert to RGB, resize to 224x224
    img_array = np.expand_dims(np.array(img, dtype=np.float32) / 255.0, axis=0)  # Normalize pixels, wrap in batch

    infer = model.signatures["serving_default"]              # Run model inference
    predictions = list(infer(tf.constant(img_array)).values())[0][0].numpy()  # Get confidence scores

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
                for l, c in zip(labels, predictions)                   # zip() combines labels and predictions
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
    return jsonify(latest_result)                            # Return last classification result

@app.route("/url")
def url():
    return jsonify({"public_url": public_url})                 # Route added in Flask so that Wokwi won't need hardcoded url

if __name__ == "__main__":                                   # Run only if executed directly
    if os.environ.get("WERKZEUG_RUN_MAIN") != "true":        # Prevent ngrok from running twice in debug mode
        ngrok.kill()                                         # Kill any existing ngrok tunnels
        ngrok.set_auth_token(os.getenv("NGROK_AUTH_TOKEN")          # Set your ngrok authtoken
        public_url = ngrok.connect(addr=5000, proto="http", bind_tls=False)  # Start ngrok tunnel on port 5000, forces ngrok to be on http only
        print("Public URL:", public_url)                     # Print the public URL for frontend/Wokwi use
    
    socketio.run(app, host="0.0.0.0", port=5000, debug=True) # Run Flask with SocketIO, debug=True shows errors

