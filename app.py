import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------------
# App Title + Config
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

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file)

    st.subheader("📌 Raw Dataset Preview")
    st.dataframe(df.head(10))

    st.write("---")

    # -----------------------------------------------------------
    # CLICKABLE EXPANDERS
    # -----------------------------------------------------------

    # -----------------------------------------------------------
    # 1. DATA CLEANING & PREPARATION
    # -----------------------------------------------------------
    with st.expander("🧹 1. Data Cleaning & Preparation (Click to Expand)"):
        
        st.write("### 🔧 Transformation Steps Applied:")

        # Convert datetime
        if 'datetime' in df.columns:
            st.write("- Converting `datetime` to proper timestamps")
            df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

        # Trim strings
        st.write("- Stripping extra spaces in string columns")
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].astype(str).str.strip()
        
        # Missing values
        st.write("- Forward & backward fill missing values")
        df = df.fillna(method='ffill').fillna(method='bfill')

        # Feature Engineering
        st.write("- Extracting `hour`, `day`, and `month` from datetime")
        if 'datetime' in df.columns:
            df['hour'] = df['datetime'].dt.hour
            df['day'] = df['datetime'].dt.day_name()
            df['month'] = df['datetime'].dt.month

        st.success("Data Cleaning Completed")
        st.dataframe(df.head())

    st.write("---")

    # -----------------------------------------------------------
    # 2. Worst Time of Day & Worst 5 Areas
    # -----------------------------------------------------------
    with st.expander("⏱ 2. Worst Time of Day & Worst 5 Areas (Click to Expand)"):

        if 'hour' in df.columns and 'traffic' in df.columns:

            st.write("### 🔥 Worst Hours Based on Traffic")
            hourly = df.groupby('hour')[['traffic', 'pollution']].mean()

            st.dataframe(hourly.sort_values('traffic', ascending=False).head())

            fig, ax = plt.subplots()
            hourly.plot(kind='bar', ax=ax)
            ax.set_title("Hourly Traffic & Pollution")
            st.pyplot(fig)

        if 'area' in df.columns:

            st.write("### 🚨 Worst 5 Areas by Traffic & Pollution")
            area_stats = df.groupby('area')[['traffic', 'pollution']].mean()
            worst_areas = area_stats.sort_values(by='traffic', ascending=False).head(5)

            st.dataframe(worst_areas)

            fig2, ax2 = plt.subplots()
            worst_areas.plot(kind='bar', ax=ax2)
            ax2.set_title("Worst 5 Areas Based on Traffic")
            st.pyplot(fig2)

    st.write("---")

    # -----------------------------------------------------------
    # 3. WEATHER IMPACT ANALYSIS
    # -----------------------------------------------------------
    with st.expander("🌧 3. Weather Impact Analysis (Click to Expand)"):

        if 'rain' in df.columns:

            col1, col2 = st.columns(2)

            with col1:
                st.write("### 🌧 Rain vs Traffic")
                fig, ax = plt.subplots()
                ax.scatter(df['rain'], df['traffic'])
                ax.set_xlabel("Rainfall")
                ax.set_ylabel("Traffic")
                st.pyplot(fig)

            with col2:
                st.write("### 🌧 Rain vs Pollution")
                fig, ax = plt.subplots()
                ax.scatter(df['rain'], df['pollution'])
                ax.set_xlabel("Rainfall")
                ax.set_ylabel("Pollution")
                st.pyplot(fig)

    st.write("---")

    # -----------------------------------------------------------
    # EXTRA: VISUALIZATION GALLERY (3+ Charts)
    # -----------------------------------------------------------
    with st.expander("📊 Visualization Gallery (3+ Charts) – Click to View"):

        st.write("### 📈 Overview of Traffic vs Pollution Over Time")

        if {'traffic','pollution'}.issubset(df.columns):
            fig, ax = plt.subplots()
            ax.plot(df['traffic'], label='Traffic')
            ax.plot(df['pollution'], label='Pollution')
            ax.legend()
            st.pyplot(fig)

        st.write("### 📉 Traffic Distribution")
        fig, ax = plt.subplots()
        df['traffic'].plot(kind='hist', bins=30, ax=ax)
        st.pyplot(fig)

        st.write("### 🗺 Area-wise Pollution Levels")
        if 'area' in df.columns:
            area_plot = df.groupby('area')['pollution'].mean()

            fig, ax = plt.subplots()
            area_plot.plot(kind='bar', ax=ax)
            st.pyplot(fig)

    st.write("---")

    st.success("App Loaded Successfully ✔")
else:
    st.info("👆 Upload a CSV file to begin analysis.")



