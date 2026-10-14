FROM python:3.11-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements-web.txt ./
RUN pip install --no-cache-dir -r requirements-web.txt

COPY api.py server.py ./
COPY artifacts/handecho_model.joblib ./artifacts/handecho_model.joblib
COPY data/HandEcho_synthetic_demo_dataset.csv ./data/HandEcho_synthetic_demo_dataset.csv
COPY site ./site

EXPOSE 3000
CMD ["sh", "-c", "exec uvicorn server:app --host 0.0.0.0 --port ${PORT:-3000}"]
