import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from datetime import datetime
import os

st.set_page_config(page_title="AI IoT Security Monitoring", layout="wide")

st.markdown("<h1 style='text-align:center;color:cyan;'>🔐 AI Powered IoT Security Dashboard</h1>", unsafe_allow_html=True)

# Load model
model = pickle.load(open("risk_model.pkl","rb"))
vendor_encoder = pickle.load(open("vendor_encoder.pkl","rb"))

# ================== Sidebar ==================
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select", ["Network Scanner", "Honeypot Monitor", "Anomaly Analysis", "Game Theory", "Report & Helpline"])

# ================== 1. Network Scanner ==================
if page=="Network Scanner":
    st.subheader("📡 Live Device Risk Analysis")

    if st.button("🔍 Scan Network Now"):
        try:
            df = pd.read_csv("training_data.csv")
            st.success("Scan Loaded Successfully")
        except:
            st.warning("No training data found")

        st.write(df)

        fig = px.pie(df, names='risk_label', title="Risk Distribution", color='risk_label')
        st.plotly_chart(fig, use_container_width=True)

# ================== 2. Honeypot ==================
elif page=="Honeypot Monitor":
    st.subheader("🪤 Honeypot Attack Logger")

    if os.path.exists("honeypot_logs.csv"):
        logs = pd.read_csv("honeypot_logs.csv")
        st.write(logs)
    else:
        st.warning("No attacks detected yet. Honeypot waiting...")

# ================== 3. Anomaly Analysis ==================
elif page=="Anomaly Analysis":
    st.subheader("📊 Anomaly Detection Results")

    if os.path.exists("anomaly_report.csv"):
        rep = pd.read_csv("anomaly_report.csv")
        st.dataframe(rep)
        fig = px.bar(rep, x="IP", y="Hits", title="Suspicious IP Activity")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Run anomaly_detection.py first!")

# ================== 4. Game Theory ==================
elif page=="Game Theory":
    st.subheader("🎮 Defender vs Attacker Battle Simulation")

    if st.button("Run Simulation"):
        import game_theory
        st.success("Simulation Completed — See Terminal Output!")
        st.info("Visual integration coming next 🔥")

# ================== 5. Reporting & Helpline ==================
elif page=="Report & Helpline":
    st.subheader("☎ Cyber Crime Reporting")

    st.write("""
    If you notice a suspicious IP or repeated attack, you can report to:
    - **India** → https://cybercrime.gov.in
    - **USA** → https://www.ic3.gov
    - **Global CERT List** → https://www.first.org/members/teams
    """)

    ip = st.text_input("Enter attacker IP to lookup approx location")

    if st.button("Trace IP"):
        st.info("Feature coming — will integrate IP location API here 🌍")
