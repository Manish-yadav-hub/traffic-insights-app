import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------------------------------------
# App Title
# -----------------------------------------------------------
st.title("🚦 City Mobility & Pollution Insights Platform")
st.write("Upload a traffic–pollution dataset to explore insights.")

# -----------------------------------------------------------
# Upload Section
# -----------------------------------------------------------
uploaded_file = st.file_uploader("Upload CSV Dataset", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.subheader("📌 Raw Dataset Preview")
    st.dataframe(df.head())

    # -------------------------------------------------------
    # Data Cleaning
    # -------------------------------------------------------
    st.subheader("🧹 Data Cleaning & Preparation")

    # Convert datetime if exists
    if 'datetime' in df.columns:
        df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')

    # Strip spaces in string columns
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].astype(str).str.strip()

    # Fill missing values
    df = df.fillna(method='ffill').fillna(method='bfill')

    st.write("✔ Data cleaned successfully!")

    # -------------------------------------------------------
    # Feature Engineering
    # -------------------------------------------------------
    if 'datetime' in df.columns:
        df['hour'] = df['datetime'].dt.hour
        df['day'] = df['datetime'].dt.day_name()
        df['month'] = df['datetime'].dt.month

    # -------------------------------------------------------
    # Traffic & Pollution Overview
    # -------------------------------------------------------
    if {'traffic', 'pollution'}.issubset(df.columns):
        st.subheader("📈 Traffic & Pollution Overview")

        fig, ax = plt.subplots()
        ax.plot(df['traffic'], label='Traffic')
        ax.plot(df['pollution'], label='Pollution')
        ax.legend()
        st.pyplot(fig)

    # -------------------------------------------------------
    # 1. How do traffic patterns relate to pollution?
    # -------------------------------------------------------
    if {'traffic', 'pollution'}.issubset(df.columns):
        st.subheader("🔍 How Do Traffic Patterns Relate To Pollution?")

        fig, ax = plt.subplots()
        ax.scatter(df['traffic'], df['pollution'])
        ax.set_xlabel("Traffic Level")
        ax.set_ylabel("Pollution Level")
        ax.set_title("Traffic vs Pollution Relationship")
        st.pyplot(fig)

        corr = df['traffic'].corr(df['pollution'])
        st.write(f"📌 Correlation: **{corr:.2f}**")

    # -------------------------------------------------------
    # 2. Does rain reduce traffic but not pollution?
    # -------------------------------------------------------
    if 'rain' in df.columns:
        st.subheader("🌧 Rain Impact Analysis")

        col1, col2 = st.columns(2)

        with col1:
            st.write("📉 Rain vs Traffic")
            fig, ax = plt.subplots()
            ax.scatter(df['rain'], df['traffic'])
            ax.set_xlabel("Rainfall")
            ax.set_ylabel("Traffic")
            st.pyplot(fig)

        with col2:
            st.write("💨 Rain vs Pollution")
            fig, ax = plt.subplots()
            ax.scatter(df['rain'], df['pollution'])
            ax.set_xlabel("Rainfall")
            ax.set_ylabel("Pollution")
            st.pyplot(fig)

    # -------------------------------------------------------
    # 3. Worst Time of the Day & Worst 5 Areas
    # -------------------------------------------------------
    st.subheader("⏱ Worst Time of Day & Worst 5 Areas")

    if 'hour' in df.columns:
        hourly = df.groupby('hour')[['traffic', 'pollution']].mean()
        st.write("### Worst Hours (Sorted by Traffic):")
        st.dataframe(hourly.sort_values('traffic', ascending=False).head())

        fig, ax = plt.subplots()
        hourly.plot(kind='bar', ax=ax)
        ax.set_title("Hourly Traffic & Pollution")
        st.pyplot(fig)

    if 'area' in df.columns:
        area_stats = df.groupby('area')[['traffic', 'pollution']].mean()
        worst_areas = area_stats.sort_values('traffic', ascending=False).head(5)

        st.write("### 🚨 Worst 5 Areas by Traffic")
        st.dataframe(worst_areas)

        fig, ax = plt.subplots()
        worst_areas.plot(kind='bar', ax=ax)
        ax.set_title("Worst Areas (Top 5)")
        st.pyplot(fig)

    # -------------------------------------------------------
    # Transport Mode Classification (If Available)
    # -------------------------------------------------------
    if 'transport_mode' in df.columns:
        st.subheader("🚌 Transport Mode Insights")

        mode_counts = df['transport_mode'].value_counts()

        fig, ax = plt.subplots()
        mode_counts.plot(kind="pie", autopct='%1.1f%%', ax=ax)
        ax.set_ylabel("")
        ax.set_title("Transport Mode Distribution")
        st.pyplot(fig)

    # -------------------------------------------------------
    # Weather Impact Analysis
    # -------------------------------------------------------
    st.subheader("🌦 Weather Impact Analysis")

    if {'rain', 'traffic'}.issubset(df.columns):
        st.write("### Rain vs Traffic Trend")
        fig, ax = plt.subplots()
        ax.plot(df['rain'], label="Rain")
        ax.plot(df['traffic'], label="Traffic")
        ax.legend()
        st.pyplot(fig)

    if {'rain', 'pollution'}.issubset(df.columns):
        st.write("### Rain vs Pollution Trend")
        fig, ax = plt.subplots()
        ax.plot(df['rain'], label="Rain")
        ax.plot(df['pollution'], label="Pollution")
        ax.legend()
        st.pyplot(fig)

else:
    st.info("👆 Upload a CSV file to begin analysis.")
