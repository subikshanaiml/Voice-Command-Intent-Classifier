"""Text intent classifier using TF-IDF features and Logistic Regression."""
import json
from pathlib import Path
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "intents.json"
MODEL_DIR = ROOT / "model"
MODEL_FILE = MODEL_DIR / "intent_classifier.joblib"


def load_training_data():
    """Load example utterances and their intent labels."""
    data = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    texts, labels = [], []
    for intent, examples in data.items():
        for example in examples:
            texts.append(example)
            labels.append(intent)
    return texts, labels


def train_model():
    """Train and save the model."""
    texts, labels = load_training_data()
    pipeline = Pipeline([
        ("tfidf", TfidfVectorizer(
            lowercase=True,
            strip_accents="unicode",
            ngram_range=(1, 2),
            sublinear_tf=True
        )),
        ("classifier", LogisticRegression(
            max_iter=1000,
            class_weight="balanced",
            random_state=42
        ))
    ])
    pipeline.fit(texts, labels)
    MODEL_DIR.mkdir(exist_ok=True)
    joblib.dump(pipeline, MODEL_FILE)
    return pipeline


def get_model():
    """Load the saved model, training it on first run if necessary."""
    if not MODEL_FILE.exists():
        return train_model()
    return joblib.load(MODEL_FILE)


def predict_intent(text, model=None):
    """Return the predicted intent, confidence and a safe fallback."""
    cleaned = " ".join(str(text).strip().split())
    if not cleaned:
        return {"intent": "unknown", "confidence": 0.0,
                "message": "Please enter or speak a command."}

    model = model or get_model()
    probabilities = model.predict_proba([cleaned])[0]
    best_index = probabilities.argmax()
    intent = model.classes_[best_index]
    confidence = float(probabilities[best_index])

    # The threshold avoids confidently acting on unrelated phrases.
    if confidence < 0.22:
        return {"intent": "unknown", "confidence": confidence,
                "message": "I could not identify that command. Try another phrase."}

    return {"intent": str(intent), "confidence": confidence,
            "message": f"Detected intent: {intent.replace('_', ' ')}."}


if __name__ == "__main__":
    model = train_model()
    print(f"Model trained and saved to: {MODEL_FILE}")
    print(f"Training examples: {len(load_training_data()[0])}")
