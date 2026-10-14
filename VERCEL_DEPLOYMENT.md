# HandEcho deployment on Vercel

This repository contains the complete HandEcho prototype: the Flutter web client, FastAPI model API, trained Random Forest artifact, supplied CSV dataset, training/evaluation code, and local/managed hosting configuration.

## Recommended setup: one GitHub repository and one Vercel project

The simplest deployment is now a **single Vercel project connected to this one GitHub repository**. The root `vercel.json` combines both parts:

- `site/` is served as the Flutter static frontend.
- `api/index.py` runs the FastAPI backend as a Vercel Python function.
- `/health`, `/predict`, and `/dataset/*` are routed to FastAPI.
- All other paths are routed to the Flutter bundle.

Because the frontend and backend share one origin, the Flutter client uses its default same-origin API configuration. No `API_BASE_URL` setting is required.

### Deploy from GitHub

1. Upload this complete project to a GitHub repository.
2. In Vercel, choose **Add New Project** and import that GitHub repository.
3. Leave the Vercel **Root Directory** set to the repository root.
4. Keep the default build settings; the committed `vercel.json` controls the frontend/backend routing.
5. Click **Deploy**.

After deployment, verify:

```bash
curl https://YOUR-PROJECT.vercel.app/health
```

The response should report the Random Forest model, five sensor features, 3,400 dataset rows, and 34 labels. Open `https://YOUR-PROJECT.vercel.app` to use the website.

### Important Vercel limits

The saved model and dataset are included exactly as requested. The backend also installs pandas, NumPy, scikit-learn, joblib, FastAPI, and Pydantic. Vercel Python functions have platform size and execution limits. If Vercel rejects the dependency bundle or function size, use the unchanged `Dockerfile` to host the API on Render, Railway, Fly.io, or a managed VM, and set `API_BASE_URL` when rebuilding the Flutter bundle. That is a fallback only; the repository is configured for the one-project deployment first.

## Optional separate-hosting fallback

If separate hosting is required later, deploy the backend with `vercel.backend.json` and deploy the `site/` directory as a static Vercel project. Rebuild the Flutter bundle with:

```bash
cd flutter_app
flutter pub get
flutter build web --release \
  --dart-define=API_BASE_URL=https://YOUR-BACKEND.vercel.app
rm -rf ../site
cp -a build/web ../site
```

The existing FastAPI CORS middleware supports a separately hosted frontend. For a stricter production policy, change `allow_origins=["*"]` in `api.py` to the exact frontend origin after deployment.

## GitHub upload

The downloadable archive is intended to be uploaded as a normal GitHub repository:

```bash
unzip HandEcho-vercel-deployment.zip
cd HandEcho-vercel-deployment

git init
git add .
git commit -m "Package HandEcho for deployment"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```

The archive excludes `.git/`, Flutter dependency caches, Python bytecode, and generated local build caches. It includes the trained model, CSV dataset, evaluation outputs, source code, deployment descriptors, and documentation.

## Other supported workflows

The existing local commands remain unchanged:

```bash
# Streamlit prototype
pip install -r requirements.txt
streamlit run app.py

# FastAPI + Flutter locally
pip install -r requirements-web.txt
python -m uvicorn api:app --reload --port 8000
cd flutter_app
flutter run -d chrome --dart-define=API_BASE_URL=http://localhost:8000
```

The included `Dockerfile` remains available for container deployment and the existing Manus-managed deployment configuration is preserved.
