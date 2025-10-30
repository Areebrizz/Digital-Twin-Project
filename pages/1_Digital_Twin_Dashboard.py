import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go # Added for the scatter plot trace
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from st_web_component import st_web_component # NEW 3D LIBRARY

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Digital Twin Dashboard",
    page_icon="📈",
    layout="wide"
)

# --- 2. DATA GENERATION (Our "Excel File") ---
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
    temperature[pressure_loss_indices] *= 1.1 # Low pressure increases temp
    vibration[pressure_loss_indices] *= 1.2

    # Overheat
    overheat_indices = (temperature > 75)
    failure_mode[overheat_indices] = 'Overheat'
    pressure[overheat_indices] *= 1.15 # High temp increases pressure
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

# --- 3. MACHINE LEARNING MODEL ---
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

st.title("📈 Smart Tire Digital Twin Dashboard")
st.markdown("---")

# --- SIDEBAR (Live Simulator) ---
st.sidebar.header("LIVE ASSET SIMULATOR")
st.sidebar.markdown("Manually adjust sensor readings to see real-time failure prediction.")

# Sliders for user input
sim_mileage = st.sidebar.slider("Mileage (km)", 5000, 80000, 50000)
sim_pressure = st.sidebar.slider("Pressure (PSI)", 20.0, 45.0, 32.0, 0.5)
sim_temp = st.sidebar.slider("Temperature (C)", 20.0, 100.0, 50.0, 1.0)
sim_vibration = st.sidebar.slider("Vibration (Hz)", 5.0, 50.0, 15.0, 0.5)

# Package inputs for the model
input_data = pd.DataFrame({
    'Mileage (km)': [sim_mileage],
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
tab1, tab2, tab3 = st.tabs(["Asset Health Monitor", "Failure Mode Analysis", "3D Twin View"])

# --- TAB 1: ASSET HEALTH MONITOR ---
with tab1:
    st.header("Real-Time Asset Health")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Current Status: Prediction")
        
        # Display the prediction with color
        if prediction == 'Normal':
            st.success(f"✅ **Prediction: {prediction}**")
            st.markdown("Asset is operating within normal parameters. No failure is predicted.")
        elif prediction == 'Pressure Loss':
            st.warning(f"⚠️ **Prediction: {prediction}**")
            st.markdown("A slow leak or under-inflation is detected. **Action:** Inspect tire and re-inflate.")
        elif prediction == 'Overheat':
            st.error(f"🔥 **Prediction: {prediction}**")
            st.markdown("Dangerously high temperature detected. **Action:** Stop vehicle immediately to cool down. Check alignment and brakes.")
        elif prediction == 'Impact/Fatigue':
            st.warning(f"💥 **Prediction: {prediction}**")
            st.markdown("Excessive vibration indicates potential structural damage or imbalance. **Action:** Inspect for physical damage, check balancing.")

    with col2:
        st.subheader("Prediction Probability")
        st.markdown("The ML model's confidence in its prediction:")
        st.dataframe(prob_df.style.format("{:.1%}"))
        
    st.markdown("---")
    st.subheader("Live Sensor Data vs. Training Data")
    st.markdown("This chart shows where your simulated data point (red star) falls relative to the entire historical dataset.")
    
    # Plotly Chart
    fig = px.scatter(df, x='Temperature (C)', y='Pressure (PSI)', color='Failure Mode',
                     title="Temperature vs. Pressure (Historical Data)",
                     color_discrete_map={
                         'Normal': 'green',
                         'Pressure Loss': 'orange',
                         'Overheat': 'red',
                         'Impact/Fatigue': 'purple'
                     })
    # Add the simulated point
    fig.add_trace(go.Scatter(x=[sim_temp], y=[sim_pressure], mode='markers',
                             marker=dict(color='red', size=20, symbol='star', line=dict(width=2, color='black')),
                             name='Live Simulated Data'))
    st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: FAILURE MODE ANALYSIS ---
with tab2:
    st.header("Failure Mode Encyclopedia")
    st.markdown("This dashboard predicts four distinct states, including three critical failure modes.")
    
    st.subheader("1. Pressure Loss")
    st.image("https://media.istockphoto.com/id/1154564414/photo/flat-tire.jpg?s=1024x1024&w=is&k=20&c=i3h1-vIT2-RwpVO-N_2M8qLwn-vNMd86-Xv9i_iIsks=", 
             width=400, caption="Caused by punctures or slow leaks. Leads to instability and potential blowouts.")

    st.subheader("2. Overheat")
    st.markdown("Caused by high speed, heavy loads, under-inflation, or dragging brakes. Leads to rubber degradation and tread separation.")
    
    st.subheader("3. Impact / Fatigue")
    st.markdown("Caused by hitting potholes, curbs, or debris. Leads to internal structural damage, bulges, and potential blowouts.")
    
    st.markdown("---")
    st.header("Historical Data Explorer")
    st.markdown("Interact with the full dataset that the ML model was trained on.")
    fig2 = px.scatter_3d(df.sample(1000), x='Mileage (km)', y='Vibration (Hz)', z='Temperature (C)',
                        color='Failure Mode', title="3D View of Historical Failures")
    st.plotly_chart(fig2, use_container_width=True)

# --- TAB 3: 3D TWIN VIEW (FIXED) ---
with tab3:
    st.header("Live 3D Digital Twin Viewer")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"3D Model Status: {prediction}")
        
        # Using a public GLTF model from modelviewer.dev for guaranteed deployment compatibility
        model_path = "https://modelviewer.dev/shared-assets/models/gltf/RobotExpressive.glb" 

        # The HTML component uses the <model-viewer> web standard for 3D rendering
        html_code = f"""
        <script type="module" src="https://ajax.googleapis.com/ajax/libs/model-viewer/3.5.0/model-viewer.min.js"></script>
        <model-viewer 
            src="{model_path}"
            alt="A 3D Model of the Digital Twin Tire"
            auto-rotate 
            camera-controls 
            ar
            style="width: 100%; height: 500px; --progress-bar-color: red;"
            shadow-intensity="1"
            >
        </model-viewer>
        """
        
        # Embed the component
        st_web_component(html_code, height=500, key="3d_viewer")


    with col2:
        st.subheader("Linked Data")
        st.markdown("The 3D model is visually linked to the asset's current predicted status.")
        
        if prediction == 'Normal':
            st.success(f"**STATUS: {prediction}**")
        elif prediction == 'Pressure Loss' or prediction == 'Impact/Fatigue':
            st.warning(f"**STATUS: {prediction}**")
        else:
            st.error(f"**STATUS: {prediction}**")
            
        st.markdown("---")
        st.subheader("Model Accuracy")
        st.metric("Classifier Accuracy", f"{accuracy:.2%}")
        st.caption("This is the model's score on the 20% of data it had never seen before.")
