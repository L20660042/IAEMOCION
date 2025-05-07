from flask import Flask, request, jsonify
from fer import FER
from PIL import Image
import io

app = Flask(__name__)
detector = FER()

@app.route('/analyze', methods=['POST'])
def analyze_image():
    file = request.files['image']
    image = Image.open(io.BytesIO(file.read()))
    emotion, score = detector.top_emotion(image)
    return jsonify({'emotion': emotion, 'score': score})
