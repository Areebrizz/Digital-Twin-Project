import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
import random

# --- CONFIGURATION & FUTURISTIC CSS (Must be repeated for the page to inherit styling) ---
st.set_page_config(
    page_title="Digital Twin Predictive Dashboard",
    page_icon="📈",
    layout="wide"
)

# Custom CSS for Futuristic Dark Theme (Deep Charcoal Black and Cyan Glow)
st.markdown("""
<style>
/* Base Dark Theme (Deep Charcoal Black) */
.main {
    background-color: #0d1117; 
    color: #f0f6fc;
}

/* Header & Title Glow (Cyan/Green Accent) */
h1, h2, h3 {
    color: #4CAF50; 
    text-shadow: 0 0 5px #00FFFF, 0 0 10px #00FFFF, 0 0 15px #00FFFF;
}

/* Metric Boxes and Containers */
.stMetric {
    background-color: #161b22;
    padding: 15px;
    border-radius: 10px;
    border-left: 5px solid #00FFFF; 
    box-shadow: 0 4px 20px rgba(0, 255, 255, 0.3); 
    transition: all 0.3s;
}
.stDataFrame {
    color: #f0f6fc;
    background-color: #161b22;
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)


# --- 2. PREDICTIVE LOGIC (Adapted from Colab) ---

# Define the alert thresholds for the wear model
WEAR_THRESHOLD_PRESSURE = 28.0 
HIGH_MILEAGE_THRESHOLD = 40000.0
CRITICAL_TEMP_THRESHOLD = 80.0

def predict_wear_and_status(pressure, mileage, temp):
    """
    Predicts the tire status based on Colab's logic and returns a status string and color.
    """
    if pressure < WEAR_THRESHOLD_PRESSURE and mileage > 10000:
        return "CRITICAL: PRESSURE & WEAR", "red"
    elif pressure < WEAR_THRESHOLD_PRESSURE:
        return "HIGH RISK: LOW PRESSURE", "orange"
    elif mileage > HIGH_MILEAGE_THRESHOLD:
        return "HIGH RISK: HIGH MILEAGE", "orange"
    elif temp > CRITICAL_TEMP_THRESHOLD:
        return "WARNING: HIGH TEMPERATURE", "yellow"
    else:
        return "NORMAL OPERATION", "green"

# --- 3. DATA GENERATION (Used for Plotting Historical Trend) ---
@st.cache_data
def generate_simulation_data():
    data = []
    pressure_start = 32
    temp_start = 25
    mileage_start = 0
    
    # Simulate a full lifetime of 100 cycles 
    for i in range(100): 
        pressure_start -= random.uniform(0.1, 0.3)
        temp_start += random.uniform(-1, 3)
        mileage_start += random.uniform(300, 800)
        data.append((mileage_start, pressure_start, temp_start))
        if pressure_start < WEAR_THRESHOLD_PRESSURE:
             break # Simulation ends when tire fails

    df = pd.DataFrame(data, columns=['Mileage (km)', 'Pressure (PSI)', 'Temperature (°C)'])
    return df

df_sim = generate_simulation_data()


# --- 4. STREAMLIT APP LAYOUT ---

st.title("Digital Twin Predictive Dashboard")
st.markdown("### Real-Time Condition Monitoring & Failure Prediction")
st.markdown("---")

# --- SIDEBAR (Live Simulator) ---
st.sidebar.header("ASSET SIMULATOR (IoT Data Feed)")
st.sidebar.markdown("Manipulate the parameters to test the predictive boundaries of the Digital Twin.")

# Sliders for user input
sim_mileage = st.sidebar.slider("Mileage (km)", 0, 50000, 20000)
sim_pressure = st.sidebar.slider("Pressure (PSI)", 20.0, 45.0, 31.5, 0.1)
sim_temp = st.sidebar.slider("Temperature (°C)", 20.0, 100.0, 55.0, 0.5)

# --- PREDICTION ---
status_text, status_color = predict_wear_and_status(sim_pressure, sim_mileage, sim_temp)


# --- DASHBOARD (Main Page) ---
tab1, tab2 = st.tabs(["3D Digital Twin & Prescriptive Alert", "Long-Term Simulation & Diagnostics"])

# --- TAB 1: 3D DIGITAL TWIN & ALERT ---
with tab1:
    
    col_3d, col_status = st.columns([2, 1])
    
    with col_3d:
        st.subheader(f"Interactive 3D Twin: Current State [{status_text}]")
        st.caption("This visualization reflects the health status determined by the predictive model.")
        
        # Determine the color and intensity for the 3D model based on status
        # This color needs to be injected into the HTML tag
        # Red/Orange/Yellow indicates danger, Green indicates safety
        
        if status_color == "green":
            twin_color = "#4CAF50" # Green for Normal
        elif status_color == "orange":
            twin_color = "#FFD700" # Gold/Yellow-Orange for High Risk
        elif status_color == "yellow":
            twin_color = "#FFA500" # Orange for Warning
        else: # Critical
            twin_color = "#FF0000" # Red for Critical

        # IMPORTANT: This is the native HTML 3D viewer for high compatibility.
        # Ensure 'offorad_vehicle_tires.glb' is in your repository root.
        model_path = "https://cdn.jsdelivr.net/gh/google/model-viewer/examples/assets/RobotExpressive.glb" # Placeholder link
        
        # To use your uploaded GLB, you need to commit it to your GitHub repo
        # and reference it directly, e.g., model_path = "https://raw.githubusercontent.com/YOUR_USER/YOUR_REPO/main/offorad_vehicle_tires.glb"

        html_code = f"""
        <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.5.0/model-viewer.min.js"></script>
        <model-viewer 
            src="{model_path}" 
            alt="Digital Twin Tire Model"
            auto-rotate 
            camera-controls 
            ar
            style="width: 100%; height: 550px; border-radius: 15px; background-color: #0d1117; 
                   box-shadow: 0 0 35px 5px {twin_color};" 
            shadow-intensity="1"
            >
        </model-viewer>
        """
        components.html(html_code, height=550)

    with col_status:
        st.subheader("Prescriptive Alert Console")
        
        # Display the prediction with high visual impact
        if status_color == "green":
            st.success(f"## ✅ {status_text}", icon="✅")
            st.info("The Digital Twin predicts optimal operating conditions. Maintain current schedule.")
        elif status_color in ["orange", "yellow"]:
            st.warning(f"## ⚠️ {status_text}", icon="⚠️")
            st.error("Proactive Maintenance Required: Schedule inspection within the next 48 hours to prevent failure.")
        else:
            st.error(f"## 🚨 {status_text}", icon="🚨")
            st.info("CRITICAL ACTION: Stop asset immediately. Impending failure detected. Requires immediate replacement.")

        st.markdown("---")
        st.subheader("Current IoT Telemetry")
        st.metric("Pressure", f"{sim_pressure} PSI", delta=f"{WEAR_THRESHOLD_PRESSURE} PSI Threshold")
        st.metric("Mileage", f"{sim_mileage} km", delta=f"{HIGH_MILEAGE_THRESHOLD} km Threshold")
        st.metric("Temperature", f"{sim_temp} °C", delta=f"{CRITICAL_TEMP_THRESHOLD} °C Warning")


# --- TAB 2: SIMULATION & DIAGNOSTICS ---
with tab2:
    st.header("Long-Term Performance Diagnostics")
    
    st.markdown("### Simulated Tire Lifetime Analysis")
    st.caption("This plot shows the simulated life of the tire based on historical data, with the wear threshold clearly marked.")
    
    # Plotly for professional-looking graph
    fig_sim = go.Figure()
    fig_sim.add_trace(go.Scatter(x=df_sim['Mileage (km)'], y=df_sim['Pressure (PSI)'], name='Pressure (PSI)', line=dict(color='cyan')))
    fig_sim.add_trace(go.Scatter(x=df_sim['Mileage (km)'], y=df_sim['Temperature (°C)'], name='Temperature (°C)', line=dict(color='yellow')))
    
    # Add Alert Threshold Line
    fig_sim.add_hline(y=WEAR_THRESHOLD_PRESSURE, line_dash="dash", line_color="red", annotation_text="CRITICAL PRESSURE THRESHOLD", annotation_position="top right")

    fig_sim.update_layout(
        title='Simulated Wear vs. Mileage',
        xaxis_title='Mileage (km)',
        yaxis_title='Value',
        plot_bgcolor='#1e2329', 
        paper_bgcolor='#0d1117', 
        font_color='#f0f6fc',
        template="plotly_dark" # Use Plotly's dark theme
    )
    st.plotly_chart(fig_sim, use_container_width=True)

    st.markdown("---")
    st.subheader("Key Diagnostic Takeaways")
    col_diag1, col_diag2 = st.columns(2)
    with col_diag1:
        st.success("**Project Value:** Demonstrates the ability to shift maintenance from **Cost Center** to **Value Driver**.")
    with col_diag2:
        st.info("**Meta 4.0 Alignment:** High-fidelity Digital Twin, IoT Integration, and Prescriptive AI.")
