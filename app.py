"""Flask web app for the Voice Command Intent Classifier."""
from flask import Flask, jsonify, render_template, request
from classifier import get_model, predict_intent

app = Flask(__name__)
model = get_model()


@app.get("/")
def home():
    return render_template("index.html")


@app.post("/predict")
def predict():
    payload = request.get_json(silent=True) or {}
    text = payload.get("text", "")
    if not isinstance(text, str):
        return jsonify({"error": "The command must be text."}), 400
    result = predict_intent(text, model)
    return jsonify(result)


@app.get("/health")
def health():
    return jsonify({"status": "ok", "model": "loaded"})


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
