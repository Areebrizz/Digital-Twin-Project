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

# Custom CSS for Futuristic Dark Theme (Must match app.py)
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

/* Sidebar Customization */
[data-testid="stSidebar"] {
    background-color: #010409; 
    color: #92e0ff;
    border-right: 2px solid #00FFFF;
}

/* Dataframe Styling for Dark Mode */
.stDataFrame {
    color: #f0f6fc;
    background-color: #161b22;
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)


# --- 2. DATA GENERATION (Keep intact) ---
@st.cache_data
def generate_data():
    np.random.seed(42)
    num_samples = 2000
    
    mileage = np.random.uniform(5000, 80000, num_samples)
    pressure = np.random.normal(32, 2, num_samples)
    temperature = np.random.normal(50, 10, num_samples)
    vibration = np.random.normal(15, 5, num_samples)
    
    failure_mode = np.array(['Normal'] * num_samples, dtype=object)
    
    # Rule-based failure injection
    pressure_loss_indices = (pressure < 29) & (mileage > 30000)
    failure_mode[pressure_loss_indices] = 'Pressure Loss'
    temperature[pressure_loss_indices] *= 1.1 
    vibration[pressure_loss_indices] *= 1.2

    overheat_indices = (temperature > 75)
    failure_mode[overheat_indices] = 'Overheat'
    pressure[overheat_indices] *= 1.15
    vibration[overheat_indices] *= 1.3

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

# --- 3. MACHINE LEARNING MODEL (Keep intact) ---
@st.cache_resource
def train_model(df):
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
    
    col1, col2 = st.columns([3, 2])
    
    with col1:
        st.subheader("Current Operational Status")
        
        # Display the prediction with color and actionable instruction
        if prediction == 'Normal':
            st.success(f"✅ **STATUS: NORMAL OPERATION (NOMINAL)**")
            st.markdown("<span style='color:#4CAF50; font-size:1.1em;'>**Prescription:** Continue optimal operation. System is stable.</span>", unsafe_allow_html=True)
        elif prediction == 'Pressure Loss':
            st.warning(f"⚠️ **STATUS: INITIATING PRESSURE LOSS EVENT**")
            st.markdown("<span style='color:#FFA500; font-size:1.1em;'>**Prescription:** Immediate pressure check and inspection for slow leaks. **Alert Level 2.**</span>", unsafe_allow_html=True)
        elif prediction == 'Overheat':
            st.error(f"🔥 **STATUS: CRITICAL OVERHEAT FAULT**")
            st.markdown("<span style='color:#FF0000; font-size:1.1em; font-weight:bold;'>**Prescription:** Emergency shutdown protocol. High risk of structural failure. **CRITICAL ALERT.**</span>", unsafe_allow_html=True)
        elif prediction == 'Impact/Fatigue':
            st.warning(f"💥 **STATUS: STRUCTURAL FATIGUE DETECTED**")
            st.markdown("<span style='color:#00FFFF; font-size:1.1em;'>**Prescription:** Schedule tire inspection and re-balancing to prevent further damage. **Alert Level 2.**</span>", unsafe_allow_html=True)

    with col2:
        st.subheader("ML Confidence Score")
        st.caption(f"Model Accuracy on Test Data: **{accuracy:.2%}**")
        st.dataframe(prob_df.style.format("{:.1%}").background_gradient(cmap='viridis'), use_container_width=True)
        
    st.markdown("---")
    st.subheader("Feature Space Mapping: Live Data Point Analysis")
    st.markdown("Visualizing the live sensor reading (red star) against the historical failure clusters (Training Data).")
    
    # Plotly Chart
    fig = px.scatter(df, x='Temperature (C)', y='Pressure (PSI)', color='Failure Mode',
                     title="Key Feature Correlation Map (Temperature vs. Pressure)",
                     color_discrete_map={
                         'Normal': '#4CAF50', 
                         'Pressure Loss': '#FFA500', 
                         'Overheat': '#FF0000', 
                         'Impact/Fatigue': '#00FFFF'
                     })
    # Add the simulated point
    fig.add_trace(go.Scatter(x=[sim_temp], y=[sim_pressure], mode='markers',
                             marker=dict(color='#FFD700', size=25, symbol='star', line=dict(width=3, color='black')),
                             name='LIVE ASSET POINT'))
                             
    fig.update_layout(plot_bgcolor='#1e2329', paper_bgcolor='#161b22', font_color='#f0f6fc', title_font_color='#f0f6fc')
    st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: DIAGNOSTIC ANALYSIS (Keep content structure) ---
with tab2:
    st.header("ML Model & Data Diagnostics")
    
    st.subheader("Failure Mode Encyclopedia")
    st.markdown("""
    The model classifies asset state into four classes, enabling targeted maintenance:
    * **Normal:** Optimal operating zone.
    * **Pressure Loss:** Signifies gradual leak or sustained under-inflation.
    * **Overheat:** Signifies excessive load or speed leading to material breakdown.
    * **Impact/Fatigue:** Signifies structural damage from external impact or excessive wear.
    """)
    
    st.markdown("---")
    st.subheader("Historical Failure Distribution (3D Feature Visualization)")
    fig2 = px.scatter_3d(df.sample(1000), x='Mileage (km)', y='Vibration (Hz)', z='Temperature (C)',
                        color='Failure Mode', title="3D Feature Space: Historical Failure Clustering")
    
    fig2.update_layout(scene=dict(bgcolor='#1e2329'), paper_bgcolor='#161b22', font_color='#f0f6fc', title_font_color='#f0f6fc')
    st.plotly_chart(fig2, use_container_width=True)

# --- TAB 3: 3D TWIN VIEW (Native HTML Fix) ---
with tab3:
    st.header("Asset 3D Twin Visualization: The Virtual Reality")
    st.markdown("The 3D model is the visual anchor of the Digital Twin, reflecting the predictive state in real-time.")
    
    col_3d, col_status = st.columns([2, 1])
    
    with col_3d:
        st.subheader(f"Virtual Twin State: {prediction}")
        
        # Public GLTF model from modelviewer.dev - REPLACE WITH YOUR OWN MODEL URL LATER
        model_path = "https://modelviewer.dev/shared-assets/models/gltf/RobotExpressive.glb" 

        # The HTML component uses the <model-viewer> web standard for 3D rendering
        html_code = f"""
        <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.5.0/model-viewer.min.js"></script>
        
        <model-viewer 
            src="{model_path}"
            alt="The Digital Twin Asset"
            auto-rotate 
            camera-controls 
            ar
            style="width: 100%; height: 500px; border-radius: 15px; background-color: #0d1117; box-shadow: 0 0 30px rgba(0, 255, 255, 0.5);"
            shadow-intensity="1"
            >
        </model-viewer>
        """
        
        # Embed the component using the native Streamlit HTML function
        components.html(html_code, height=500)


    with col_status:
        st.subheader("Live Operational Metrics")
        
        # Summary Status
        status_color = {'Normal': 'green', 'Pressure Loss': 'orange', 'Impact/Fatigue': 'yellow', 'Overheat': 'red'}.get(prediction, 'white')
        st.markdown(f"<p style='font-size: 1.5em; font-weight: bold; color: {status_color}; border-bottom: 3px solid {status_color}; padding-bottom: 5px;'>PREDICTED STATE: {prediction.upper()}</p>", unsafe_allow_html=True)
            
        st.markdown("---")
        st.subheader("Current IoT Readings")
        # Use st.metric for consistent styling
        st.metric("Pressure (PSI)", f"{sim_pressure}", delta="Optimal: 32.0", delta_color="off")
        st.metric("Temperature (°C)", f"{sim_temp}", delta="Max Safe: 70.0", delta_color="off")
        st.metric("Vibration (Hz)", f"{sim_vibration}", delta="Max Safe: 25.0", delta_color="off")
