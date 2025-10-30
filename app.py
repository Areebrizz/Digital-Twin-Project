import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import streamlit.components.v1 as components
import random

# --- CONFIGURATION: Maximize Screen Real Estate ---
st.set_page_config(
    page_title="Erasmus Meta 4.0 Digital Twin Command Center",
    page_icon="⚙️",
    layout="wide", # Essential for no-scroll
    initial_sidebar_state="collapsed" # Hide sidebar by default
)

# --- 1. PREDICTIVE LOGIC (Core Constants) ---
WEAR_THRESHOLD_PRESSURE = 28.0 
HIGH_MILEAGE_THRESHOLD = 40000.0
CRITICAL_TEMP_THRESHOLD = 80.0

def predict_wear_and_status(pressure, mileage, temp):
    """Predicts the tire status and returns status string, color, and icon."""
    if pressure < WEAR_THRESHOLD_PRESSURE and mileage > 10000:
        return "CRITICAL FAILURE IMMINENT", "red", "🛑"
    elif pressure < WEAR_THRESHOLD_PRESSURE:
        return "HIGH RISK: LOW PRESSURE", "orange", "🚨"
    elif mileage > HIGH_MILEAGE_THRESHOLD:
        return "HIGH RISK: HIGH MILEAGE", "orange", "⚠️"
    elif temp > CRITICAL_TEMP_THRESHOLD:
        return "WARNING: HIGH TEMPERATURE", "yellow", "🔥"
    else:
        return "NORMAL OPERATING STATE", "green", "✅"

@st.cache_data
def generate_simulation_data():
    """Generates the data for the historical trend plot."""
    data = []
    pressure_start = 32
    temp_start = 25
    mileage_start = 0
    
    for i in range(100): 
        pressure_start -= random.uniform(0.1, 0.3)
        temp_start += random.uniform(-1, 3)
        mileage_start += random.uniform(300, 800)
        data.append((mileage_start, pressure_start, temp_start))
        if pressure_start < WEAR_THRESHOLD_PRESSURE:
             break 
    df = pd.DataFrame(data, columns=['Mileage (km)', 'Pressure (PSI)', 'Temperature (°C)'])
    return df

df_sim = generate_simulation_data()


# --- 2. THEME: High-Contrast, Professional Dark Mode (No Bright "Bullshit") ---
st.markdown("""
<style>
/* 1. BASE THEME: Pure Black Background, Sharp Text */
.main {
    background-color: #000000; /* Pure Black for maximum contrast */
    color: #e0e0e0; /* Off-White/Gray Text */
    padding-top: 1rem; /* Reduce top padding */
}

/* 2. HEADER & TITLE: Controlled Cyan Glow */
h1, h2, h3 {
    color: #39FF14; /* Neon Green/Cyan for controlled digital look */
    text-shadow: 0 0 5px #39FF14, 0 0 10px rgba(57, 255, 20, 0.5); 
    font-family: 'Consolas', monospace; 
    border-bottom: 2px solid rgba(57, 255, 20, 0.3);
    padding-bottom: 5px;
    margin-bottom: 10px;
}

/* 3. CONTAINERS & METRICS: Subtle Charcoal Backgrounds */
.stMetric {
    background-color: #1a1a1a; /* Dark charcoal */
    padding: 15px;
    border-radius: 8px;
    border: 1px solid rgba(57, 255, 20, 0.4); 
    box-shadow: 0 0 8px rgba(57, 255, 20, 0.2); 
}

/* Metric Value: Large and Green */
.stMetric > div:nth-child(1) > div:nth-child(1) {
    font-size: 2.2em;
    color: #39FF14;
}

/* 4. WIDGETS (Sliders/Inputs): Clean, Minimalist */
div[role="slider"] {
    background-color: #1a1a1a; 
    border-radius: 4px;
    border: 1px solid #39FF14;
}
.stSlider > div > div > div:nth-child(2) { 
    background-color: #333333;
}

/* 5. Alerts: High visibility, low brightness */
.stAlert {
    background-color: #1a1a1a !important;
    border-left: 5px solid;
    border-radius: 6px;
    font-size: 1.1em;
}
.stSuccess { border-left-color: #39FF14 !important; }
.stWarning { border-left-color: #FFD700 !important; }
.stError { border-left-color: #FF0000 !important; }

/* 6. Text Emphasis */
.value-text {
    color: #FFD700; /* Gold */
    font-weight: 700;
}

/* 7. Eliminate Whitespace */
div.block-container {
    padding-top: 1rem;
    padding-bottom: 1rem;
    padding-left: 1rem;
    padding-right: 1rem;
}

/* Custom 3D Container Styling (Crucial for visual impact) */
.model-viewer-container {
    padding: 0px;
    border: 2px solid rgba(57, 255, 20, 0.6);
    border-radius: 12px;
    overflow: hidden; /* Ensures model-viewer respects border-radius */
}
</style>
""", unsafe_allow_html=True)


# --- 3. INPUTS (Placed in a compact top-left block) ---
col_A, col_B = st.columns([1, 4])

with col_A:
    st.subheader("I/O SIMULATOR")
    st.caption("Adjust parameters to test alert response.")
    sim_mileage = st.slider("Mileage (km)", 0, 50000, 20000, 1000)
    sim_pressure = st.slider("Pressure (PSI)", 20.0, 45.0, 31.5, 0.1)
    sim_temp = st.slider("Temperature (°C)", 20.0, 100.0, 55.0, 0.5)

    status_text, status_color, status_icon = predict_wear_and_status(sim_pressure, sim_mileage, sim_temp)


# --- 4. MAIN LAYOUT (4 Columns for Compact Dashboard) ---
with col_B:
    st.title("META 4.0: Digital Twin Command Center")
    st.markdown("### Prescriptive Maintenance for Vehicle Tire Assets")
    st.markdown("---")

# Main Content Row (Visuals, Metrics, Alerts, ROI)
col1, col2, col3, col4 = st.columns(4)

# --- COLUMN 1: INTERACTIVE 3D VISUALIZATION (Digital Twin) ---
with col1:
    st.subheader(f"Digital Twin: Asset State")
    
    # Logic to set 3D box glow/color
    if status_color == "green":
        twin_glow = "rgba(57, 255, 20, 0.8)" 
    elif status_color == "yellow":
        twin_glow = "rgba(255, 215, 0, 0.8)"
    elif status_color == "orange":
        twin_glow = "rgba(255, 140, 0, 0.8)"
    else: 
        twin_glow = "rgba(255, 0, 0, 0.8)"

    # IMPORTANT: Use the final URL for your GLB model here.
    model_path = "https://cdn.jsdelivr.net/gh/google/model-viewer/examples/assets/RobotExpressive.glb" 

    html_code = f"""
    <div class="model-viewer-container" style="box-shadow: 0 0 20px 5px {twin_glow};">
        <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.5.0/model-viewer.min.js"></script>
        <model-viewer 
            src="{model_path}" 
            alt="Digital Twin Tire Model"
            auto-rotate 
            camera-controls 
            ar
            style="width: 100%; height: 250px; background-color: #000000;" 
            shadow-intensity="1"
            >
        </model-viewer>
    </div>
    """
    components.html(html_code, height=270)
    st.caption(f"Status color reflects current risk level.")


# --- COLUMN 2: REAL-TIME METRICS ---
with col2:
    st.subheader("IoT Telemetry & Thresholds")
    st.metric("Pressure (PSI)", f"{sim_pressure}", delta=f"Critical < {WEAR_THRESHOLD_PRESSURE}", delta_color="inverse")
    st.metric("Mileage (km)", f"{sim_mileage}", delta=f"Threshold > {HIGH_MILEAGE_THRESHOLD}", delta_color="inverse")
    st.metric("Temperature (°C)", f"{sim_temp}", delta=f"Warning > {CRITICAL_TEMP_THRESHOLD}")


# --- COLUMN 3: PRESCRIPTIVE ALERT ---
with col3:
    st.subheader("Prescriptive Alert Console")
    
    # Use st.expander or simple text output for concise feedback
    if status_color == "green":
        st.success(f"### {status_icon} {status_text}")
        st.markdown("**Action:** Maintenance schedule approved. Low Risk.")
    elif status_color == "yellow":
        st.warning(f"### {status_icon} {status_text}")
        st.markdown("**Action:** Minor inspection recommended. Monitor closely.")
    elif status_color == "orange":
        st.error(f"### {status_icon} {status_text}")
        st.markdown("**Action:** **Proactive Maintenance Required!** Schedule inspection within 48h.")
    else:
        st.error(f"### {status_icon} {status_text}")
        st.markdown("**Action:** **CRITICAL SHUTDOWN!** Stop asset immediately. Impending failure.")


# --- COLUMN 4: PROJECT VALUE / ROI ---
with col4:
    st.subheader("Strategic Value (ROI)")
    st.markdown("""
    This twin delivers **Prescriptive Intelligence** to maximize ROI:
    * **20%** Reduction in Unplanned Downtime 
    * **15%** Optimization of Tire Life
    * **72 Hours** Predictive Lead Time
    """, unsafe_allow_html=True)
    st.markdown("---")
    st.caption("**Meta 4.0 Alignment:** High-fidelity Twin, IoT Integration, Prescriptive AI.")


# --- 5. BOTTOM ROW: HISTORICAL PLOT (Max Width) ---
st.markdown("---")
st.subheader("Diagnostic History: Wear Trend Analysis")

fig_sim = go.Figure()
fig_sim.add_trace(go.Scatter(x=df_sim['Mileage (km)'], y=df_sim['Pressure (PSI)'], name='Pressure (PSI)', line=dict(color='#00FFFF')))
fig_sim.add_trace(go.Scatter(x=df_sim['Mileage (km)'], y=df_sim['Temperature (°C)'], name='Temperature (°C)', line=dict(color='#FFD700')))

fig_sim.add_hline(y=WEAR_THRESHOLD_PRESSURE, line_dash="dot", line_color="#FF0000", 
                  annotation_text="CRITICAL THRESHOLD", annotation_position="top right",
                  annotation_font_color="#FF0000")

fig_sim.update_layout(
    xaxis_title='Mileage (km)',
    yaxis_title='Value',
    plot_bgcolor='#1a1a1a', 
    paper_bgcolor='#000000', 
    font_color='#e0e0e0',
    margin=dict(l=10, r=10, t=20, b=20), # Reduce margins
    height=300, # Control height to limit scrolling
    template="plotly_dark",
    hovermode="x unified"
)
st.plotly_chart(fig_sim, use_container_width=True)
