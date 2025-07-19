import streamlit as st
import pandas as pd
import numpy as np

# ---------------- Load Dataset ----------------
df = pd.read_csv("SP 500 ESG Risk Ratings.csv")
df.columns = [col.strip() for col in df.columns]

df.rename(columns={
    'Total ESG Risk score': 'Total_ESG',
    'Environment Risk Score': 'Environment',
    'Social Risk Score': 'Social',
    'Governance Risk Score': 'Governance',
    'Controversy Score': 'Controversy',
    'ESG Risk Level': 'Normal_Risk',
    'Controversy Level': 'Controversy_Level',
    'Sector': 'Sector',
}, inplace=True)

df = df.dropna(subset=["Total_ESG", "Environment", "Governance", "Social", "Controversy", "Normal_Risk", "Controversy_Level"])

for col in ["Total_ESG", "Environment", "Governance", "Social", "Controversy"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ---------------- Streamlit App ----------------

st.set_page_config(page_title="Investment & Fraud Risk Predictor", layout="wide")
st.title("📈 Investment & Fraud Risk Predictor using ESG Metrics")

st.markdown("Input the **Environment**, **Social**, **Governance** and **Controversy Score** to get an ESG risk level, fraud prediction, and investment recommendation.")

# --------- User Inputs ----------
env_input = st.slider("🌍 Environment Risk Score", 0.0, 50.0, 15.0)
soc_input = st.slider("🧑‍🤝‍🧑 Social Risk Score", 0.0, 50.0, 12.0)
gov_input = st.slider("🏛️ Governance Risk Score", 0.0, 50.0, 10.0)
contro_input = st.slider("⚠️ Controversy Score", 0.0, 5.0, 1.0)

submit = st.button("🚀 Predict")

if submit:
    # -------- Risk Score ------------
    total_score = env_input + soc_input + gov_input

    # Risk Level
    if total_score < 10:
        risk_level = "Negligible"
    elif total_score < 20:
        risk_level = "Low"
    elif total_score < 30:
        risk_level = "Medium"
    elif total_score < 40:
        risk_level = "High"
    else:
        risk_level = "Severe"

    # -------- Controversy Level & Fraud Chance --------
    if contro_input <= 1:
        contro_level = "Low"
        fraud_chance = "🟢 Very Low"
    elif contro_input <= 2:
        contro_level = "Moderate"
        fraud_chance = "🟡 Moderate"
    elif contro_input <= 3:
        contro_level = "Elevated"
        fraud_chance = "🟠 High"
    elif contro_input <= 4:
        contro_level = "High"
        fraud_chance = "🔴 Very High"
    else:
        contro_level = "Severe"
        fraud_chance = "🔴 Extremely High"

    # -------- Investment Advice --------
    if risk_level in ["Negligible", "Low"] and contro_level in ["Low", "Moderate"]:
        recommendation = "🟢 **Strong Buy** — Excellent ESG profile and low fraud risk."
    elif risk_level == "Medium" and contro_level in ["Low", "Moderate"]:
        recommendation = "🟡 **Hold / Moderate Buy** — Medium sustainability risk, but manageable fraud risk."
    elif risk_level in ["High", "Severe"] or contro_level in ["Elevated", "High"]:
        recommendation = "🔴 **Avoid** — Elevated risk due to poor ESG or controversy signals."
    else:
        recommendation = "🔴 **High Risk Investment** — ESG or controversy scores indicate high exposure."

    # -------- Output Display --------
    st.markdown("## 📊 Risk Analysis Results")
    st.write(f"**Total ESG Risk Score**: {total_score:.2f}")
    st.write(f"**Normal Risk Level**: {risk_level}")
    st.write(f"**Controversy Level**: {contro_level}")
    st.write(f"**Predicted Fraud Risk**: {fraud_chance}")
    st.markdown("---")

    st.markdown("## 💼 Investment Recommendation")
    st.success(recommendation)

    # -------- Chart ------------
    avg_env = df["Environment"].mean()
    avg_soc = df["Social"].mean()
    avg_gov = df["Governance"].mean()

    chart_data = pd.DataFrame({
        "Metric": ["Environment", "Social", "Governance"],
        "User Input": [env_input, soc_input, gov_input],
        "S&P 500 Avg": [avg_env, avg_soc, avg_gov]
    })

    st.markdown("## 📉 Comparison to S&P 500 Averages")
    st.bar_chart(chart_data.set_index("Metric"))
