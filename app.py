import streamlit as st

# --- CONFIGURATION & FUTURISTIC CSS ---
st.set_page_config(
    page_title="Erasmus Meta 4.0 Digital Twin",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
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

# --- SIDEBAR NAVIGATION & META DATA ---
st.sidebar.title("Erasmus Meta 4.0")
st.sidebar.markdown("### Digital Twin Implementation")
st.sidebar.info("Navigate to the **Digital Twin Dashboard** page to access the live predictive model and 3D visualization.")

# --- MAIN PAGE CONTENT ---
st.title("Digital Twin for Predictive Tire Maintenance")
st.header("Executive Project Overview for Meta 4.0")

st.markdown("""
A high-fidelity Digital Twin solution integrating IoT data (Pressure, Temperature, Mileage) with a physics-based model to provide **Prescriptive Maintenance** alerts, reducing unscheduled downtime and optimizing fleet safety.
""")
st.markdown("---")

# --- CORE METRICS ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="Predicted Failure Reduction", value="20%", delta="Target 20% Increase in Uptime")
with col2:
    st.metric(label="IoT Data Streams Integrated", value="3", delta="Pressure, Temp, Mileage")
with col3:
    st.metric(label="Predictive Lead Time", value="72 Hours", delta="Pre-emptive vs. Reactive Maintenance")

st.markdown("---")

# --- PROJECT VALUE ---
st.header("1. Strategic Business Impact (ROI Case Study)")

col_value, col_tech = st.columns(2)

with col_value:
    st.markdown("#### **Financial & Operational Upside**")
    st.markdown("""
    This project is a high-fidelity demonstration of **Industry 4.0** principles, transforming operational data into **Prescriptive Intelligence** for Master Motors & Tristar Transport.
    * <span class="value-text">**20% Reduction** in Unplanned Vehicle Downtime</span>
    * <span class="value-text">**15% Optimization** of Tire Lifecycle Costs (Predictive Retirement)</span>
    * <span class="value-text">**Demonstration of Core Competency** for Erasmus Meta 4.0 Focus Areas</span>
    """, unsafe_allow_html=True)

with col_tech:
    st.markdown("#### **Technology Stack & Alignment**")
    st.markdown("""
    * **Digital Twin:** Real-time synchronization of physical asset state with virtual model.
    * **Visualization:** High-impact 3D rendering (WebGL/Model-Viewer).
    * **Predictive Model:** Custom physics-informed wear logic.
    * **Goal:** Shift maintenance from a **Cost Center** to a **Value Driver**.
    """)

st.markdown("---")
st.header("2. Project Showcase")
st.markdown("Click on the **Digital Twin Dashboard** page to interact with the live simulation and see the immediate impact of predictive analytics.")
