import streamlit as st

st.set_page_config(
    page_title="Digital Twin Project Homepage",
    page_icon="🚗",
    layout="wide"
)

# --- HEADER SECTION ---
st.title("The 'Smart Tire' Digital Twin: An Industry 4.0 Project")
st.subheader("Project by: [Your Name Here]") # <-- ADD YOUR NAME
st.markdown("---")

# --- PROJECT INTRODUCTION ---
st.header("1. The Problem: Unplanned Vehicle Downtime")
st.image("https://images.unsplash.com/photo-1579583764841-3818d10b70d7?w=1200", 
         caption="Unplanned tire failures are a major cost and safety risk for automotive fleets.",
         use_column_width=True)
st.write("""
In the logistics, mining, and automotive industries, vehicle downtime is the enemy. A single truck or piece of heavy machinery
sidelined by an unexpected tire failure can cost thousands of dollars per hour in lost productivity and create significant safety hazards.
Traditional maintenance is reactive (fixing after failure) or preventative (replacing at fixed intervals), which is inefficient and costly.
""")

st.header("2. The Industry 4.0 Solution: A Predictive Digital Twin")
st.write("""
This project demonstrates an **Industry 4.0** solution by creating a **Digital Twin** of a 'Smart Tire'. 
This is not just a 3D model; it's a living, data-driven simulation that:
* **Monitors** real-time (simulated) IoT data from sensors for pressure, temperature, and vibration.
* **Analyzes** this data using a Machine Learning model to detect subtle patterns that precede a failure.
* **Predicts** not just *if* a failure is likely, but *what kind* of failure is developing (e.g., Pressure Loss vs. Overheating).
* **Prescribes** a specific maintenance action, moving the team from reactive to predictive maintenance.
""")

# --- TECHNOLOGY STACK ---
st.header("3. Technology Stack")
st.markdown("""
-   **Data:** Synthetic sensor data generated with `Pandas` & `Numpy`.
-   **Machine Learning:** `Scikit-learn` (Random Forest Classifier) to predict multi-class failure modes.
-   **Dashboard:** `Streamlit` for the interactive web UI.
-   **Visualizations:** `Plotly` for interactive 2D charts.
-   **3D Model:** `streamlit-3d-viewer` to render a live 3D model of the tire.
-   **Deployment:** `Streamlit Cloud` integrated directly with this `GitHub` repository.
""")

# --- CALL TO ACTION ---
st.markdown("---")
st.success("### 🚀 Click 'Digital Twin Dashboard' in the sidebar to launch the application!")
