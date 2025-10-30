import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
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

# --- 2. ENHANCED UI THEME: Cyberpunk Inspired ---
st.markdown("""
<style>
/* 1. BASE THEME: Pure Black with Cyberpunk Elements */
.main {
    background-color: #000000;
    color: #e0e0e0;
    padding-top: 0.5rem;
}

/* 2. HEADER & TITLE: Neon Cyberpunk */
h1, h2, h3 {
    color: #00FFFF;
    text-shadow: 0 0 10px #00FFFF, 0 0 20px #00FFFF, 0 0 30px #0080FF;
    font-family: 'Courier New', monospace;
    font-weight: 700;
    letter-spacing: 1px;
    margin-bottom: 0.5rem;
}

/* 3. COMPACT CONTAINERS */
.stMetric {
    background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
    padding: 12px;
    border-radius: 10px;
    border: 1px solid #00FFFF;
    box-shadow: 0 0 15px rgba(0, 255, 255, 0.3);
    margin-bottom: 8px;
}

.stMetric > div:nth-child(1) > div:nth-child(1) {
    font-size: 1.8em;
    color: #00FFFF;
    font-weight: 700;
}

/* 4. COMPACT WIDGETS */
.stSlider {
    margin-bottom: 5px;
}
div[role="slider"] {
    background-color: #1a1a1a;
}
.stSlider > div > div > div:nth-child(2) { 
    background-color: #00FFFF;
}

/* 5. COMPACT ALERTS */
.stAlert {
    padding: 10px;
    margin-bottom: 8px;
    border-radius: 8px;
    font-size: 0.9em;
}
.stSuccess { 
    background: linear-gradient(135deg, #0a2a0a 0%, #1a3a1a 100%) !important;
    border-left: 4px solid #00FF00 !important;
}
.stWarning { 
    background: linear-gradient(135deg, #2a2a0a 0%, #3a3a1a 100%) !important;
    border-left: 4px solid #FFFF00 !important;
}
.stError { 
    background: linear-gradient(135deg, #2a0a0a 0%, #3a1a1a 100%) !important;
    border-left: 4px solid #FF0000 !important;
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
    border: 2px solid #00FFFF;
    border-radius: 12px;
    box-shadow: 0 0 20px rgba(0, 255, 255, 0.4);
    overflow: hidden;
    margin-bottom: 8px;
}

.cyber-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, #00FFFF, transparent);
    margin: 5px 0;
}

.compact-section {
    margin-bottom: 0.5rem;
}

/* 9. STATUS INDICATORS */
.status-indicator {
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 0.8em;
    font-weight: bold;
}
.status-normal { background: #00FF00; color: black; }
.status-warning { background: #FFFF00; color: black; }
.status-critical { background: #FF0000; color: white; }
</style>
""", unsafe_allow_html=True)

# --- 3. COMPACT LAYOUT: Single Page, No Scroll ---
# Top Section: Title and Controls
header_col1, header_col2 = st.columns([3, 1])

with header_col1:
    st.markdown("# 🚀 META 4.0 DIGITAL TWIN COMMAND CENTER")
    st.markdown("### Prescriptive Maintenance Intelligence Platform")

with header_col2:
    st.markdown("### I/O SIMULATOR")
    st.caption("Adjust parameters to test system response")

# Main Dashboard Grid - Single View, No Scroll
main_col1, main_col2, main_col3, main_col4 = st.columns([2, 1.5, 1.5, 1])

# Get current status
sim_mileage = 20000
sim_pressure = 31.5
sim_temp = 55.0

with main_col4:
    # Compact controls in the right column
    sim_mileage = st.slider("Mileage (km)", 0, 50000, 20000, 1000, key="mileage")
    sim_pressure = st.slider("Pressure (PSI)", 20.0, 45.0, 31.5, 0.1, key="pressure")
    sim_temp = st.slider("Temperature (°C)", 20.0, 100.0, 55.0, 0.5, key="temp")

status_text, status_color, status_icon = predict_wear_and_status(sim_pressure, sim_mileage, sim_temp)

# --- COLUMN 1: DIGITAL TWIN VISUALIZATION ---
with main_col1:
    st.markdown("### DIGITAL TWIN VISUALIZATION")
    
    # Dynamic glow based on status
    glow_colors = {
        "green": "rgba(0, 255, 0, 0.6)",
        "yellow": "rgba(255, 255, 0, 0.6)", 
        "orange": "rgba(255, 165, 0, 0.6)",
        "red": "rgba(255, 0, 0, 0.6)"
    }
    
    twin_glow = glow_colors.get(status_color, "rgba(0, 255, 255, 0.6)")
    model_path = "https://cdn.jsdelivr.net/gh/google/model-viewer/examples/assets/RobotExpressive.glb"

    html_code = f"""
    <div class="digital-twin-container" style="box-shadow: 0 0 25px 8px {twin_glow};">
        <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.5.0/model-viewer.min.js"></script>
        <model-viewer 
            src="{model_path}" 
            alt="Digital Twin Asset Model"
            auto-rotate 
            camera-controls
            style="width: 100%; height: 280px; background-color: #000000;" 
            shadow-intensity="1.5"
            exposure="1.2"
            environment-image="neutral"
            >
        </model-viewer>
    </div>
    """
    components.html(html_code, height=300)
    
    # Status indicator below twin
    status_colors = {
        "green": "status-normal",
        "yellow": "status-warning", 
        "orange": "status-warning",
        "red": "status-critical"
    }
    st.markdown(f'<div class="{status_colors[status_color]} status-indicator">{status_icon} {status_text}</div>', unsafe_allow_html=True)

# --- COLUMN 2: REAL-TIME TELEMETRY ---
with main_col2:
    st.markdown("### REAL-TIME TELEMETRY")
    
    # Pressure Gauge
    pressure_percent = max(0, min(100, (sim_pressure - 20) / (45 - 20) * 100))
    pressure_color = "#00FF00" if sim_pressure > WEAR_THRESHOLD_PRESSURE else "#FF0000"
    
    st.markdown(f"**PRESSURE:** {sim_pressure} PSI")
    st.markdown(f"""
    <div style="background: #1a1a1a; border-radius: 10px; padding: 5px; margin-bottom: 15px;">
        <div style="background: linear-gradient(90deg, {pressure_color} {pressure_percent}%, #333 {pressure_percent}%); 
                    height: 20px; border-radius: 8px; border: 1px solid #00FFFF;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Temperature Gauge
    temp_percent = max(0, min(100, (sim_temp - 20) / (100 - 20) * 100))
    temp_color = "#00FF00" if sim_temp < CRITICAL_TEMP_THRESHOLD else "#FF0000"
    
    st.markdown(f"**TEMPERATURE:** {sim_temp}°C")
    st.markdown(f"""
    <div style="background: #1a1a1a; border-radius: 10px; padding: 5px; margin-bottom: 15px;">
        <div style="background: linear-gradient(90deg, {temp_color} {temp_percent}%, #333 {temp_percent}%); 
                    height: 20px; border-radius: 8px; border: 1px solid #00FFFF;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    # Mileage Gauge
    mileage_percent = max(0, min(100, sim_mileage / 50000 * 100))
    mileage_color = "#00FF00" if sim_mileage < HIGH_MILEAGE_THRESHOLD else "#FF0000"
    
    st.markdown(f"**MILEAGE:** {sim_mileage} km")
    st.markdown(f"""
    <div style="background: #1a1a1a; border-radius: 10px; padding: 5px; margin-bottom: 15px;">
        <div style="background: linear-gradient(90deg, {mileage_color} {mileage_percent}%, #333 {mileage_percent}%); 
                    height: 20px; border-radius: 8px; border: 1px solid #00FFFF;"></div>
    </div>
    """, unsafe_allow_html=True)

# --- COLUMN 3: PRESCRIPTIVE ANALYTICS ---
with main_col3:
    st.markdown("### PRESCRIPTIVE ANALYTICS")
    
    # Alert Display
    if status_color == "green":
        st.success(f"**{status_icon} {status_text}**")
        st.markdown("**ACTION:** Continue normal operations")
        st.markdown("**NEXT MAINTENANCE:** 30 days")
        
    elif status_color == "yellow":
        st.warning(f"**{status_icon} {status_text}**")
        st.markdown("**ACTION:** Schedule inspection within 7 days")
        st.markdown("**RISK LEVEL:** Medium")
        
    elif status_color == "orange":
        st.error(f"**{status_icon} {status_text}**")
        st.markdown("**ACTION:** **Urgent maintenance required within 48h**")
        st.markdown("**RISK LEVEL:** High")
        
    else:
        st.error(f"**{status_icon} {status_text}**")
        st.markdown("**ACTION:** **IMMEDIATE SHUTDOWN REQUIRED**")
        st.markdown("**RISK LEVEL:** Critical")
    
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

# --- BOTTOM SECTION: COMPACT TREND VISUALIZATION ---
st.markdown('<div class="cyber-divider"></div>', unsafe_allow_html=True)

# Create a compact trend visualization
trend_col1, trend_col2 = st.columns([3, 1])

with trend_col1:
    st.markdown("### ASSET HEALTH TREND ANALYSIS")
    
    fig = go.Figure()
    
    # Add traces with cyberpunk colors
    fig.add_trace(go.Scatter(
        x=df_sim['Mileage (km)'], 
        y=df_sim['Pressure (PSI)'], 
        name='Pressure',
        line=dict(color='#00FFFF', width=3),
        fill='tozeroy',
        fillcolor='rgba(0, 255, 255, 0.1)'
    ))
    
    fig.add_trace(go.Scatter(
        x=df_sim['Mileage (km)'], 
        y=df_sim['Temperature (°C)'], 
        name='Temperature',
        line=dict(color='#FF00FF', width=3),
        yaxis='y2'
    ))
    
    # Threshold lines
    fig.add_hline(
        y=WEAR_THRESHOLD_PRESSURE, 
        line_dash="dash", 
        line_color="#FF0000",
        annotation_text="CRITICAL PRESSURE",
        annotation_font_color="#FF0000"
    )
    
    # Fixed layout configuration - proper syntax
    fig.update_layout(
        height=200,
        margin=dict(l=20, r=50, t=30, b=20),
        plot_bgcolor='#0a0a0a',
        paper_bgcolor='#000000',
        font_color='#e0e0e0',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    # Separate axis updates
    fig.update_yaxes(
        title="Pressure (PSI)",
        titlefont=dict(color="#00FFFF"),
        tickfont=dict(color="#00FFFF"),
        gridcolor='#1a1a1a'
    )
    
    fig.update_yaxes(
        title="Temperature (°C)",
        titlefont=dict(color="#FF00FF"),
        tickfont=dict(color="#FF00FF"),
        overlaying='y',
        side='right',
        gridcolor='#1a1a1a'
    )
    
    fig.update_xaxes(
        gridcolor='#1a1a1a'
    )
    
    st.plotly_chart(fig, use_container_width=True)

with trend_col2:
    st.markdown("### ROI IMPACT")
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0a1a2a 0%, #1a2a3a 100%); 
                padding: 15px; border-radius: 10px; border: 1px solid #00FFFF;">
    <h4 style="color: #00FFFF; margin: 0;">📈 +20%</h4>
    <p style="margin: 5px 0;">Uptime</p>
    <h4 style="color: #00FFFF; margin: 10px 0 0 0;">💰 +15%</h4>
    <p style="margin: 5px 0;">Asset Life</p>
    <h4 style="color: #00FFFF; margin: 10px 0 0 0;">🛡️ 72h</h4>
    <p style="margin: 5px 0;">Predictive Lead</p>
    </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns([2, 1, 1])
with footer_col1:
    st.caption("© 2024 Erasmus Meta 4.0 Digital Twin Platform | Real-time Prescriptive Maintenance")
with footer_col2:
    st.caption("System Status: **OPERATIONAL**")
with footer_col3:
    st.caption("Last Update: Live Feed")
