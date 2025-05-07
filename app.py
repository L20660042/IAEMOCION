from flask import Flask, request, jsonify
from fer import FER
from flask_cors import CORS
import cv2
import numpy as np
import os

app = Flask(__name__)
CORS(app, origins=["https://l20660042.github.io"])

detector = FER(mtcnn=True)

@app.route("/")
def index():
    return "IAEmocion API online."

@app.route("/emotion/upload", methods=["POST"])
def upload_emotion():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image uploaded"}), 400

        image_file = request.files['image']
        user = request.form.get("user", "anonymous")

        # Leer imagen como numpy array
        img_bytes = image_file.read()
        npimg = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        # Detectar emociones
        result = detector.detect_emotions(img)
        if not result:
            return jsonify({"error": "No face detected"}), 400

        top_emotion = max(result[0]["emotions"], key=result[0]["emotions"].get)

        return jsonify({
            "emotion": top_emotion,
            "details": result[0]["emotions"],
            "user": user
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Agrega esto para que escuche en el puerto dinámico de Railway
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
