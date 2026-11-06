# Voice Command Intent Classifier

A beginner-friendly Natural Language Processing (NLP) project that classifies a spoken or typed command into an intent such as `greeting`, `play_music`, or `set_reminder`.

The project includes a Flask web application, a machine-learning text classifier, a small editable training dataset, and browser-based speech recognition.

## Features

- Classifies typed commands using TF-IDF and Logistic Regression.
- Captures voice input through the browser's Web Speech API (where supported).
- Displays the predicted intent and model confidence.
- Includes example commands for quick testing.
- Uses an `unknown` fallback when confidence is low.
- Automatically trains the model the first time the app runs.

## Project structure

```text
voice-command-intent-classifier/
├── app.py
├── classifier.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   └── intents.json
├── templates/
│   └── index.html
└── static/
    ├── app.js
    └── style.css
```

The trained model is generated in the `model/` directory when the application starts. It is not required in Git because it can be recreated from the dataset.

## Requirements

- Python 3.10 or newer
- A modern browser
- Internet connection may be required by the browser for speech recognition

## Run locally

1. Extract this project ZIP and open a terminal in the project folder.
2. Create a virtual environment:

   **Windows**
   ```bash
   python -m venv .venv
   .venv\\Scripts\\activate
   ```

   **macOS / Linux**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Start the web application:

   ```bash
   python app.py
   ```

5. Open **http://127.0.0.1:5000** in your browser. Allow microphone access if you want to use voice input.

## Train the model manually

```bash
python classifier.py
```

This creates `model/intent_classifier.joblib`.

## Add or change intents

Edit `data/intents.json`. Each key is an intent label and its value is a list of example phrases. Add several varied examples for every new intent, then delete the `model/` folder or run `python classifier.py` to retrain.

Example:

```json
{
  "greeting": ["hello", "good morning"],
  "play_music": ["play music", "start a song"]
}
```

## API

### `POST /predict`

Request:

```json
{
  "text": "Please play some music"
}
```

Example response:

```json
{
  "intent": "play_music",
  "confidence": 0.74,
  "message": "Detected intent: play music."
}
```

The confidence value is a model probability, not a guarantee that the prediction is correct.

### `GET /health`

Returns a simple application health status.

## How it works

1. **Voice input:** The browser converts speech into text using its Web Speech API. Typed text can also be used.
2. **Preprocessing and features:** TF-IDF converts the command into numerical features using word and two-word phrase patterns.
3. **Classification:** Logistic Regression predicts the most likely intent.
4. **Confidence check:** Low-confidence predictions are returned as `unknown`.
5. **Result:** The web page displays the predicted intent and confidence.

## Limitations

- This is an educational prototype trained on a small dataset. Add more real-world examples to improve generalization.
- Browser speech recognition support varies. The typed-command feature works even when microphone recognition is unavailable.
- The classifier identifies intent only; it does not actually open apps, set reminders, or control music.
- The current speech recognition language is set to English (India) in `static/app.js`; change `recognition.lang` to suit your needs.

## Suggested future improvements

- Expand the dataset with more speakers, accents, and paraphrases.
- Add multilingual intent examples.
- Evaluate the model using a held-out test set and a confusion matrix.
- Connect selected intents to real actions with appropriate user confirmation.
- Add user authentication and deployment configuration before exposing the app publicly.

## License

MIT License. You may use, modify, and distribute this project.
