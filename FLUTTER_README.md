# HandEcho — Simulated Dataset Dashboard

This is a real Flutter web client for the HandEcho prototype. It keeps prediction in the existing Python model and uses a small FastAPI bridge; the UI does not hardcode sign predictions.

## Prerequisites

- Flutter stable SDK 3.3+
- Python 3.10+
- Existing trained artifact: `artifacts/handecho_model.joblib`

## Start the prediction API

From `/home/ubuntu/HandEcho`:

```bash
python3 -m uvicorn api:app --host 0.0.0.0 --port 8000
```

Check it:

```bash
curl http://localhost:8000/health
```

## Run Flutter in development

In a second terminal:

```bash
cd /home/ubuntu/HandEcho/flutter_app
flutter pub get
flutter run -d web-server --web-port 8080 \\
  --dart-define=API_BASE_URL=http://localhost:8000
```

Open `http://localhost:8080`.

## Build and serve the production web bundle

```bash
cd /home/ubuntu/HandEcho/flutter_app
flutter pub get
flutter build web --release \\
  --dart-define=API_BASE_URL=http://localhost:8000
python3 -m http.server 8080 -d build/web --bind 0.0.0.0
```

The **Audio output** switch uses the browser's native speech synthesis. Enable it after a prediction and choose **Play sign**, or leave it enabled to speak automatically after the next prediction.

## UI direction

The interface uses a restrained product-dashboard aesthetic: deep navy for trust and structure, a teal signature accent for the sensing/translation loop, warm coral only for attention states, generous whitespace, and a responsive two-column-to-stacked layout. It presents model confidence as a dashboard signal and keeps the review context visible.


## Product site sections

- **Home:** system purpose, product positioning, and the five-stage flow.
- **Live Translator:** dataset-driven label search, sample navigation, actual sensor readings, animated reading bars, model prediction, manual input, and audio output.
- **Technology:** glove sensors → preprocessing → ML model → translated text → speech.
- **Cybersecurity:** communication, data minimization, validation, and logging considerations.
- **Hardware Integration:** an explicit not-connected boundary plus the future REST/WebSocket feature contract.

The API exposes:

- `GET /dataset/summary` — dataset dimensions, labels, columns, split counts, and feature ranges.
- `GET /dataset/samples?label=<label>&limit=<n>` — actual CSV records with pagination support.
- `GET /dataset/sample/<sample_id>` — one exact record.
- `POST /predict` — sends five values to the saved model when available.

The dashboard uses the CSV records as returned by the API. Simulated demonstrations are labeled as such, while CSV readings and model predictions are shown as separate outputs.
