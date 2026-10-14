"""FastAPI bridge for the HandEcho product site and saved model."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "artifacts" / "handecho_model.joblib"
DATASET_PATH = ROOT / "data" / "HandEcho_synthetic_demo_dataset.csv"
FEATURE_COLUMNS = ["thumb", "index", "middle", "ring", "little"]

app = FastAPI(title="HandEcho — Wearable Sign Translation API", version="2.0.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SensorReadings(BaseModel):
    thumb: float = Field(ge=0)
    index: float = Field(ge=0)
    middle: float = Field(ge=0)
    ring: float = Field(ge=0)
    little: float = Field(ge=0)


@lru_cache(maxsize=1)
def load_dataset() -> pd.DataFrame:
    if not DATASET_PATH.exists():
        raise RuntimeError(f"Dataset not found: {DATASET_PATH}")
    return pd.read_csv(DATASET_PATH)


@lru_cache(maxsize=1)
def load_bundle() -> dict[str, Any]:
    if not MODEL_PATH.exists():
        raise RuntimeError(f"Model artifact not found: {MODEL_PATH}")
    return joblib.load(MODEL_PATH)


def clean_record(row: pd.Series) -> dict[str, Any]:
    record = row.to_dict()
    return {key: (value.item() if hasattr(value, "item") else value) for key, value in record.items()}


def filtered_dataset(label: str | None, search: str | None, split: str | None) -> pd.DataFrame:
    frame = load_dataset()
    if label:
        frame = frame[frame["label"].astype(str) == label]
    if search:
        needle = search.strip().lower()
        frame = frame[frame["label"].astype(str).str.lower().str.contains(needle, regex=False)]
    if split:
        frame = frame[frame["split"].astype(str) == split]
    return frame


@app.get("/health")
def health() -> dict[str, Any]:
    bundle = load_bundle()
    frame = load_dataset()
    return {
        "status": "ok",
        "model": bundle["model_name"],
        "features": bundle["feature_columns"],
        "dataset_rows": len(frame),
        "labels": int(frame["label"].nunique()),
    }


@app.get("/dataset/summary")
def dataset_summary() -> dict[str, Any]:
    frame = load_dataset()
    return {
        "rows": int(len(frame)),
        "labels": sorted(frame["label"].astype(str).unique().tolist()),
        "label_count": int(frame["label"].nunique()),
        "feature_columns": FEATURE_COLUMNS,
        "all_columns": frame.columns.tolist(),
        "split_counts": {str(k): int(v) for k, v in frame["split"].value_counts().to_dict().items()},
        "label_counts": {str(k): int(v) for k, v in frame["label"].value_counts().sort_index().to_dict().items()},
        "feature_ranges": {
            column: {"min": float(frame[column].min()), "max": float(frame[column].max()), "mean": float(frame[column].mean())}
            for column in FEATURE_COLUMNS
        },
    }


@app.get("/dataset/samples")
def dataset_samples(
    label: str | None = None,
    search: str | None = None,
    split: str | None = None,
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=50, ge=1, le=200),
) -> dict[str, Any]:
    frame = filtered_dataset(label, search, split)
    page = frame.iloc[offset : offset + limit]
    return {
        "total": int(len(frame)),
        "offset": offset,
        "limit": limit,
        "samples": [clean_record(row) for _, row in page.iterrows()],
    }


@app.get("/dataset/sample/{sample_id}")
def dataset_sample(sample_id: str) -> dict[str, Any]:
    frame = load_dataset()
    match = frame[frame["sample_id"].astype(str) == sample_id]
    if match.empty:
        raise HTTPException(status_code=404, detail=f"Sample {sample_id!r} not found")
    return clean_record(match.iloc[0])


@app.post("/predict")
def predict(readings: SensorReadings) -> dict[str, Any]:
    try:
        bundle = load_bundle()
        frame = pd.DataFrame([readings.model_dump()], columns=bundle["feature_columns"])
        model = bundle["model"]
        sign = str(model.predict(frame)[0])
        probabilities = model.predict_proba(frame)[0]
        return {
            "sign": sign,
            "confidence": float(max(probabilities)),
            "model": bundle["model_name"],
            "feature_columns": bundle["feature_columns"],
            "input_source": "manual sensor input",
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
