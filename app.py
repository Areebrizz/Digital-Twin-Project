import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots # Necessary for stable dual-axis plot
import streamlit.components.v1 as components
import random

# --- CONFIGURATION: Full Screen, No Scroll ---
st.set_page_config(
    page_title="Erasmus Meta 4.0 Digital Twin Command Center",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
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

# --- 2. LIGHT THEME UI: Professional and High-Contrast (CSS omitted for brevity, assumed correct) ---
st.markdown("""
<style>
/* 1. BASE THEME: Bright White/Light Gray Background */
.main {
    background-color: #F8F8F8; 
    color: #111111; 
    padding-top: 0.5rem;
}

/* 2. HEADER & TITLE: Deep Blue Accent */
h1, h2, h3 {
    color: #000080; 
    font-family: 'Segoe UI', sans-serif;
    font-weight: 700;
    border-bottom: 2px solid #ADD8E6; 
    padding-bottom: 5px;
    margin-bottom: 0.5rem;
}

/* 3. CONTAINERS & METRICS: Clean White Boxes with Blue Border */
.stMetric {
    background-color: #FFFFFF;
    padding: 12px;
    border-radius: 10px;
    border: 1px solid #000080; 
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1); 
    margin-bottom: 8px;
}

.stMetric > div:nth-child(1) > div:nth-child(1) {
    font-size: 1.8em;
    color: #000080; 
    font-weight: 700;
}

/* 4. COMPACT WIDGETS */
.stSlider {
    margin-bottom: 5px;
}
div[role="slider"] {
    background-color: #E0E0E0; 
    border-radius: 8px;
    border: 1px solid #000080;
}
.stSlider > div > div > div:nth-child(2) { 
    background-color: #000080; 
}

/* 5. COMPACT ALERTS */
.stAlert {
    padding: 10px;
    margin-bottom: 8px;
    border-radius: 8px;
    font-size: 0.9em;
    color: #111111; 
}
.stSuccess {  
    background: #E6F7E6 !important; 
    border-left: 4px solid #3CB371 !important; 
}
.stWarning { 
    background: #FFFBE6 !important; 
    border-left: 4px solid #FFA500 !important; 
}
.stError { 
    background: #FFEBE6 !important; 
    border-left: 4px solid #FF4500 !important; 
}

/* 6. ELIMINATE ALL WHITESPACE */
div.block-container {
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
    padding-left: 1rem;
    padding-right: 1rem;
}

/* 7. COMPACT COLUMNS AND LAYOUT */
[data-testid="column"] {
    padding: 0.5rem;
}

/* 8. CUSTOM COMPONENTS */
.digital-twin-container {
    border: 2px solid #000080; 
    border-radius: 12px;
    box-shadow: 0 0 10px rgba(0, 0, 128, 0.2);
    overflow: hidden;
    margin-bottom: 8px;
}

.cyber-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, #ADD8E6, transparent);
    margin: 5px 0;
}

/* 9. STATUS INDICATORS */
.status-indicator {
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.9em;
    font-weight: bold;
    text-align: center;
}
.status-normal { background: #3CB371; color: white; }
.status-warning { background: #FFA500; color: white; }
.status-critical { background: #FF4500; color: white; }
</style>
""", unsafe_allow_html=True)

# --- 3. COMPACT LAYOUT: Single Page, No Scroll ---
header_col1, header_col2 = st.columns([3, 1])

with header_col1:
    st.markdown("# 🚀 META 4.0 DIGITAL TWIN COMMAND CENTER")
    st.markdown("### Prescriptive Maintenance Intelligence Platform")

# Get current status
sim_mileage = 20000
sim_pressure = 31.5
sim_temp = 55.0

# Main Dashboard Grid - Single View, No Scroll
main_col1, main_col2, main_col3, main_col4 = st.columns([2.5, 1.5, 2, 1.5])

# --- COLUMN 4: I/O SIMULATOR (COMPACT CONTROLS) ---
with main_col4:
    st.markdown("### I/O SIMULATOR")
    st.caption("Adjust parameters to test system response")
    
    # Sliders for user input
    sim_mileage = st.slider("Mileage (km)", 0, 50000, 20000, 1000, key="mileage")
    sim_pressure = st.slider("Pressure (PSI)", 20.0, 45.0, 31.5, 0.1, key="pressure")
    sim_temp = st.slider("Temperature (°C)", 20.0, 100.0, 55.0, 0.5, key="temp")

status_text, status_color, status_icon = predict_wear_and_status(sim_pressure, sim_mileage, sim_temp)


# --- COLUMN 1: DIGITAL TWIN VISUALIZATION ---
with main_col1:
    st.markdown("### DIGITAL TWIN VISUALIZATION")
    
    # Dynamic glow based on status
    glow_colors = {
        "green": "rgba(60, 179, 113, 0.6)", 
        "yellow": "rgba(255, 165, 0, 0.6)", 
        "orange": "rgba(255, 69, 0, 0.6)",  
        "red": "rgba(255, 0, 0, 0.6)"
    }
    
    twin_glow = glow_colors.get(status_color, "rgba(0, 0, 128, 0.6)")
    
    # Corrected GLB URL using raw content
    model_path = "https://raw.githubusercontent.com/Areebrizz/Digital-Twin-Project/main/offorad_vehicle_tires.glb" 

    html_code = f"""
    <div class="digital-twin-container" style="box-shadow: 0 0 10px 3px {twin_glow};">
        <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.5.0/model-viewer.min.js"></script>
        <model-viewer 
            src="{model_path}" 
            alt="Digital Twin Asset Model"
            auto-rotate 
            camera-controls
            style="width: 100%; height: 280px; background-color: #F8F8F8;" 
            shadow-intensity="1.5"
            exposure="1.2"
            environment-image="neutral"
            >
        </model-viewer>
    </div>
    """
    components.html(html_code, height=300)
    
    # Status indicator below twin
    status_class = {
        "green": "status-normal",
        "yellow": "status-warning", 
        "orange": "status-warning",
        "red": "status-critical"
    }
    st.markdown(f'<div class="{status_class[status_color]} status-indicator">{status_icon} {status_text}</div>', unsafe_allow_html=True)

# --- COLUMN 2: REAL-TIME TELEMETRY (Gauges) ---
with main_col2:
    st.markdown("### REAL-TIME TELEMETRY")
    
    # Pressure Gauge
    pressure_percent = max(0, min(100, (sim_pressure - 20) / (45 - 20) * 100))
    pressure_color = "#3CB371" if sim_pressure > WEAR_THRESHOLD_PRESSURE else "#FF4500"
    
    st.markdown(f"**PRESSURE:** **{sim_pressure}** PSI")
    st.markdown(f"""
    <div style="background: #E0E0E0; border-radius: 10px; padding: 5px; margin-bottom: 15px;">
        <div style="background: linear-gradient(90deg, {pressure_color} {pressure_percent}%, #BBBBBB {pressure_percent}%); 
                    height: 15px; border-radius: 6px; border: 1px solid #000080;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Temperature Gauge
    temp_percent = max(0, min(100, (sim_temp - 20) / (100 - 20) * 100))
    temp_color = "#3CB371" if sim_temp < CRITICAL_TEMP_THRESHOLD else "#FF4500"
    
    st.markdown(f"**TEMPERATURE:** **{sim_temp}**°C")
    st.markdown(f"""
    <div style="background: #E0E0E0; border-radius: 10px; padding: 5px; margin-bottom: 15px;">
        <div style="background: linear-gradient(90deg, {temp_color} {temp_percent}%, #BBBBBB {temp_percent}%); 
                    height: 15px; border-radius: 6px; border: 1px solid #000080;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Mileage Gauge
    mileage_percent = max(0, min(100, sim_mileage / 50000 * 100))
    mileage_color = "#3CB371" if sim_mileage < HIGH_MILEAGE_THRESHOLD else "#FF4500"
    
    st.markdown(f"**MILEAGE:** **{sim_mileage}** km")
    st.markdown(f"""
    <div style="background: #E0E0E0; border-radius: 10px; padding: 5px; margin-bottom: 15px;">
        <div style="background: linear-gradient(90deg, {mileage_color} {mileage_percent}%, #BBBBBB {mileage_percent}%); 
                    height: 15px; border-radius: 6px; border: 1px solid #000080;"></div>
    </div>
    """, unsafe_allow_html=True)

# --- COLUMN 3: PRESCRIPTIVE ANALYTICS & QUICK METRICS ---
with main_col3:
    st.markdown("### PRESCRIPTIVE ANALYTICS")
    
    # Alert Display
    if status_color == "green":
        st.success(f"**{status_icon} {status_text}**")
        st.markdown("**Action:** Continue normal operations. Next inspection: **30 days**.")
    elif status_color == "yellow":
        st.warning(f"**{status_icon} {status_text}**")
        st.markdown("**Action:** Schedule inspection within **7 days**. Risk level: **Medium**.")
    elif status_color == "orange":
        st.error(f"**{status_icon} {status_text}**")
        st.markdown("**Action:** **Urgent maintenance required within 48h**. Risk level: **High**.")
    else:
        st.error(f"**{status_icon} {status_text}**")
        st.markdown("**Action:** **IMMEDIATE SHUTDOWN REQUIRED**. Impending failure.")
    
    st.markdown('<div class="cyber-divider"></div>', unsafe_allow_html=True)
    
    # Quick Stats
    st.markdown("### PERFORMANCE METRICS")
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Uptime", "98.7%", "0.3%")
        st.metric("Fuel Eff.", "++ 5.2%")
    with col_b:
        st.metric("Cost Saved", "$2.8K", "+12%")
        st.metric("Risk Score", "24/100", "-8%")


# --- 5. BOTTOM SECTION: COMPACT TREND & ROI (Full Width) ---
st.markdown('<div class="cyber-divider"></div>', unsafe_allow_html=True)

trend_col1, trend_col2 = st.columns([4, 1])

with trend_col1:
    st.markdown("### ASSET HEALTH TREND ANALYSIS")
    
    # FIX 1: Use make_subplots to explicitly set up the secondary axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Trace 1: Pressure (Primary Y-axis)
    # FIX 2: Removed 'secondary_y' argument from INSIDE go.Scatter()
    fig.add_trace(go.Scatter(
        x=df_sim['Mileage (km)'], 
        y=df_sim['Pressure (PSI)'], 
        name='Pressure (PSI)',
        line=dict(color='#000080', width=3),
        fill='tozeroy',
        fillcolor='rgba(0, 0, 128, 0.1)'
    ), secondary_y=False) # Correct placement for axis assignment
    
    # Trace 2: Temperature (Secondary Y-axis)
    # FIX 2: Removed 'secondary_y' argument from INSIDE go.Scatter()
    fig.add_trace(go.Scatter(
        x=df_sim['Mileage (km)'], 
        y=df_sim['Temperature (°C)'], 
        name='Temperature (°C)',
        line=dict(color='#800080', width=3)
    ), secondary_y=True) # Correct placement for axis assignment
    
    # Add horizontal critical line to the primary axis
    fig.add_hline(
        y=WEAR_THRESHOLD_PRESSURE, 
        line_dash="dash", 
        line_color="#FF4500",
        annotation_text="CRITICAL PRESSURE",
        annotation_font_color="#FF4500",
        secondary_y=False
    )
    
    # Apply general layout settings
    fig.update_layout(
        height=250, 
        margin=dict(l=20, r=50, t=30, b=20),
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#F8F8F8',
        font_color='#111111',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom", y=1.02, xanchor="right", x=1
        ),
        xaxis=dict(gridcolor='#E0E0E0', title="Mileage (km)"),
    )
    
    # Apply primary axis settings using update_yaxes
    fig.update_yaxes(
        title_text="Pressure (PSI)", 
        title_font=dict(color="#000080"), 
        tickfont=dict(color="#000080"), 
        gridcolor='#E0E0E0',
        secondary_y=False 
    )
    
    # Apply secondary axis settings using update_yaxes
    fig.update_yaxes(
        title_text="Temperature (°C)", 
        title_font=dict(color="#800080"), 
        tickfont=dict(color="#800080"),
        gridcolor='#E0E0E0',
        showgrid=False,
        secondary_y=True 
    )
    
    st.plotly_chart(fig, use_container_width=True)

with trend_col2:
    st.markdown("### STRATEGIC ROI")
    st.markdown("""
    <div style="background: #FFFFFF; border-radius: 10px; padding: 15px; border: 1px solid #000080; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
    <h4 style="color: #3CB371; margin: 0;">✅ 20% UPTIME</h4>
    <p style="margin: 5px 0 10px 0; font-size: 0.8em; color: #111111;">Reduction in Downtime</p>
    
    <h4 style="color: #3CB371; margin: 0;">✅ 15% ASSET LIFE</h4>
    <p style="margin: 5px 0 10px 0; font-size: 0.8em; color: #111111;">Lifecycle Optimization</p>

    <h4 style="color: #3CB371; margin: 0;'>✅ 72h LEAD TIME</h4>
    <p style="margin: 5px 0; font-size: 0.8em; color: #111111;">Prescriptive Maintenance</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown('<div class="cyber-divider"></div>', unsafe_allow_html=True)
footer_col1, footer_col2, footer_col3 = st.columns([2, 1, 1])
with footer_col1:
    st.caption("© 2024 Erasmus Meta 4.0 Digital Twin Platform | Real-time Prescriptive Maintenance")
with footer_col2:
    st.caption("System Status: **OPERATIONAL**")
with footer_col3:
    st.caption("Last Update: Live Feed")
