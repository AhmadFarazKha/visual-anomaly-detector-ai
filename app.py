import streamlit as st
import os
from src.core.anomaly_detector import detect_visual_anomaly
from src.utils.file_handler import create_directories_if_not_exist
import io
from PIL import Image # Needed for displaying images reliably

# Ensure data directory exists if you plan to save anything locally
create_directories_if_not_exist("data")

# --- Streamlit Session State Initialization ---
if 'uploaded_image_bytes' not in st.session_state:
    st.session_state.uploaded_image_bytes = None
if 'anomaly_analysis_result' not in st.session_state:
    st.session_state.anomaly_analysis_result = ""
if 'user_anomaly_prompt' not in st.session_state:
    st.session_state.user_anomaly_prompt = ""
if 'show_result' not in st.session_state:
    st.session_state.show_result = False

# --- Page Configuration (Theme controlled by .streamlit/config.toml) ---
st.set_page_config(
    page_title="AI Visual Anomaly Detector",
    page_icon="🔍", # Magnifying glass for detection
    layout="centered", # Or 'wide'
    initial_sidebar_state="collapsed"
)

# --- Application Content ---
st.title("🔍 AI Visual Anomaly Detector")
st.markdown("<p style='text-align: center; color: #E0E0EB; font-size: 1.1rem; margin-bottom: 2rem;'>Upload an image and define 'normal' for AI to detect defects or unusual patterns.</p>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 4, 1])

with col2:
    st.markdown("### 1. Upload Your Image")
    uploaded_file = st.file_uploader(
        "Choose an image file (JPG, PNG) of the item to inspect.",
        type=["jpg", "jpeg", "png"],
        key="image_uploader"
    )

    if uploaded_file is not None:
        st.session_state.uploaded_image_bytes = uploaded_file.getvalue()
        # Reset result if new image is uploaded
        st.session_state.anomaly_analysis_result = ""
        st.session_state.show_result = False

        st.success("Image uploaded successfully!")
        st.image(st.session_state.uploaded_image_bytes, caption='Uploaded Image for Inspection', use_column_width=True)

    st.markdown("---")

    st.markdown("### 2. Define 'Normal' and Ask AI to Detect Anomalies")
    default_prompt_template = """
    Analyze this image to detect any defects, irregularities, or anomalies.
    
    Consider the following as 'normal' or 'expected':
    - [Describe what a normal item should look like, e.g., "The surface should be smooth and uniform," "The plant leaves should be green without spots," "The product packaging should be intact."]

    Describe any deviations from this normal state. If the item appears normal, state that clearly.
    """
    user_prompt_input = st.text_area(
        "Provide details on what a 'normal' item looks like and your specific question:",
        value=st.session_state.user_anomaly_prompt if st.session_state.user_anomaly_prompt else default_prompt_template,
        height=250,
        placeholder=default_prompt_template,
        key="user_prompt_area"
    )
    st.session_state.user_anomaly_prompt = user_prompt_input # Update session state

    st.markdown("---")

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Detect Anomalies with AI 🚀", use_container_width=True, key="btn_detect"):
            if st.session_state.uploaded_image_bytes:
                if user_prompt_input:
                    with st.spinner("AI is inspecting your image for anomalies..."):
                        try:
                            analysis_output = detect_visual_anomaly(
                                st.session_state.uploaded_image_bytes,
                                user_prompt_input
                            )
                            st.session_state.anomaly_analysis_result = analysis_output
                            st.session_state.show_result = True
                            st.success("Anomaly detection complete!")
                        except Exception as e:
                            st.error(f"Error during AI anomaly detection: {e}. Please ensure your API key is correct and the image content is appropriate.")
                            st.session_state.show_result = False
                else:
                    st.warning("Please provide details on what constitutes 'normal' and your detection query.")
            else:
                st.warning("Please upload an image first to analyze for anomalies.")

    with col_btn2:
        if st.button("Clear All & Start Over 🔄", use_container_width=True, key="btn_reset_all"):
            st.session_state.uploaded_image_bytes = None
            st.session_state.anomaly_analysis_result = ""
            st.session_state.user_anomaly_prompt = ""
            st.session_state.show_result = False
            st.info("App state cleared. Ready for a new inspection!")
            st.rerun() # Force rerun to clear uploader and image display

# Display Anomaly Detection Result
if st.session_state.show_result and st.session_state.anomaly_analysis_result:
    with col2: # Align output with central column
        st.markdown("---")
        st.subheader("💡 AI Anomaly Detection Result:")
        st.markdown(st.session_state.anomaly_analysis_result)

        # Download button for the result
        st.download_button(
            label="Download Analysis Text ⬇️",
            data=st.session_state.anomaly_analysis_result.encode('utf-8'),
            file_name="anomaly_analysis.txt",
            mime="text/plain",
            use_container_width=True,
            key="btn_download_result"
        )
    
st.markdown("---")
st.info("Powered by Google Gemini Vision AI and Streamlit.")
st.markdown("<p style='text-align: center; font-size: 0.9rem; color: #a0a0a0; margin-top: 2rem;'>Developed with ❤️ in Piplan, Punjab, Pakistan</p>", unsafe_allow_html=True)