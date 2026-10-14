"""Simple Streamlit interface for the saved HandEcho model."""
from pathlib import Path

import joblib
import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parent
MODEL_PATH = ROOT / "artifacts" / "handecho_model.joblib"

st.set_page_config(page_title="HandEcho — Simulated Dataset Dashboard", page_icon="✋", layout="centered")
st.title("HandEcho — Simulated Dataset Dashboard")
st.warning(
    "Preliminary software dashboard for review. Physical sensor integration is planned for a later phase."
)

if not MODEL_PATH.exists():
    st.error("No trained model found. Run `python src/train.py` from the project directory first.")
    st.stop()

bundle = joblib.load(MODEL_PATH)
model = bundle["model"]
features = bundle["feature_columns"]

st.sidebar.header("Simulated sensor readings")
st.sidebar.caption("Enter one reading for each finger sensor.")
values = {
    feature: st.sidebar.number_input(feature.capitalize(), min_value=0.0, value=2000.0, step=1.0)
    for feature in features
}

sensor_frame = pd.DataFrame([values], columns=features)
st.subheader("Input readings")
st.dataframe(sensor_frame, hide_index=True, use_container_width=True)

if st.button("Predict sign", type="primary", use_container_width=True):
    prediction = model.predict(sensor_frame)[0]
    st.success(f"Predicted sign: **{prediction}**")
    if hasattr(model, "predict_proba"):
        probability = float(model.predict_proba(sensor_frame).max())
        st.caption(f"Model-estimated class probability: {probability:.1%}.")

st.divider()
st.caption(f"Deployment model: {bundle['model_name']} | Features: {', '.join(features)}")
st.caption("Physical hardware integration and real sensor data collection are future work.")
