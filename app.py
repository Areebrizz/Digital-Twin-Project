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
/* Base Dark Theme (Deep Charcoal Black) */
.main {
    background-color: #0d1117; 
    color: #f0f6fc;
}

/* Header & Title Glow (Cyan/Green Accent) */
h1, h2, h3 {
    color: #4CAF50; 
    text-shadow: 0 0 5px #00FFFF, 0 0 10px #00FFFF, 0 0 15px #00FFFF; /* Stronger Cyan Glow */
}

/* Metric Boxes and Containers */
.stMetric {
    background-color: #161b22;
    padding: 15px;
    border-radius: 10px;
    border-left: 5px solid #00FFFF; /* Cyan highlight */
    box-shadow: 0 4px 20px rgba(0, 255, 255, 0.3); /* Stronger shadow */
    transition: all 0.3s;
}

/* Sidebar Customization */
[data-testid="stSidebar"] {
    background-color: #010409; 
    color: #92e0ff;
    border-right: 2px solid #00FFFF;
}

/* Divider Line */
hr {
    border-top: 3px solid #4CAF50; /* Green Divider */
    opacity: 0.7;
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
    box-shadow: 0 0 20px rgba(76, 175, 80, 0.4);
}
.logo-box {
    text-align: center;
    color: #f0f6fc;
    font-size: 0.9em;
}

/* Specific text color for project value */
.value-text {
    color: #FFD700; /* Gold for emphasis */
    font-weight: bold;
    font-size: 1.1em;
}

/* Center elements */
.stImage {
    text-align: center !important;
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
    st.markdown("#### **Strategic Business Impact (ROI)**")
    st.markdown("""
    This project demonstrates a fully functional **Prescriptive Maintenance** solution, a cornerstone of **Industry 4.0**. Based on fleet simulations, the estimated value proposition includes:
    * <span class="value-text">20% Reduction in Unplanned Vehicle Downtime</span>
    * <span class="value-text">15% Optimization of Fleet Maintenance Spends (Tyre Lifetime)</span>
    * <span class="value-text">Improved Fleet Safety & Compliance</span>
    """, unsafe_allow_html=True)
    st.caption("Value driven by predicting failure modes days in advance, not hours.")

with col_creator:
    st.markdown("#### **Creator & Technical Competency**")
    st.markdown(f"""
    Project Architect: **[Your Name Here]**
    * **ML & Data Science:** Predictive Multi-class Classification (Random Forest), Feature Engineering.
    * **Cloud & DevOps:** Full-Stack Data Application Development (Streamlit), Deployment on Streamlit Community Cloud.
    * **Visualization:** Advanced Interactive Plotly charts and **Native 3D Digital Twin Integration** (Web Component).
    """)

st.markdown("---")

# --- INDUSTRY PARTNERS ---
st.header("2. Industry Collaboration & Context")

st.markdown("#### **Real-World Application Partners**")

st.markdown("""
<div class="logo-container">
    <div class="logo-box">
        <img src="https://placehold.co/150x80/0d1117/28a745?text=Master%20Motors" style="border-radius: 5px; border: 2px solid #28a745;">
        <p>Strategic Automotive Partner: **Master Motors**</p>
    </div>
    <div class="logo-box">
        <img src="https://placehold.co/150x80/0d1117/007bff?text=Tristar%20Transport" style="border-radius: 5px; border: 2px solid #007bff;">
        <p>Logistics & Fleet Partner: **Tristar Transport**</p>
    </div>
</div>
<p style='text-align: center;'>This solution directly addresses operational continuity challenges in heavy logistics, transforming sensor data into actionable financial intelligence for our partners.</p>
""", unsafe_allow_html=True)
st.markdown("---")

# --- PROBLEM AND SOLUTION ---
st.header("3. Digital Twin: Problem and Prescriptive Solution")
col_p, col_s = st.columns(2)

with col_p:
    st.subheader("The **4.0 Problem**: Reactive Maintenance")
    st.image("https://placehold.co/600x200/FF0000/FFFFFF?text=HIGH+RISK+%7C+COSTLY+DOWNTIME", 
             caption="Latent failures and catastrophic blowouts driven by unseen multivariate stress.",
             use_column_width=True)
    st.write("""
    Existing systems are **reactive**, only flagging critical failures *after* they occur. The key challenge is correlating subtle, simultaneous anomalies (e.g., small pressure drop + high vibration) to predict the **mode** of failure before physical damage is done.
    """)

with col_s:
    st.subheader("The **Digital Twin Solution**: Prescriptive Intelligence")
    st.image("https://placehold.co/600x200/00FFFF/161b22?text=PREDICTIVE+%7C+OPTIMIZED+ACTION", 
             caption="Fusion of ML Prediction and 3D Visualization for Decision Support.",
             use_column_width=True)
    st.write("""
    The Smart Tire Digital Twin is a **virtual fusion model**. It ingests live IoT data, runs it through a robust Machine Learning classifier, and provides a clear, preemptive diagnosis. This allows maintenance teams to act with **prescriptive intelligence**.
    """)

# --- CALL TO ACTION ---
st.markdown("---")
st.success("### 🚀 Navigate to 'Digital Twin Dashboard' to interact with the live simulation and predictive twin!")
