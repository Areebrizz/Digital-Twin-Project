import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit.components.v1 as components
import random

# --- CONFIGURATION & FUTURISTIC CSS (MANDATORY FOR CONSISTENCY) ---
st.set_page_config(
    page_title="Digital Twin Predictive Dashboard",
    page_icon="📈",
    layout="wide"
)

# Custom CSS for Executive-Grade Futuristic Dark Theme (Deep Navy/Cyan Glow)
st.markdown("""
<style>
/* 1. BASE THEME: Deep Navy/Charcoal */
.main {
    background-color: #0c1524; /* Deep Navy Blue */
    color: #e6f1ff; /* Light Blue/White Text */
}

/* 2. HEADER & TITLE GLOW: High Contrast Cyan */
h1, h2, h3 {
    color: #00FFFF; /* Pure Cyan */
    text-shadow: 0 0 8px rgba(0, 255, 255, 0.7), 0 0 15px rgba(0, 255, 255, 0.4);
    font-family: 'Consolas', monospace; /* Techy font feel */
    border-bottom: 1px solid rgba(0, 255, 255, 0.2);
    padding-bottom: 5px;
}

/* 3. CONTAINERS & METRICS: Subtly Elevated Backgrounds */
.stMetric {
    background: linear-gradient(135deg, #16243a, #0c1524); /* Subtle Gradient */
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #00FFFF; /* Cyan Border */
    box-shadow: 0 0 15px rgba(0, 255, 255, 0.2);
    transition: all 0.3s;
}
.stMetric:hover {
    box-shadow: 0 0 25px rgba(0, 255, 255, 0.5); /* Hover effect */
}

/* 4. SIDEBAR: Ultra Dark */
[data-testid="stSidebar"] {
    background-color: #060d16; /* Near Black */
    color: #99FFFF;
    border-right: 3px solid #00FFFF;
}
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
    color: #00FFFF;
    text-shadow: 0 0 3px rgba(0, 255, 255, 0.7);
}

/* 5. EMPHASIS TEXT: Gold/Yellow for Value */
.value-text {
    color: #FFD700; /* Gold */
    font-weight: 700;
    font-size: 1.1em;
    text-shadow: 0 0 5px #FFD700;
}

/* 6. DIVIDER LINE */
hr {
    border-top: 3px solid rgba(0, 255, 255, 0.3);
    opacity: 0.8;
}

/* 7. WIDGETS (Sliders/Inputs): Sharper, Darker Look */
div[role="slider"] {
    background-color: #16243a; 
    border-radius: 5px;
    border: 1px solid #00FFFF;
}
.stSlider > div > div > div:nth-child(2) { /* Slider rail */
    background: linear-gradient(to right, #00FFFF, #16243a);
}

/* 8. TAB STYLING: Highlight Active Tab */
.stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
    border-bottom: 3px solid #00FFFF; 
    color: #00FFFF !important;
    text-shadow: 0 0 5px #00FFFF;
}

/* 9. Alerts */
.stAlert {
    border-left: 5px solid;
    border-radius: 8px;
    background-color: #16243a !important;
}

/* 10. Success/Warning/Error Overrides for better contrast */
.stSuccess { border-left-color: #4CAF50 !important; }
.stWarning { border-left-color: #FFD700 !important; }
.stError { border-left-color: #FF0000 !important; }

</style>
""", unsafe_allow_html=True)

# --- 2. PREDICTIVE LOGIC (Adapted from Colab) ---
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
        if status_color == "green":
            twin_color = "#4CAF50" # Green for Normal
        elif status_color == "yellow":
            twin_color = "#FFD700" # Gold/Yellow-Orange for Warning
        elif status_color == "orange":
            twin_color = "#FFA500" # Orange for High Risk
        else: # Critical
            twin_color = "#FF0000" # Red for Critical

        # NOTE: This placeholder model URL MUST be replaced with your GLB file's RAW URL from GitHub
        model_path = "https://cdn.jsdelivr.net/gh/google/model-viewer/examples/assets/RobotExpressive.glb" 

        html_code = f"""
        <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.5.0/model-viewer.min.js"></script>
        <model-viewer 
            src="{model_path}" 
            alt="Digital Twin Tire Model"
            auto-rotate 
            camera-controls 
            ar
            style="width: 100%; height: 550px; border-radius: 15px; background-color: #0c1524; 
                   box-shadow: 0 0 35px 5px {twin_color}; border: 2px solid {twin_color};" 
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
        elif status_color == "yellow":
            st.warning(f"## ⚠️ {status_text}", icon="⚠️")
            st.markdown("*Action:* Minor inspection recommended. Monitor parameters closely.")
        elif status_color == "orange":
            st.error(f"## 🚨 {status_text}", icon="🚨")
            st.markdown("*Action:* **Proactive Maintenance Required!** Schedule inspection within 48 hours.")
        else:
            st.error(f"## 🛑 {status_text}", icon="🛑")
            st.markdown("*Action:* **CRITICAL SHUTDOWN!** Stop asset immediately. Impending failure detected.")

        st.markdown("---")
        st.subheader("Current IoT Telemetry")
        st.metric("Pressure", f"{sim_pressure} PSI", delta=f"Threshold: {WEAR_THRESHOLD_PRESSURE} PSI")
        st.metric("Mileage", f"{sim_mileage} km", delta=f"Threshold: {HIGH_MILEAGE_THRESHOLD} km")
        st.metric("Temperature", f"{sim_temp} °C", delta=f"Warning: {CRITICAL_TEMP_THRESHOLD} °C")


# --- TAB 2: SIMULATION & DIAGNOSTICS ---
with tab2:
    st.header("Long-Term Performance Diagnostics")
    
    st.markdown("### Simulated Tire Lifetime Analysis")
    st.caption("This Plotly chart demonstrates the model's ability to track wear and predict the point of failure.")
    
    # Plotly for professional-looking graph
    fig_sim = go.Figure()
    fig_sim.add_trace(go.Scatter(x=df_sim['Mileage (km)'], y=df_sim['Pressure (PSI)'], name='Pressure (PSI)', line=dict(color='#00FFFF')))
    fig_sim.add_trace(go.Scatter(x=df_sim['Mileage (km)'], y=df_sim['Temperature (°C)'], name='Temperature (°C)', line=dict(color='#FFD700')))
    
    # Add Alert Threshold Line
    fig_sim.add_hline(y=WEAR_THRESHOLD_PRESSURE, line_dash="dot", line_color="#FF0000", 
                      annotation_text="CRITICAL PRESSURE THRESHOLD", annotation_position="top right",
                      annotation_font_color="#FF0000")

    fig_sim.update_layout(
        title='Simulated Wear vs. Mileage',
        xaxis_title='Mileage (km)',
        yaxis_title='Value',
        plot_bgcolor='#16243a', 
        paper_bgcolor='#0c1524', 
        font_color='#e6f1ff',
        template="plotly_dark", # Use Plotly's dark theme
        hovermode="x unified"
    )
    st.plotly_chart(fig_sim, use_container_width=True)

    st.markdown("---")
    st.subheader("Key Diagnostic Takeaways")
    col_diag1, col_diag2 = st.columns(2)
    with col_diag1:
        st.success("Mastery Demonstrated: High-fidelity Digital Twin, IoT Integration, and Prescriptive AI.")
    with col_diag2:
        st.info("Project Value: Successfully demonstrated the shift from **Reactive** to **Prescriptive** maintenance.")
