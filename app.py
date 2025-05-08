from flask import Flask, request, jsonify
import numpy as np
from PIL import Image
import io
import spacy

app = Flask(__name__)
nlp = spacy.load("es_core_news_sm")

@app.route('/analyze/drawing', methods=['POST'])
def analyze_drawing():
    try:
        if 'image' not in request.files:
            return jsonify({"error": "No image provided"}), 400
        
        image = request.files['image'].read()
        user = request.form.get('user', 'anonymous')
        
        # Simulación de análisis de emociones
        emotions = ["feliz", "triste", "enojado", "sorprendido"]
        emotion_idx = hash(image) % len(emotions)
        confidence = 0.7 + (hash(image) % 30) / 100
        
        return jsonify({
            "user": user,
            "emotion": emotions[emotion_idx],
            "confidence": confidence,
            "details": {
                "model": "simulated",
                "emotion_distribution": {
                    "feliz": 0.25,
                    "triste": 0.25,
                    "enojado": 0.25,
                    "sorprendido": 0.25
                }
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/analyze/text', methods=['POST'])
def analyze_text():
    try:
        text = request.form.get('text', '')
        user = request.form.get('user', 'anonymous')
        doc = nlp(text)
        
        # Análisis simplificado
        positive = sum(1 for token in doc if token.lemma_ in ["feliz", "contento", "alegre"])
        negative = sum(1 for token in doc if token.lemma_ in ["triste", "enojado", "molesto"])
        
        sentiment = "neutral"
        if positive > negative:
            sentiment = "positive"
        elif negative > positive:
            sentiment = "negative"
        
        return jsonify({
            "user": user,
            "sentiment": sentiment,
            "spellingErrors": [],
            "details": {
                "tokens": [token.text for token in doc],
                "lemmas": [token.lemma_ for token in doc],
                "posTags": [token.pos_ for token in doc]
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)