import streamlit as st

# --- CONFIGURATION & FUTURISTIC CSS ---
st.set_page_config(
    page_title="Executive Briefing: Smart Tire Digital Twin",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for Futuristic Dark Theme (Cyberpunk/Industry 4.0 style)
st.markdown("""
<style>
/* Base Dark Theme */
.main {
    background-color: #0d1117; /* Deep Charcoal Black */
    color: #f0f6fc;
}

/* Header & Title Glow */
h1, h2, h3 {
    color: #4CAF50; /* Green Accent */
    text-shadow: 0 0 5px #00FFFF, 0 0 10px #00FFFF; /* Cyan Glow */
}

/* Metric Boxes and Containers */
.stMetric {
    background-color: #161b22;
    padding: 15px;
    border-radius: 10px;
    border-left: 5px solid #00FFFF; /* Cyan highlight */
    box-shadow: 0 4px 15px rgba(0, 255, 255, 0.2);
    transition: all 0.3s;
}
.stMetric > div > div:nth-child(1) {
    font-size: 1.5rem;
    font-weight: 700;
}

/* Sidebar Customization */
[data-testid="stSidebar"] {
    background-color: #010409; /* Even darker sidebar */
    color: #92e0ff;
    border-right: 2px solid #00FFFF;
}

/* Divider Line */
hr {
    border-top: 2px solid #00FFFF;
    opacity: 0.5;
}

/* Logo container for better presentation */
.logo-container {
    display: flex;
    justify-content: space-around;
    align-items: center;
    padding: 20px;
    border-radius: 10px;
    background: linear-gradient(90deg, #161b22, #0d1117);
    margin-bottom: 30px;
    box-shadow: 0 0 15px rgba(76, 175, 80, 0.3);
}
.logo-box {
    text-align: center;
    color: #f0f6fc;
    font-size: 0.9em;
}

/* Specific text color for project value */
.value-text {
    color: #FFD700; /* Gold for value */
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.title("Digital Transformation: The Smart Tire Digital Twin")
st.markdown("### Executive Briefing for Meta 4.0 Erasmus Committee")
st.markdown("---")

# --- PROJECT VALUE AND CREATOR ---
st.header("1. Project & Personal Worth")

col_value, col_creator = st.columns(2)

with col_value:
    st.markdown("#### **Strategic Business Impact**")
    st.markdown(f"""
    This project is a high-fidelity demonstration of **Industry 4.0** principles, transforming operational data into **Prescriptive Intelligence**.
    The estimated value proposition for a typical fleet operation is a:
    -   <span class="value-text">20% Reduction in Unplanned Downtime</span>
    -   <span class="value-text">15% Optimization of Maintenance Costs</span>
    -   <span class="value-text">Significant Improvement in Fleet Safety</span>
    """, unsafe_allow_html=True)

with col_creator:
    st.markdown("#### **Creator & Technical Competency**")
    st.markdown(f"""
    Project Architect: **[Your Name Here]**
    -   **Skills Demonstrated:** Advanced Machine Learning (Predictive Classification), Full-Stack Data App Development (Streamlit, Plotly), Cloud Deployment, and Industrial Visualization (3D Digital Twin Integration).
    -   **Focus:** Bridging the gap between raw IoT data and executive decision-making.
    """)

st.markdown("---")

# --- INDUSTRY PARTNERS ---
st.header("2. Industry Collaboration & Context")

st.markdown("#### **Real-World Application Partners**")

st.markdown("""
<div class="logo-container">
    <div class="logo-box">
        <img src="https://placehold.co/120x80/28a745/ffffff?text=Master%20Motors%0ALogo" style="border-radius: 5px;">
        <p>Master Motors</p>
    </div>
    <div class="logo-box">
        <img src="https://placehold.co/120x80/007bff/ffffff?text=Tristar%20Transport%0ALogo" style="border-radius: 5px;">
        <p>Tristar Transport</p>
    </div>
</div>
<p>This solution directly addresses the operational continuity challenges faced by leading logistics and automotive firms, moving maintenance from reactive to proactive.</p>
""", unsafe_allow_html=True)
st.markdown("---")

# --- PROBLEM AND SOLUTION ---
st.header("3. The Core Challenge & Digital Twin Solution")
col_p, col_s = st.columns(2)

with col_p:
    st.subheader("The Challenge: Invisible Failure States")
    st.image("https://placehold.co/600x300/161b22/FFFFFF?text=Unplanned+Downtime+Diagram", 
             caption="The high cost of unexpected asset failure in fleet operations.",
             use_column_width=True)
    st.write("""
    Fleet operators suffer due to **latent failures**—subtle sensor anomalies that precede catastrophic events (e.g., small pressure fluctuations, unusual vibration patterns). Traditional systems fail to correlate these multivariate inputs, leading to high-risk and high-cost operational interruptions.
    """)

with col_s:
    st.subheader("The Solution: Predictive Digital Twin")
    st.image("https://placehold.co/600x300/00FFFF/161b22?text=Digital+Twin+Architecture+Diagram", 
             caption="Industry 4.0 architecture: IoT Data to Prescriptive Action.",
             use_column_width=True)
    st.write("""
    Our Digital Twin serves as a virtual counterpart to the physical asset (the tire). It uses **Machine Learning** to fuse four distinct sensor data streams (Pressure, Temperature, Vibration, Mileage) to achieve **multi-class classification** of failure modes, enabling maintenance to be performed precisely when needed.
    """)

# --- CALL TO ACTION ---
st.markdown("---")
st.success("### 🚀 Navigate to 'Digital Twin Dashboard' to experience the live simulation and predictive model in action!")
