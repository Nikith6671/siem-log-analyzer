import streamlit as st
import pandas as pd
import time
from db import connect_db
from  auth import authenticate

# ---------------- LOGIN FUNCTION ---------------- #

def login():
    st.title("🔐 SIEM Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        role = authenticate(username, password)

        if role:
            st.session_state["logged_in"] = True
            st.session_state["role"] = role
            st.success("✅ Login successful")
            st.rerun()
        else:
            st.error("❌ Invalid credentials")

# ---------------- FETCH LOGS ---------------- #
from sqlalchemy import create_engine 
def fetch_logs():
    engine = create_engine("postgresql://postgres:6671@localhost:5432/siem_logs")
    query = "SELECT * FROM logs ORDER BY timestamp DESC"
    df = pd.read_sql(query, engine)
    return df

# ---------------- DASHBOARD ---------------- #

def dashboard():
    st.markdown ("""
                 <style>
                 .main {
                     background-color: #0e1117;
                 }
                 h1,h2,h3{
                     color: #00ffcc;
                 }
                 </style>
                 """, unsafe_allow_html=True)    
    st.set_page_config(page_title="SIEM Dashboard", layout="wide")

    role = st.session_state.get("role")

    st.title("🔐 SIEM Security Dashboard")
    st.markdown("Real-time log monitoring & threat detection system")

    # Sidebar
    st.sidebar.header("🔎 Filters")
    st.sidebar.write(f"👤 Role: {role}")

    df = fetch_logs()
    search = st.text_input("🔍 Search Logs")
    if search:
        df = df[df["message"].str.contains(search, case=False)]
        sort_order = st.selectbox("Sort logs", ["Latest First", "Oldest First"])
        if sort_order == "Latest First":
            df = df.sort_values(by="timestamp", ascending=True)

    # Filter by level
    level_filter = st.sidebar.selectbox(
        "Select Log Level",
        ["ALL"] + list(df['level'].unique())
    )

    if level_filter != "ALL":
        df = df[df['level'] == level_filter]

    # Metrics
    st.subheader("📊 Key Metrics")
    col1, col2 = st.columns(2)
    failed_logins = df[df['message'].str.contains("failed", case=False)]
    with col1:
        st.metric("Total Logs", len(df))

    with col2:
        st.metric("Failed Attempts", len(failed_logins))

    # Alerts
    st.subheader("⚠️ Threat Detection")

    if len(failed_logins) > 5:
        st.error(f"⚠️ ALERT: {len(failed_logins)} suspicious activities detected!")
    else:
        st.success("✅ System is normal")

    # Role-based access
    st.subheader("📄 Logs Data")

    if role == "admin":
        st.dataframe(df, width="stretch")
        st.download_button(
            label="Download Logs as CSV",
            data=df.to_csv(index=False),
            file_name="siem_logs.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ Limited access: Only admins can view full logs")

    # Chart
    st.subheader("📊 Log Level Distribution")
    log_counts = df['level'].value_counts()
    st.bar_chart(log_counts)

    # Top threats
    st.subheader("🚨 Top Threats")
    threats = df[df['level'] == 'WARNING']['message'].value_counts()
    st.table(threats)

    # Logout
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["role"] = None
        st.rerun()

    # Auto refresh
    st.caption("🔄 Auto-refresh every 10 seconds")
    time.sleep(10)
    st.rerun()

# ---------------- MAIN ---------------- #

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if st.session_state["logged_in"]:
    dashboard()
else:
    login()