# HandEcho managed deployment outcomes

## Permanent managed website

- The existing HandEcho Flutter client is deployed as the website's static output.
- The existing FastAPI/Python service runs from a production container and serves the saved model and supplied CSV dataset.
- The public deployment uses same-origin browser requests so the frontend does not depend on a temporary Sandbox URL.
- Unauthenticated `/health`, `/dataset/*`, and `/predict` requests route to the server; the remaining website paths route to the Flutter bundle.

## Product behavior preserved

- Home, Live Translator, Technology, Cybersecurity, and Hardware Integration views remain available.
- CSV records, model predictions, simulated demonstrations, and future hardware mode remain clearly distinguished.
- Browser speech controls and graceful service-unavailable handling remain available.

## Release validation

- Flutter analysis passes.
- Flutter release build produces `site/index.html` and `site/main.dart.js`.
- FastAPI health, dataset summary, sample filtering, and model prediction checks pass.
- Managed Preview is reachable before the permanent publication request.
