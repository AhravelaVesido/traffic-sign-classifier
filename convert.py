# A model Converter - Run this once locally to convert savedmodel to model.tflite

import tensorflow as tf                                      # Full TensorFlow needed only for conversion (run locally)

model = tf.saved_model.load("model/saved_model/model.savedmodel")  # Load savedmodel instead of keras .h5
converter = tf.lite.TFLiteConverter.from_saved_model(              # Convert directly from savedmodel folder
    "model/saved_model/model.savedmodel"
)
tflite_model = converter.convert()                           # Convert to lightweight TFLite format

with open("model/model.tflite", "wb") as f:                 # Save the converted model to the model folder
    f.write(tflite_model)

print("Done! model/model.tflite saved.")                     # Confirm conversion was successful