import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit.components.v1 as components
import random

# --- CONFIGURATION: Full Screen, No Scroll ---
st.set_page_config(
    page_title="META 4.0 Digital Twin Command Center",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 1. REALISTIC CONSTANTS & BUSINESS LOGIC ---
# Tire pressure thresholds (realistic for heavy vehicles)
WEAR_THRESHOLD_PRESSURE = 28.0  # Critical pressure for off-road tires
OPTIMAL_PRESSURE_RANGE = (30.0, 35.0)  # Ideal operating range
PRESSURE_ALERT_THRESHOLD = 29.0  # Early warning threshold

# Mileage thresholds (realistic for tire lifespan)
HIGH_MILEAGE_THRESHOLD = 40000.0  # km - typical tire lifespan
MILEAGE_ALERT_THRESHOLD = 35000.0  # Early warning

# Temperature thresholds (realistic for tire operation)
CRITICAL_TEMP_THRESHOLD = 80.0  # °C - dangerous temperature
TEMP_ALERT_THRESHOLD = 70.0  # °C - warning threshold
OPTIMAL_TEMP_RANGE = (40.0, 65.0)  # Normal operating range

# Business metrics (realistic calculations)
BASE_MAINTENANCE_COST = 1200  # $ per unplanned maintenance event
TIRE_REPLACEMENT_COST = 800   # $ per tire
DAILY_OPERATIONAL_COST = 450  # $ per day of downtime
FUEL_COST_PER_KM = 0.85      # $ per km for heavy vehicle

def predict_wear_and_status(pressure, mileage, temp):
    """Predicts the tire status with realistic multi-factor analysis."""
    risk_factors = 0
    
    # Pressure analysis
    if pressure < WEAR_THRESHOLD_PRESSURE:
        risk_factors += 3  # Critical pressure
    elif pressure < PRESSURE_ALERT_THRESHOLD:
        risk_factors += 2  # Warning pressure
    elif not OPTIMAL_PRESSURE_RANGE[0] <= pressure <= OPTIMAL_PRESSURE_RANGE[1]:
        risk_factors += 1  # Suboptimal pressure
    
    # Mileage analysis
    if mileage > HIGH_MILEAGE_THRESHOLD:
        risk_factors += 3  # Critical mileage
    elif mileage > MILEAGE_ALERT_THRESHOLD:
        risk_factors += 2  # Warning mileage
    
    # Temperature analysis
    if temp > CRITICAL_TEMP_THRESHOLD:
        risk_factors += 3  # Critical temperature
    elif temp > TEMP_ALERT_THRESHOLD:
        risk_factors += 2  # Warning temperature
    elif not OPTIMAL_TEMP_RANGE[0] <= temp <= OPTIMAL_TEMP_RANGE[1]:
        risk_factors += 1  # Suboptimal temperature
    
    # Multi-factor risk assessment
    if risk_factors >= 6:
        return "CRITICAL FAILURE IMMINENT", "red", "🛑"
    elif risk_factors >= 4:
        return "HIGH RISK: MULTIPLE FACTORS", "orange", "🚨"
    elif risk_factors >= 2:
        return "WARNING: ELEVATED RISK", "yellow", "⚠️"
    else:
        return "NORMAL OPERATING STATE", "green", "✅"

def calculate_business_metrics(pressure, mileage, temp, status_color):
    """Calculate realistic business metrics based on current state."""
    
    # Base efficiency (affected by pressure)
    pressure_efficiency = 1.0
    if pressure < OPTIMAL_PRESSURE_RANGE[0]:
        pressure_efficiency = 0.85 - (OPTIMAL_PRESSURE_RANGE[0] - pressure) * 0.03
    elif pressure > OPTIMAL_PRESSURE_RANGE[1]:
        pressure_efficiency = 0.95 - (pressure - OPTIMAL_PRESSURE_RANGE[1]) * 0.02
    
    # Fuel efficiency impact (realistic ranges)
    fuel_efficiency_impact = 0
    if pressure < OPTIMAL_PRESSURE_RANGE[0]:
        fuel_efficiency_impact = -((OPTIMAL_PRESSURE_RANGE[0] - pressure) * 2.5)  # 2.5% per PSI under
    elif pressure > OPTIMAL_PRESSURE_RANGE[1]:
        fuel_efficiency_impact = -((pressure - OPTIMAL_PRESSURE_RANGE[1]) * 1.0)  # 1% per PSI over
    
    # Maintenance cost savings (based on predictive capabilities)
    base_maintenance_cost = 1200
    if status_color == "green":
        maintenance_savings = base_maintenance_cost * 0.85  # 15% savings with good maintenance
        risk_score = random.randint(15, 25)
    elif status_color == "yellow":
        maintenance_savings = base_maintenance_cost * 0.70  # 30% savings with early detection
        risk_score = random.randint(35, 50)
    elif status_color == "orange":
        maintenance_savings = base_maintenance_cost * 0.50  # 50% savings by avoiding breakdown
        risk_score = random.randint(60, 75)
    else:
        maintenance_savings = base_maintenance_cost * 0.20  # 80% savings by preventing catastrophic failure
        risk_score = random.randint(85, 95)
    
    # Uptime calculation (affected by maintenance state)
    base_uptime = 97.5
    if status_color == "green":
        uptime = base_uptime + random.uniform(0.8, 1.5)
    elif status_color == "yellow":
        uptime = base_uptime - random.uniform(0.5, 1.2)
    elif status_color == "orange":
        uptime = base_uptime - random.uniform(2.0, 3.5)
    else:
        uptime = base_uptime - random.uniform(5.0, 8.0)
    
    return {
        "uptime": round(uptime, 1),
        "fuel_efficiency": round(max(-15, min(5, fuel_efficiency_impact)), 1),
        "maintenance_savings": int(maintenance_savings),
        "risk_score": risk_score,
        "pressure_efficiency": pressure_efficiency
    }

@st.cache_data
def generate_simulation_data():
    """Generates realistic simulation data with proper wear patterns."""
    data = []
    pressure_start = 33.5  # Start at optimal pressure
    temp_start = 45.0      # Start at normal operating temp
    mileage_start = 0
    
    # Realistic wear simulation
    for i in range(150): 
        # Pressure decreases gradually with some randomness
        pressure_wear = random.uniform(0.08, 0.25)  # Realistic pressure loss per interval
        if mileage_start > 25000:  # Increased wear after 25k km
            pressure_wear *= 1.3
        pressure_start -= pressure_wear
        
        # Temperature fluctuates based on mileage and pressure
        temp_change = random.uniform(-2, 4)
        if pressure_start < 30:  # Lower pressure increases temperature
            temp_change += random.uniform(1, 3)
        if mileage_start > 30000:  # Older tires run hotter
            temp_change += random.uniform(0.5, 2)
        temp_start = max(25, min(95, temp_start + temp_change))
        
        # Mileage accumulation
        mileage_start += random.uniform(250, 600)  # Realistic distance intervals
        
        # Stop simulation if pressure critically low or temperature critically high
        if pressure_start < WEAR_THRESHOLD_PRESSURE - 2 or temp_start > CRITICAL_TEMP_THRESHOLD + 5:
            break 
    
    df = pd.DataFrame(data, columns=['Mileage (km)', 'Pressure (PSI)', 'Temperature (°C)'])
    return df

df_sim = generate_simulation_data()

# --- 2. LIGHT THEME UI: Professional and High-Contrast (Sleek CSS) ---
st.markdown("""
<style>
/* 1. BASE THEME: Light Gray Background, Compact Text */
.main {
    background-color: #F8F8F8; 
    color: #111111; 
    padding-top: 0.5rem;
}

/* 2. HEADER & TITLE: Deep Blue Accent for professionalism */
h1 {
    color: #000080; 
    font-weight: 900;
    margin-bottom: 0px;
    padding-bottom: 0px;
}
h3 {
    color: #000080; 
    font-weight: 700;
    border-bottom: 2px solid #ADD8E6; 
    padding-bottom: 3px;
    margin-bottom: 0.5rem;
    font-size: 1.2em; /* Smaller for compactness */
}
h4 { /* For the ROI box */
    margin: 0;
}

/* 3. CONTAINERS & METRICS: Clean, sharp boxes */
.stMetric {
    background-color: #FFFFFF;
    padding: 8px; /* Reduced padding for compactness */
    border-radius: 8px;
    border: 1px solid #000080; 
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05); 
    margin-bottom: 5px;
}
.stMetric > div:nth-child(1) > div:nth-child(1) {
    font-size: 1.6em; /* Slightly smaller metric value */
    color: #000080; 
    font-weight: 700;
}

/* 4. COMPACT WIDGETS */
.stSlider {
    margin-bottom: 5px;
}

/* 6. ELIMINATE ALL WHITESPACE (CRITICAL FOR NO-SCROLL) */
div.block-container {
    padding-top: 0.5rem;
    padding-bottom: 0.5rem;
    padding-left: 1rem;
    padding-right: 1rem;
}

/* 7. COMPACT COLUMNS AND LAYOUT */
[data-testid="column"] {
    padding: 0.4rem; /* Reduced column padding */
}

/* 8. CUSTOM COMPONENTS */
.digital-twin-container {
    border: 2px solid #000080; 
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 128, 0.2);
    overflow: hidden;
    margin-bottom: 5px;
}

.cyber-divider {
    height: 2px;
    background: linear-gradient(90deg, transparent, #ADD8E6, transparent);
    margin: 3px 0; /* Reduced margin */
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

/* 10. INTRO BOX STYLE */
.intro-box {
    font-size: 0.9em;
    padding: 8px;
    border: 1px solid #000080;
    border-radius: 5px;
    background-color: #E6F7FF; /* Very light blue background */
    margin-bottom: 5px;
}

/* 11. REALISTIC GAUGE STYLES */
.gauge-container {
    background: #E0E0E0; 
    border-radius: 10px; 
    padding: 5px; 
    margin-bottom: 15px;
    border: 1px solid #000080;
}
.gauge-optimal-range {
    background: rgba(60, 179, 113, 0.3);
    height: 15px;
    border-radius: 6px;
    position: absolute;
    z-index: 1;
}
</style>
""", unsafe_allow_html=True)

# --- 3. COMPACT LAYOUT: Single Page, No Scroll ---
# FIX: Increased column width for the title to prevent cutoff. (From [3, 1] to [4, 1])
header_col1, header_col2 = st.columns([4, 1])

with header_col1:
    st.markdown("# 🚀 META 4.0 DIGITAL TWIN COMMAND CENTER")
    st.markdown("### Prescriptive Maintenance Intelligence Platform")
    
# --- INTRO / CONTEXT SECTION (Sleek, direct, non-bolded text) ---
st.markdown("""
<div class='intro-box'>
   <b>Problem:</b> Asset failures lead to unplanned downtime and high maintenance costs.<br>
<b>Solution:</b> This platform utilizes a Digital Twin fed by Real-Time Telemetry to predict component wear, enabling Prescriptive Maintenance before failure occurs.
</div>
""", unsafe_allow_html=True)
st.markdown('<div class="cyber-divider"></div>', unsafe_allow_html=True)

# Get current status with realistic default values
sim_mileage = 18500
sim_pressure = 32.2
sim_temp = 52.5

# Main Dashboard Grid - Single View, No Scroll
main_col1, main_col2, main_col3, main_col4 = st.columns([2.5, 1.3, 2.0, 1.5]) 

# --- COLUMN 4: I/O SIMULATOR (COMPACT CONTROLS) ---
with main_col4:
    st.markdown("### I/O SIMULATOR")
    st.caption("Test different operational scenarios")
    
    # Realistic slider ranges
    sim_mileage = st.slider("Mileage (km)", 0, 50000, 18500, 500, 
                           help="Typical tire lifespan: 40,000 km")
    sim_pressure = st.slider("Pressure (PSI)", 20.0, 45.0, 32.2, 0.1,
                            help="Optimal range: 30-35 PSI, Critical: <28 PSI")
    sim_temp = st.slider("Temperature (°C)", 20.0, 100.0, 52.5, 0.5,
                        help="Optimal range: 40-65°C, Critical: >80°C")

# Calculate status and business metrics
status_text, status_color, status_icon = predict_wear_and_status(sim_pressure, sim_mileage, sim_temp)
business_metrics = calculate_business_metrics(sim_pressure, sim_mileage, sim_temp, status_color)

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
    
    # Calculate optimal range positions for gauges
    pressure_optimal_start = ((OPTIMAL_PRESSURE_RANGE[0] - 20) / (45 - 20)) * 100
    pressure_optimal_width = ((OPTIMAL_PRESSURE_RANGE[1] - OPTIMAL_PRESSURE_RANGE[0]) / (45 - 20)) * 100
    
    temp_optimal_start = ((OPTIMAL_TEMP_RANGE[0] - 20) / (100 - 20)) * 100
    temp_optimal_width = ((OPTIMAL_TEMP_RANGE[1] - OPTIMAL_TEMP_RANGE[0]) / (100 - 20)) * 100
    
    # Pressure Gauge with optimal range indicator
    pressure_percent = max(0, min(100, (sim_pressure - 20) / (45 - 20) * 100))
    pressure_color = "#3CB371" if OPTIMAL_PRESSURE_RANGE[0] <= sim_pressure <= OPTIMAL_PRESSURE_RANGE[1] else "#FFA500"
    pressure_color = "#FF4500" if sim_pressure < WEAR_THRESHOLD_PRESSURE else pressure_color
    
    st.markdown(f"**PRESSURE:** **{sim_pressure}** PSI")
    st.markdown(f"""
    <div class="gauge-container" style="position: relative;">
        <div class="gauge-optimal-range" style="left: {pressure_optimal_start}%; width: {pressure_optimal_width}%;"></div>
        <div style="background: linear-gradient(90deg, {pressure_color} {pressure_percent}%, transparent {pressure_percent}%); 
                    height: 15px; border-radius: 6px; border: 1px solid #000080; position: relative; z-index: 2;"></div>
    </div>
    """, unsafe_allow_html=True)
    st.caption(f"Optimal: {OPTIMAL_PRESSURE_RANGE[0]}-{OPTIMAL_PRESSURE_RANGE[1]} PSI")
    
    # Temperature Gauge with optimal range indicator
    temp_percent = max(0, min(100, (sim_temp - 20) / (100 - 20) * 100))
    temp_color = "#3CB371" if OPTIMAL_TEMP_RANGE[0] <= sim_temp <= OPTIMAL_TEMP_RANGE[1] else "#FFA500"
    temp_color = "#FF4500" if sim_temp > CRITICAL_TEMP_THRESHOLD else temp_color
    
    st.markdown(f"**TEMPERATURE:** **{sim_temp}**°C")
    st.markdown(f"""
    <div class="gauge-container" style="position: relative;">
        <div class="gauge-optimal-range" style="left: {temp_optimal_start}%; width: {temp_optimal_width}%;"></div>
        <div style="background: linear-gradient(90deg, {temp_color} {temp_percent}%, transparent {temp_percent}%); 
                    height: 15px; border-radius: 6px; border: 1px solid #000080; position: relative; z-index: 2;"></div>
    </div>
    """, unsafe_allow_html=True)
    st.caption(f"Optimal: {OPTIMAL_TEMP_RANGE[0]}-{OPTIMAL_TEMP_RANGE[1]}°C")
    
    # Mileage Gauge
    mileage_percent = max(0, min(100, sim_mileage / 50000 * 100))
    mileage_color = "#3CB371" if sim_mileage < MILEAGE_ALERT_THRESHOLD else "#FFA500"
    mileage_color = "#FF4500" if sim_mileage > HIGH_MILEAGE_THRESHOLD else mileage_color
    
    st.markdown(f"**MILEAGE:** **{sim_mileage}** km")
    st.markdown(f"""
    <div class="gauge-container">
        <div style="background: linear-gradient(90deg, {mileage_color} {mileage_percent}%, #BBBBBB {mileage_percent}%); 
                    height: 15px; border-radius: 6px; border: 1px solid #000080;"></div>
    </div>
    """, unsafe_allow_html=True)
    st.caption(f"Alert at: {MILEAGE_ALERT_THRESHOLD:,} km")

# --- COLUMN 3: PRESCRIPTIVE ANALYTICS & QUICK METRICS ---
with main_col3:
    st.markdown("### PRESCRIPTIVE ANALYTICS")
    
    # Alert Display with realistic recommendations
    if status_color == "green":
        st.success(f"**{status_icon} {status_text}**")
        st.markdown("**Action:** Continue normal operations. Next inspection: **30 days**.")
        st.markdown("**Maintenance Impact:** Optimal performance, maximum cost savings")
    elif status_color == "yellow":
        st.warning(f"**{status_icon} {status_text}**")
        st.markdown("**Action:** Schedule inspection within **7 days**. Risk level: **Medium**.")
        st.markdown("**Maintenance Impact:** Early detection prevents 60% of potential failures")
    elif status_color == "orange":
        st.error(f"**{status_icon} {status_text}**")
        st.markdown("**Action:** **Urgent maintenance required within 48h**. Risk level: **High**.")
        st.markdown("**Maintenance Impact:** Preventive action avoids 85% of breakdown costs")
    else:
        st.error(f"**{status_icon} {status_text}**")
        st.markdown("**Action:** **IMMEDIATE SHUTDOWN REQUIRED**. Impending failure.")
        st.markdown("**Maintenance Impact:** Critical intervention prevents catastrophic failure")
    
    st.markdown('<div class="cyber-divider"></div>', unsafe_allow_html=True)
    
    # Realistic Performance Metrics
    st.markdown("### PERFORMANCE METRICS")
    col_a, col_b = st.columns(2)
    with col_a:
        uptime_delta = f"{business_metrics['uptime'] - 97.5:+.1f}%" if business_metrics['uptime'] != 97.5 else "0.0%"
        st.metric("Uptime", f"{business_metrics['uptime']}%", uptime_delta)
        
        fuel_delta = f"{business_metrics['fuel_efficiency']:+.1f}%"
        st.metric("Fuel Efficiency", f"{business_metrics['fuel_efficiency']}%", fuel_delta)
        
    with col_b:
        st.metric("Cost Avoided", f"${business_metrics['maintenance_savings']:,}", 
                 f"+{business_metrics['maintenance_savings']/BASE_MAINTENANCE_COST*100:.0f}%")
        
        risk_delta = f"{business_metrics['risk_score'] - 50:+.0f}" if business_metrics['risk_score'] != 50 else "0"
        st.metric("Risk Score", f"{business_metrics['risk_score']}/100", risk_delta)

# --- 5. BOTTOM SECTION: COMPACT TREND & ROI (Full Width) ---
st.markdown('<div class="cyber-divider"></div>', unsafe_allow_html=True)

trend_col1, trend_col2 = st.columns([4, 1])

with trend_col1:
    st.markdown("### ASSET HEALTH TREND ANALYSIS")
    
    # Plotly Dual-Axis Setup
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # Trace 1: Pressure (Primary Y-axis)
    fig.add_trace(go.Scatter(
        x=df_sim['Mileage (km)'], 
        y=df_sim['Pressure (PSI)'], 
        name='Pressure (PSI)',
        line=dict(color='#000080', width=3),
        fill='tozeroy',
        fillcolor='rgba(0, 0, 128, 0.1)'
    ), secondary_y=False) 
    
    # Trace 2: Temperature (Secondary Y-axis)
    fig.add_trace(go.Scatter(
        x=df_sim['Mileage (km)'], 
        y=df_sim['Temperature (°C)'], 
        name='Temperature (°C)',
        line=dict(color='#800080', width=3)
    ), secondary_y=True) 
    
    # Add horizontal critical lines
    fig.add_hline(
        y=WEAR_THRESHOLD_PRESSURE, 
        line_dash="dash", 
        line_color="#FF4500",
        annotation_text="CRITICAL PRESSURE",
        annotation_font_color="#FF4500",
        secondary_y=False
    )
    
    fig.add_hline(
        y=CRITICAL_TEMP_THRESHOLD, 
        line_dash="dash", 
        line_color="#FF4500",
        annotation_text="CRITICAL TEMP",
        annotation_font_color="#FF4500",
        secondary_y=True
    )
    
    # Apply general layout settings
    fig.update_layout(
        height=250,
        margin=dict(l=20, r=50, t=20, b=20),
        plot_bgcolor='#FFFFFF',
        paper_bgcolor='#F8F8F8',
        font_color='#111111',
        showlegend=True,
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1
        ),
        xaxis=dict(gridcolor='#E0E0E0', title="Mileage (km)"),
    )
    
    # Apply y-axis settings
    fig.update_yaxes(
        title_text="Pressure (PSI)", title_font=dict(color="#000080"), tickfont=dict(color="#000080"), 
        gridcolor='#E0E0E0', secondary_y=False 
    )
    fig.update_yaxes(
        title_text="Temperature (°C)", title_font=dict(color="#800080"), tickfont=dict(color="#800080"),
        gridcolor='#E0E0E0', showgrid=False, secondary_y=True 
    )
    
    st.plotly_chart(fig, use_container_width=True)

with trend_col2:
    st.markdown("### STRATEGIC ROI")
    st.markdown("""
    <div style="background: #FFFFFF; border-radius: 10px; padding: 15px; border: 1px solid #000080; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);">
    <h4 style="color: #3CB371; margin: 0;">📈 20-25%</h4>
    <p style="margin: 5px 0 10px 0; font-size: 0.8em; color: #111111;">Reduction in Downtime</p>
    
    <h4 style="color: #3CB371; margin: 0;">💰 15-20%</h4>
    <p style="margin: 5px 0 10px 0; font-size: 0.8em; color: #111111;">Maintenance Cost Savings</p>

    <h4 style="color: #3CB371; margin: 0;">⛽ 3-8%</h4>
    <p style="margin: 5px 0 10px 0; font-size: 0.8em; color: #111111;">Fuel Efficiency Gain</p>
    
    <h4 style="color: #3CB371; margin: 0;'>🛡️ 72h</h4>
    <p style="margin: 5px 0; font-size: 0.8em; color: #111111;">Predictive Lead Time</p>
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
