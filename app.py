from flask import Flask, request, jsonify
from fer import FER
import cv2
import numpy as np

app = Flask(__name__)
detector = FER()

@app.route("/")
def index():
    return "API de detección de emociones activa"

@app.route("/predict", methods=["POST"])
def predict():
    if "image" not in request.files:
        return jsonify({"error": "No se envió imagen"}), 400

    file = request.files["image"]
    img_array = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

    emotions = detector.detect_emotions(img)

    return jsonify({"emotions": emotions})
