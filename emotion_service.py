from flask import Flask, request, jsonify
from fer import FER
import cv2
import numpy as np

app = Flask(__name__)
detector = FER()

@app.route('/analyze', methods=['POST'])
def analyze_emotion():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    npimg = np.frombuffer(file.read(), np.uint8)
    img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    result = detector.detect_emotions(img)

    if result:
        emotions = result[0]['emotions']
        top_emotion = max(emotions, key=emotions.get)
        return jsonify({'emotion': top_emotion, 'details': emotions})
    else:
        return jsonify({'error': 'No emotion detected'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
