import streamlit as st
import requests
from google import genai
from google.genai import types
from streamlit_lottie import st_lottie


# Lottie Animation Loader
def load_lottie(url):
    res = requests.get(url)
    if res.status_code != 200:
        return None
    return res.json()

# Lottie Animations
header_anim = load_lottie("https://lottie.host/6f6a89d9-7ee8-4dee-b1d8-64519202e300/9IsLLH0RoC.json")

# ────────────────────────────────
# Gemini API Initialization
API_KEY = "AIzaSyDuvEOiKijZDwTLoA9A90gf0DSVnU5VTdU"
client = genai.Client(api_key=API_KEY)

# ────────────────────────────────
# Function to create prompt for Gemini
def create_prompt(ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity):
    return f"""
        You are a water quality expert. Based on the following parameters, do the following:

        1. Predict whether the water is "Potable" or "Not Potable".
        2. If the water is "Not Potable", provide clear suggestions on what treatments are needed to make it potable in para only dont give it in bullet points.
        3. Keep your answer concise and structured.

        Water Quality Parameters:
        - pH: {ph}
        - Hardness: {hardness} mg/L
        - Solids: {solids} ppm
        - Chloramines: {chloramines} ppm
        - Sulfate: {sulfate} mg/L
        - Conductivity: {conductivity} μS/cm
        - Organic Carbon: {organic_carbon} mg/L
        - Trihalomethanes: {trihalomethanes} μg/L
        - Turbidity: {turbidity} NTU

        Return the result in the format:
        Prediction: [Potable/Not Potable]
        Treatment Suggestions: [If needed]
    """

# ────────────────────────────────
# Page Config & Styling
st.set_page_config(page_title="💧 AI Water Quality Predictor", layout="centered")
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Roboto', sans-serif;
        background: linear-gradient(to right, #dfe9f3, #ffffff);
    }
    
    .main-box:hover {
        transform: scale(1.02);
    }
    .stButton > button {
        background-color: #0F9D58;
        color: white;
        padding: 0.6rem 1.4rem;
        border-radius: 8px;
        border: none;
        font-size: 1rem;
        font-weight: bold;
        transition: 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #0c7b44;
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

# ────────────────────────────────
# UI Layout
with st.container():
    # st.markdown('<div class="main-box">', unsafe_allow_html=True)

    if header_anim:
        st_lottie(header_anim, height=200)

    st.title("💧 AI Water Quality Predictor")
    st.markdown("""
    <div style="font-size: 1.05rem; color: #333; margin-bottom: 1.2rem;">
        This AI-powered tool analyzes key water quality parameters to determine if water is safe for drinking. 
        It not only predicts potability but also offers treatment suggestions if the water is not potable.
    </div>
    """, unsafe_allow_html=True)

    # Highlighted explanation of terms
    st.markdown("""
    <div style="background-color: #f0f9ff; padding: 1rem; border-radius: 10px; border-left: 6px solid #2196F3; margin-bottom: 1.5rem;">
        <b style="color: #0b5394;">Potable</b> means the water is <b style="color: green;">safe to drink</b> without any treatment.<br>
        <b style="color: #a61c00;">Not Potable</b> means the water is <b style="color: red;">unsafe to drink</b> and needs treatment.
    </div>
    """, unsafe_allow_html=True)
    st.markdown("Enter the water quality parameters below to check if the water is potable:")

    # Input Fields
    ph = st.number_input("pH", 0.0, 14.0, 7.0)
    hardness = st.number_input("Hardness (mg/L)", 0.0, 500.0, 100.0)
    solids = st.number_input("Solids (ppm)", 0.0, 10000.0, 500.0)
    chloramines = st.number_input("Chloramines (ppm)", 0.0, 10.0, 3.0)
    sulfate = st.number_input("Sulfate (mg/L)", 0.0, 1000.0, 200.0)
    conductivity = st.number_input("Conductivity (μS/cm)", 0.0, 2000.0, 400.0)
    organic_carbon = st.number_input("Organic Carbon (mg/L)", 0.0, 30.0, 5.0)
    trihalomethanes = st.number_input("Trihalomethanes (μg/L)", 0.0, 150.0, 50.0)
    turbidity = st.number_input("Turbidity (NTU)", 0.0, 10.0, 3.0)

    # Predict Button
    if st.button("🔍 Predict Potability"):
        prompt = create_prompt(ph, hardness, solids, chloramines, sulfate,
                               conductivity, organic_carbon, trihalomethanes, turbidity)

        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[prompt],
                config=types.GenerateContentConfig(
                    max_output_tokens=300,
                    temperature=0.3
                )
            )
            output = response.text.strip()

            st.markdown("### 🧠 AI Response")
            if "Prediction:" in output:
                for line in output.splitlines():
                    if line.startswith("Prediction:"):
                        prediction = line.replace("Prediction:", "").strip()
                        if prediction.lower() == "potable":
                            st.success(f"✅ Prediction: {prediction}")
                        elif prediction.lower() == "not potable":
                            st.markdown(f"""
                                <div style="
                                    background-color: #fdecea;
                                    padding: 1rem 1.5rem;
                                    margin-top: 1rem;
                                    border-left: 6px solid #d93025;
                                    border-radius: 10px;
                                    font-weight: bold;
                                    color: #b71c1c;
                                    font-size: 1.05rem;
                                ">
                                    ❌ Prediction: {prediction}
                                </div>
                            """, unsafe_allow_html=True)
                    elif line.startswith("Treatment Suggestions:"):
                        suggestions = line.replace("Treatment Suggestions:", "").strip()

                        st.markdown("### 💡 Treatment Suggestions")
                        st.markdown(f"""
                            <div style="
                                background-color: #eafaf1;
                                padding: 1rem 1.5rem;
                                margin-top: 0.5rem;
                                border-left: 5px solid #34a853;
                                border-radius: 12px;
                                box-shadow: 0 5px 20px rgba(0,0,0,0.05);
                                font-size: 1rem;
                                color: #1a3c34;
                            ">
                                {suggestions}
                            </div>
                        """, unsafe_allow_html=True)
                    elif line.strip():
                        st.write(line)
            else:
                st.write(output)

        except Exception as e:
            st.error(f"❌ Error generating response: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<hr style="margin-top: 3rem; margin-bottom: 1rem;">
<div style="text-align: center; color: #999;">
    🔬 Powered by AI | Built with ❤️ using <b>Streamlit</b>
</div>
""", unsafe_allow_html=True)
