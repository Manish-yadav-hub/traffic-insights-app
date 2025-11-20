import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------------
# App Configuration
# -----------------------------------------------------------
st.set_page_config(
    page_title="City Mobility & Pollution Insights",
    page_icon="🚦",
    layout="wide"
)

st.title("🚦 City Mobility & Pollution Insights Platform")
st.write("Upload a traffic–pollution dataset to explore insights.")

# -----------------------------------------------------------
# Upload Section
# -----------------------------------------------------------
uploaded_file = st.file_uploader("📤 Upload CSV Dataset", type=["csv"])

# Utility function to check columns safely
def has_columns(df, cols):
    return all(col in df.columns for col in cols)

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.subheader("📌 Raw Dataset Preview")
    st.dataframe(df.head(10))
    st.write("---")

    # -----------------------------------------------------------
    # 1. DATA CLEANING & PREPARATION (CLICKABLE)
    # -----------------------------------------------------------
    with st.expander("🧹 1. Data Cleaning & Preparation — Click to View"):

        st.write("### 🔧 Transformations Applied:")

        # --- 1.1 Datetime cleaning
        if 'datetime' in df.columns:
            st.write("- Converting `datetime` into proper timestamp format")
            df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

        # --- 1.2 Trim string columns
        st.write("- Trimming whitespace from string columns")
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].astype(str).str.strip()

        # --- 1.3 Missing values
        st.write("- Filling missing values (forward + backward fill)")
        df = df.fillna(method='ffill').fillna(method='bfill')

        # --- 1.4 Feature engineering
        if 'datetime' in df.columns:
            st.write("- Extracting `hour`, `day`, `month` from datetime")
            df['hour'] = df['datetime'].dt.hour
            df['day'] = df['datetime'].dt.day_name()
            df['month'] = df['datetime'].dt.month

        st.success("Data Cleaning Completed ✔")
        st.dataframe(df.head())

    st.write("---")

    # -----------------------------------------------------------
    # 2. WORST TIME OF DAY & WORST 5 AREAS (CLICKABLE)
    # -----------------------------------------------------------
    with st.expander("⏱ 2. Worst Time of Day & Worst 5 Areas — Click to View"):

        # --- hourly analysis
        if has_columns(df, ['hour', 'traffic', 'pollution']):
            st.write("### 🔥 Worst Hours Based on Traffic")

            hourly = df.groupby('hour')[['traffic', 'pollution']].mean()
            st.dataframe(hourly.sort_values('traffic', ascending=False).head())

            fig, ax = plt.subplots()
            hourly.plot(kind='bar', ax=ax)
            ax.set_title("Hourly Traffic & Pollution")
            st.pyplot(fig)
        else:
            st.warning("Missing columns: hour / traffic / pollution")

        # --- area analysis
        if has_columns(df, ['area', 'traffic']):
            st.write("### 🚨 Worst 5 Areas by Traffic")

            area_stats = df.groupby('area')[['traffic', 'pollution']].mean()
            worst_areas = area_stats.sort_values(by='traffic', ascending=False).head(5)

            st.dataframe(worst_areas)

            fig2, ax2 = plt.subplots()
            worst_areas.plot(kind='bar', ax=ax2)
            ax2.set_title("Worst 5 Areas")
            st.pyplot(fig2)
        else:
            st.warning("Missing columns: area / traffic / pollution")

    st.write("---")

    # -----------------------------------------------------------
    # 3. WEATHER IMPACT ANALYSIS (CLICKABLE)
    # -----------------------------------------------------------
    with st.expander("🌧 3. Weather Impact Analysis — Click to View"):

        if has_columns(df, ['rain', 'traffic']):
            st.write("### 🌧 Rain vs Traffic")
            fig, ax = plt.subplots()
            ax.scatter(df['rain'], df['traffic'])
            ax.set_xlabel("Rainfall")
            ax.set_ylabel("Traffic")
            st.pyplot(fig)

        if has_columns(df, ['rain', 'pollution']):
            st.write("### 💨 Rain vs Pollution")
            fig, ax = plt.subplots()
            ax.scatter(df['rain'], df['pollution'])
            ax.set_xlabel("Rainfall")
            ax.set_ylabel("Pollution")
            st.pyplot(fig)

        if not has_columns(df, ['rain']):
            st.warning("Missing column: rain")

    st.write("---")

    # -----------------------------------------------------------
    # 4. VISUALIZATION GALLERY (CLICKABLE)
    # -----------------------------------------------------------
    with st.expander("📊 Visualization Gallery (3+ Charts) — Click to View"):

        # --- Chart 1: Traffic vs Pollution
        if has_columns(df, ['traffic', 'pollution']):
            st.write("### 📈 Traffic vs Pollution Trend")
            fig, ax = plt.subplots()
            ax.plot(df['traffic'], label='Traffic')
            ax.plot(df['pollution'], label='Pollution')
            ax.legend()
            st.pyplot(fig)

        # --- Chart 2: Traffic Histogram
        if has_columns(df, ['traffic']):
            st.write("### 📉 Traffic Distribution Histogram")
            fig, ax = plt.subplots()
            df['traffic'].plot(kind='hist', bins=30, ax=ax)
            st.pyplot(fig)

        # --- Chart 3: Area-wise Pollution
        if has_columns(df, ['area', 'pollution']):
            st.write("### 🗺 Area-wise Pollution")
            area_plot = df.groupby('area')['pollution'].mean()

            fig, ax = plt.subplots()
            area_plot.plot(kind='bar', ax=ax)
            st.pyplot(fig)

        # --- Chart 4: Rain Trend
        if has_columns(df, ['rain']):
            st.write("### 🌧 Rainfall Trend")
            fig, ax = plt.subplots()
            ax.plot(df['rain'])
            ax.set_ylabel("Rain")
            st.pyplot(fig)

else:
    st.info("👆 Upload a CSV file to begin analysis.")

