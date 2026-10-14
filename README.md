

## Vercel and GitHub packaging

The repository includes a deployment guide at [`VERCEL_DEPLOYMENT.md`](VERCEL_DEPLOYMENT.md). The primary setup is one GitHub repository and one Vercel project: `site/` is the Flutter frontend and `api/index.py` is the FastAPI serverless backend, routed together by the root `vercel.json`. A separate-hosting fallback is also documented if Vercel's Python function limits require it.

The package includes the saved model, supplied CSV dataset, training artifacts, backend source, Flutter source, built frontend bundle, dependency manifests, Docker configuration, and deployment metadata. Existing local, Streamlit, Docker, and Manus workflows are unchanged.
