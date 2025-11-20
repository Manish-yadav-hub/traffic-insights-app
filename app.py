import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Traffic & Pollution Insights", layout="wide")

st.title("🚦 Traffic • Weather • Pollution Insights App")

st.write("Upload the traffic dataset to begin.")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.success("Dataset successfully loaded!")

    # ---------------------------------------------------------------------
    # SECTION 1 – DATA CLEANING (Expandable)
    # ---------------------------------------------------------------------
    with st.expander("🧹 1. Data Cleaning & Preparation (Click to View)"):
        st.write("### ➤ Raw Data")
        st.dataframe(df.head())

        # -------------------- CLEANING --------------------
        cleaning_steps = []

        # Convert timestamp
        if "timestamp" in df.columns:
            df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
            cleaning_steps.append("Converted 'timestamp' to datetime")

        # Strip strings
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].astype(str).str.strip()
            cleaning_steps.append(f"Cleaned extra spaces in column '{col}'")

        # Remove duplicates
        before = len(df)
        df = df.drop_duplicates()
        after = len(df)
        cleaning_steps.append(f"Removed {before-after} duplicate rows")

        # Final data view
        st.write("### ➤ Cleaning Steps Applied")
        for step in cleaning_steps:
            st.write("✔", step)

        st.write("### ➤ Cleaned Dataset Preview")
        st.dataframe(df.head())

    # ---------------------------------------------------------------------
    # SECTION 2 – WORST TIME OF DAY & TOP 5 WORST AREAS
    # ---------------------------------------------------------------------
    with st.expander("⏰ 2. Worst Time of Day & Worst 5 Areas"):
        if "timestamp" in df.columns and "severity" in df.columns:
            df["hour"] = df["timestamp"].dt.hour

            worst_time = df.groupby("hour")["severity"].mean().sort_values(ascending=False)
            st.write("### ⏱ Worst Hours of the Day (By Severity)")
            st.bar_chart(worst_time)

        else:
            st.warning("Missing 'timestamp' or 'severity' column.")

        if "area" in df.columns and "severity" in df.columns:
            worst_areas = df.groupby("area")["severity"].mean().nlargest(5)
            st.write("### 🛑 Worst 5 Areas (By Severity)")
            st.bar_chart(worst_areas)
        else:
            st.warning("Missing 'area' or 'severity' column.")

    # ---------------------------------------------------------------------
    # SECTION 3 – WEATHER IMPACT ANALYSIS
    # ---------------------------------------------------------------------
    with st.expander("🌧 3. Weather Impact Analysis"):
        if "weather" in df.columns and "severity" in df.columns:
            st.write("### 📊 Severity by Weather Type")
            weather_impact = df.groupby("weather")["severity"].mean().sort_values(ascending=False)
            st.bar_chart(weather_impact)
        else:
            st.warning("Missing 'weather' or 'severity' column.")

    # ---------------------------------------------------------------------
    # SECTION 4 – VISUALIZATION GALLERY (3 REQUIRED PLOTS)
    # ---------------------------------------------------------------------
    with st.expander("📈 Visualization Gallery (3 Required Charts)"):

        # 1. Timestamp vs Speed
        st.write("### 1️⃣ Timestamp vs Speed (speed_kmph)")
        if "timestamp" in df.columns and "speed_kmph" in df.columns:
            fig, ax = plt.subplots()
            ax.plot(df["timestamp"], df["speed_kmph"])
            ax.set_xlabel("Timestamp")
            ax.set_ylabel("Speed (kmph)")
            st.pyplot(fig)
        else:
            st.warning("Missing 'timestamp' or 'speed_kmph'.")

        # 2. Weather vs Incident Type
        st.write("### 2️⃣ Weather vs Incident Type")
        if "weather" in df.columns and "incident_type" in df.columns:
            incident = df.groupby("weather")["incident_type"].count()

            fig, ax = plt.subplots()
            incident.plot(kind="bar", ax=ax)
            ax.set_ylabel("Incident Count")
            st.pyplot(fig)
        else:
            st.warning("Missing 'weather' or 'incident_type'.")

        # 3. Travel Delay vs Road Type
        st.write("### 3️⃣ Travel Delay vs Road Type")
        if "travel_delay_minutes" in df.columns and "road_type" in df.columns:
            delay_plot = df.groupby("road_type")["travel_delay_minutes"].mean()

            fig, ax = plt.subplots()
            delay_plot.plot(kind="bar", ax=ax)
            ax.set_ylabel("Avg Travel Delay (minutes)")
            st.pyplot(fig)
        else:
            st.warning("Missing 'travel_delay_minutes' or 'road_type'.")

else:
    st.info("Please upload a CSV file to start analysis.")
