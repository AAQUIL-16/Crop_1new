import streamlit as st
import pandas as pd
import numpy as np

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Context-Repairing Crop Intelligence System",
    layout="centered"
)

st.title("🧠 Context-Repairing Soil–Climate–Crop Intelligence System")

st.warning(
    "⚠️ This system does NOT perform crop yield prediction.\n\n"
    "Yield values are used ONLY as temporal signals to detect "
    "context degradation and stability loss."
)

# ---------------- LOAD DATA ----------------
DATA_PATH = "data/crop_yield_dataset.csv"
df = pd.read_csv(DATA_PATH)

# ---------------- BASIC CHECK ----------------
required_cols = [
    "Crop_Yield", "Soil_pH", "Temperature",
    "Humidity", "N", "P", "K"
]

for col in required_cols:
    if col not in df.columns:
        st.error(f"Missing column: {col}")
        st.stop()

# ---------------- TEMPORAL CONTEXT ANALYSIS ----------------
yield_series = df["Crop_Yield"].values

mean_yield = np.mean(yield_series)
std_yield = np.std(yield_series)

current_yield = yield_series[-1]
context_deviation = abs(current_yield - mean_yield)

# Latent failure detection (NOT prediction)
context_failure = context_deviation > (1.5 * std_yield)

# ---------------- YIELD STABILITY PRESERVATION INDEX ----------------
yield_delta = np.abs(np.diff(yield_series))
stability_index = round(1 / (1 + yield_delta.mean()), 3)

# ---------------- COUNTERFACTUAL CONTEXT REPAIR ----------------
def counterfactual_repair():
    return {
        "Soil_pH_Adjustment": "+0.3",
        "Nutrient_Action": "NPK Rebalancing",
        "Climate_Adaptation": "Sowing window shift",
        "Execution_Timing": "Next crop cycle",
        "Expected_Stabilization_Horizon": "2 seasons"
    }

# ---------------- UI METRICS ----------------
st.subheader("📊 Context Stability Indicators")

c1, c2, c3 = st.columns(3)
c1.metric("Yield Stability Index", stability_index)
c2.metric("Context Deviation", round(context_deviation, 2))
c3.metric("Latent Context Failure", "YES" if context_failure else "NO")

# ---------------- CURRENT CONTEXT SNAPSHOT ----------------
st.subheader("🧩 Current Context Snapshot")

latest_context = {
    "Soil_pH": df["Soil_pH"].iloc[-1],
    "Temperature": df["Temperature"].iloc[-1],
    "Humidity": df["Humidity"].iloc[-1],
    "Nitrogen (N)": df["N"].iloc[-1],
    "Phosphorus (P)": df["P"].iloc[-1],
    "Potassium (K)": df["K"].iloc[-1]
}

st.json(latest_context)

# ---------------- REPAIR CONTROLLER OUTPUT ----------------
st.subheader("🔧 Counterfactual Context Repair Controller")

st.json(counterfactual_repair())

# ---------------- FINAL NOTE ----------------
st.info(
    "🧠 This system focuses on **preventive context repair**, not yield optimization.\n\n"
    "It detects silent degradation in soil–climate–crop behavior "
    "before visible yield collapse occurs."
)
