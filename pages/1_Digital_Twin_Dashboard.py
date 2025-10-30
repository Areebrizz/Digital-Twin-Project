import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import streamlit.components.v1 as components # Native HTML embedding for 3D

# --- CONFIGURATION & FUTURISTIC CSS (Must be repeated for the page to inherit styling) ---
st.set_page_config(
    page_title="Digital Twin Dashboard",
    page_icon="📈",
    layout="wide"
)

st.markdown("""
<style>
/* Base Dark Theme */
.main {
    background-color: #0d1117; 
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
    background-color: #010409; 
    color: #92e0ff;
    border-right: 2px solid #00FFFF;
}
</style>
""", unsafe_allow_html=True)


# --- 2. DATA GENERATION (Keep this section intact) ---
@st.cache_data
def generate_data():
    """Generates a synthetic dataset for tire health monitoring."""
    np.random.seed(42)
    num_samples = 2000
    
    # Features
    mileage = np.random.uniform(5000, 80000, num_samples)
    pressure = np.random.normal(32, 2, num_samples)
    temperature = np.random.normal(50, 10, num_samples)
    vibration = np.random.normal(15, 5, num_samples)
    
    # Target (Failure Modes)
    failure_mode = np.array(['Normal'] * num_samples, dtype=object)
    
    # Rule-based failure injection (This is the "prehistoric data" logic)
    # Pressure Loss
    pressure_loss_indices = (pressure < 29) & (mileage > 30000)
    failure_mode[pressure_loss_indices] = 'Pressure Loss'
    temperature[pressure_loss_indices] *= 1.1 
    vibration[pressure_loss_indices] *= 1.2

    # Overheat
    overheat_indices = (temperature > 75)
    failure_mode[overheat_indices] = 'Overheat'
    pressure[overheat_indices] *= 1.15
    vibration[overheat_indices] *= 1.3

    # Impact/Fatigue (High Vibration)
    impact_indices = (vibration > 30) & (mileage > 40000)
    failure_mode[impact_indices] = 'Impact/Fatigue'
    temperature[impact_indices] *= 1.2

    df = pd.DataFrame({
        'Mileage (km)': mileage,
        'Pressure (PSI)': pressure,
        'Temperature (C)': temperature,
        'Vibration (Hz)': vibration,
        'Failure Mode': failure_mode
    })
    return df

# --- 3. MACHINE LEARNING MODEL (Keep this section intact) ---
@st.cache_resource
def train_model(df):
    """Trains a RandomForestClassifier on the synthetic data."""
    features = ['Mileage (km)', 'Pressure (PSI)', 'Temperature (C)', 'Vibration (Hz)']
    target = 'Failure Mode'
    
    X = df[features]
    y = df[target]
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    accuracy = model.score(X_test, y_test)
    return model, accuracy

# --- 4. LOAD DATA AND TRAIN MODEL ---
df = generate_data()
model, accuracy = train_model(df)


# --- 5. STREAMLIT APP LAYOUT ---

st.title("Digital Twin Predictive Dashboard")
st.markdown("### Real-Time Prescriptive Maintenance Console")
st.markdown("---")

# --- SIDEBAR (Live Simulator) ---
st.sidebar.header("ASSET SIMULATOR (IoT Data Feed)")
st.sidebar.markdown("Manipulate the parameters to test the predictive boundaries of the ML model.")

# Sliders for user input
sim_mileage = st.sidebar.slider("Mileage (km)", 5000, 80000, 50000)
sim_pressure = st.sidebar.slider("Pressure (PSI)", 20.0, 45.0, 32.0, 0.5)
sim_temp = st.sidebar.slider("Temperature (C)", 20.0, 100.0, 50.0, 1.0)
sim_vibration = st.sidebar.slider("Vibration (Hz)", 5.0, 50.0, 15.0, 0.5)

# Package inputs for the model
input_data = pd.DataFrame({
    'Mileage (km': [sim_mileage],
    'Pressure (PSI)': [sim_pressure],
    'Temperature (C)': [sim_temp],
    'Vibration (Hz)': [sim_vibration]
})

# --- PREDICTION ---
prediction = model.predict(input_data)[0]
probabilities = model.predict_proba(input_data)
prob_df = pd.DataFrame(probabilities, columns=model.classes_).T
prob_df.columns = ['Probability']
prob_df = prob_df.sort_values(by='Probability', ascending=False)

# --- DASHBOARD (Main Page) ---
tab1, tab2, tab3 = st.tabs(["Real-Time Health", "Diagnostic Analysis", "3D Twin Visualization"])

# --- TAB 1: ASSET HEALTH MONITOR ---
with tab1:
    st.header("Asset Condition: Predictive Outcome")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Current Operational Status")
        
        # Display the prediction with color and actionable instruction
        if prediction == 'Normal':
            st.success(f"✅ **STATUS: NORMAL OPERATION**")
            st.markdown("Asset metrics are within optimal, safe bounds. Continue monitoring.")
        elif prediction == 'Pressure Loss':
            st.warning(f"⚠️ **STATUS: INITIATING PRESSURE LOSS EVENT**")
            st.markdown("**PRESCRIPTION:** Immediate pressure check recommended. Potential slow leak detected. <span style='color:orange;'>Service Alert Level 2.</span>", unsafe_allow_html=True)
        elif prediction == 'Overheat':
            st.error(f"🔥 **STATUS: CRITICAL OVERHEAT FAULT**")
            st.markdown("**PRESCRIPTION:** **Stop Vehicle Immediately.** Investigate excessive friction, alignment, or bearing failure. <span style='color:red; font-weight:bold;'>Critical Alert Level 1.</span>", unsafe_allow_html=True)
        elif prediction == 'Impact/Fatigue':
            st.warning(f"💥 **STATUS: STRUCTURAL FATIGUE DETECTED**")
            st.markdown("**PRESCRIPTION:** Schedule structural inspection. High vibration suggests impact damage or imbalance. <span style='color:yellow;'>Service Alert Level 2.</span>", unsafe_allow_html=True)

    with col2:
        st.subheader("ML Confidence Score")
        st.dataframe(prob_df.style.format("{:.1%}"))
        
    st.markdown("---")
    st.subheader("Multivariate Feature Correlation Map")
    st.markdown("This plot illustrates the relationship between key variables across the historical data, with the live asset's position (red star) overlaid.")
    
    # Plotly Chart
    fig = px.scatter(df, x='Temperature (C)', y='Pressure (PSI)', color='Failure Mode',
                     title="Feature Space Mapping: Temperature vs. Pressure",
                     color_discrete_map={
                         'Normal': '#4CAF50', # Green
                         'Pressure Loss': '#FFA500', # Orange
                         'Overheat': '#FF0000', # Red
                         'Impact/Fatigue': '#00FFFF' # Cyan
                     })
    # Add the simulated point
    fig.add_trace(go.Scatter(x=[sim_temp], y=[sim_pressure], mode='markers',
                             marker=dict(color='red', size=20, symbol='star', line=dict(width=2, color='black')),
                             name='Live Asset Data'))
                             
    fig.update_layout(plot_bgcolor='#1e2329', paper_bgcolor='#161b22', font_color='#f0f6fc')
    st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: FAILURE MODE ANALYSIS ---
with tab2:
    st.header("ML Model Performance & Training Data")
    st.markdown("The Random Forest classifier was trained on 2,000 synthetic data points to achieve robust multi-class separation.")
    
    st.metric("Model Classification Accuracy (Test Set)", f"{accuracy:.2%}", delta_color="normal")
    
    st.markdown("---")
    st.subheader("Historical Failure Distribution (3D Visualization)")
    st.markdown("The 3D feature space confirms the separability of the four primary operational states for effective classification.")
    fig2 = px.scatter_3d(df.sample(1000), x='Mileage (km)', y='Vibration (Hz)', z='Temperature (C)',
                        color='Failure Mode', title="3D Feature Space: Historical Failure Clustering")
    
    fig2.update_layout(scene=dict(bgcolor='#1e2329'), paper_bgcolor='#161b22', font_color='#f0f6fc')
    st.plotly_chart(fig2, use_container_width=True)

# --- TAB 3: 3D TWIN VIEW (Native HTML Fix) ---
with tab3:
    st.header("Live 3D Digital Twin Visualization")
    st.markdown("The virtual twin provides a unified view, reflecting the predicted operational status.")
    
    col_3d, col_status = st.columns([2, 1])
    
    with col_3d:
        st.subheader(f"Asset Model: {prediction} State")
        
        # Public GLTF model from modelviewer.dev - REPLACE WITH YOUR OWN MODEL URL LATER
        model_path = "https://modelviewer.dev/shared-assets/models/gltf/RobotExpressive.glb" 

        # The HTML component uses the <model-viewer> web standard for 3D rendering
        html_code = f"""
        <!-- Load the model-viewer web component library -->
        <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.5.0/model-viewer.min.js"></script>
        
        <!-- The actual 3D viewer tag -->
        <model-viewer 
            src="{model_path}"
            alt="A 3D Model of the Digital Twin Tire"
            auto-rotate 
            camera-controls 
            ar
            style="width: 100%; height: 500px; border-radius: 10px; background-color: #1e2329; box-shadow: 0 0 20px rgba(0, 255, 255, 0.5);"
            shadow-intensity="1"
            >
        </model-viewer>
        """
        
        # Embed the component using the native Streamlit HTML function
        components.html(html_code, height=500)


    with col_status:
        st.subheader("Summary")
        
        if prediction == 'Normal':
            st.success(f"**STATUS: {prediction}**")
            st.info("System is Green. Data integrity confirmed.")
        elif prediction == 'Pressure Loss':
            st.warning(f"**STATUS: {prediction}**")
            st.error("System is Orange. Proactive maintenance required.")
        elif prediction == 'Overheat':
            st.error(f"**STATUS: {prediction}**")
            st.error("System is Red. Immediate shutdown protocol.")
        else:
            st.warning(f"**STATUS: {prediction}**")
            st.info("System is Yellow. Scheduled diagnostic is pending.")
            
        st.markdown("---")
        st.subheader("IoT Input Metrics")
        st.metric("Pressure", f"{sim_pressure} PSI")
        st.metric("Temperature", f"{sim_temp}° C")
        st.metric("Vibration", f"{sim_vibration} Hz")
