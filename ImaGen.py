import os
import streamlit as st
from PIL import Image
import google.generativeai as genai
import requests
import io
import uuid
import time
from constants import gemini_key

# Streamlit framework configuration
st.set_page_config(
    page_title="OxImaGen 🎨",
    page_icon="🖼️",
    layout="wide"
)

# Load custom CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the CSS file
load_css("ui/Style.css")

# API configuration
os.environ["GOOGLE_API_KEY"] = gemini_key
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Hugging Face API configuration
HF_API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
HF_HEADERS = {"Authorization": "Bearer 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"}

# Function to query Hugging Face model with parameters
def query_hf_model(prompt, theme=None, style=None, size="512x512", quality="high", creativity="medium", temperature=1.0, variance=1.0, num_images=1):
    images = []
    for _ in range(num_images):
        payload = {"inputs": prompt}
        if theme:
            payload["theme"] = theme
        if style:
            payload["style"] = style
        if size:
            payload["size"] = size
        if quality:
            payload["quality"] = quality
        if creativity:
            payload["creativity"] = creativity
        payload["temperature"] = temperature + (0.05 * _)  # Apply slight variation
        payload["variance"] = variance + (0.05 * _)  # Apply slight variation
        payload["seed"] = str(uuid.uuid4())  # Ensure unique seed for different images

        try:
            response = requests.post(HF_API_URL, headers=HF_HEADERS, json=payload)
            response.raise_for_status()
            images.append(response.content)
        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {e}")
    return images

def get_gemini_response(input_text, image=None):
    model = genai.GenerativeModel('gemini-1.5-pro')
    if image is not None:
        response = model.generate_content([input_text, image])
    else:
        response = model.generate_content(input_text)
    return response.text

# Initialize session state for images and project info
if "generated_images" not in st.session_state:
    st.session_state.generated_images = []
if "full_screen_mode" not in st.session_state:
    st.session_state.full_screen_mode = False
if "show_info" not in st.session_state:
    st.session_state.show_info = True  # Start with project info

# Functions to handle main app and project info
def show_main_app():
    st.session_state.show_info = False
    st.experimental_rerun()

def show_project_info():
    st.session_state.show_info = True
    st.experimental_rerun()

# # Sidebar for navigation
# with st.sidebar:
#     st.header("Navigation")
#     if st.session_state.show_info:
#         if st.button("🏠 Main App"):
#             show_main_app()

# Project Information Section
if st.session_state.show_info:
    st.markdown("""
    ## 🚀 OxImaGen: Comprehensive Image Generation & Analysis 🌟
    ---------

     ***🏗️ Architecture 🏛️***
                
    OxImaGen integrates cutting-edge technologies to provide a comprehensive image generation and analysis solution. 🛠️ The architecture includes:
    - **Frontend:** Developed using Streamlit for a responsive and interactive user interface. 🌐
    - **Backend:** Utilizes Hugging Face and Google Gemini APIs for image generation and content analysis. 🔍
    - **Data Handling:** Efficiently manages image inputs and outputs through robust data pipelines. 📊

     ***🛠️ API Calling 📡***
                
    OxImaGen leverages the following APIs for various functionalities:
    1. **Hugging Face API:** Handles image generation with customizable parameters like style, resolution, and content. 🎨
       - **Endpoint:** `/generate-image` 🖼️
       - **Parameters:** `prompt`, `style`, `resolution` 📝
    2. **Google Gemini API:** Provides advanced content generation and analysis. 📈
       - **Endpoint:** `/analyze-image` 🖼️
       - **Parameters:** `image_url`, `analysis_type` 🔎

    ***⚙️ Function Calling 🔧***
                
    The core functions of OxImaGen include:
    - **`query_hf_model(prompt, style, resolution)`**: Communicates with the Hugging Face API to generate images based on user-defined prompts and styles. 📩
    - **`get_gemini_response(image_url, analysis_type)`**: Interacts with Google Gemini API to provide insights and analysis on the uploaded images. 📊

    ***🔍 Inference Calling 🔬***
                
    Inference in OxImaGen involves:
    1. **Image Generation:** Users provide a text prompt and optional parameters. The `query_hf_model` function sends these details to the Hugging Face API, which generates and returns an image. 🖼️
    2. **Image Analysis:** Once an image is generated or uploaded, the `get_gemini_response` function sends the image URL to the Google Gemini API for analysis, returning insights or detailed reports based on the analysis type specified. 🔍

    ***📚 Use Cases 🛠️***
                
    OxImaGen provides several practical use cases, including:
    1. **Image Generation:** Create images from textual descriptions with various themes, styles, and resolutions to suit different needs. 🎨
    2. **Image Analysis:** Analyze uploaded images to gain insights, detect patterns, or retrieve content-specific information. 🔎
    3. **Interactive UI:** Engage users with a friendly and intuitive interface for generating, viewing, and downloading images. Explore project details and functionalities effortlessly. 🖥️

    ***🛠️ Frameworks Used 🧰***
                
    OxImaGen is built using a blend of powerful frameworks and technologies:
    - **Streamlit:** Enables the creation of an interactive and user-friendly web app interface. 💻
    - **Hugging Face:** Utilized for its FLUX.1-dev model to generate high-quality images from text prompts. 🖼️
    - **Google Gemini:** Provides advanced capabilities for content generation and image analysis, enhancing the overall functionality of the app. 🔍

    ***🔄 Full Workflow 🔄***
                
    Here's a step-by-step breakdown of the image generation workflow in OxImaGen:
    1. **User Input:** The user provides a text prompt and optional parameters (style, resolution) through the app interface. 📝
    2. **Image Generation Request:** The `query_hf_model` function sends these inputs to the Hugging Face API. 📩
    3. **Image Generation:** The Hugging Face API processes the request and generates an image based on the provided prompt and parameters. 🖼️
    4. **Image Retrieval:** The generated image is retrieved and displayed to the user. 👀
    5. **Image Analysis Request:** If the user opts for analysis, the `get_gemini_response` function sends the image URL to the Google Gemini API. 🌐
    6. **Analysis Results:** The Google Gemini API processes the image and returns insights or reports based on the specified analysis type. 📈
    7. **Display Results:** The analysis results are presented to the user through the app interface. 📊

    ***🔄 Navigation 🏠***
                
    Want to go main app, click the button below: 🏡
    """)

    if st.button("🏠 Go to Main App"):
        show_main_app()

else:
    # Main App content (Once the user navigates from the info section)
    st.header('🎨 Oxsecure ImaGen 🎨 / FLUX-Dev ♨️')
    st.markdown("-----")

    # Text input for prompt
    input_text = st.text_input("🖋️ Input Prompt For Image Generation & Analysis", key="input")

    # Layout for parameters
    col1, col2 = st.columns(2)

    with col1:
        theme = st.selectbox("🎭 Select Theme:", ["None", "Nature 🌳", "Sci-Fi 🚀", "Abstract 🌀", "Fantasy 🧚‍♀️", "Anime 💖", "Spectular 👓"], key="theme")
        size = st.selectbox("📏 Select Image Size:", ["256x256", "512x512", "1024x1024"], key="size")
        creativity = st.selectbox("🎨 Select Creativity Level:", ["low", "medium", "high"], key="creativity")

    with col2:
        style = st.selectbox("🖼️ Select Art Style:", ["None", "Impressionism 🎨", "Cubism 🎭", "Surrealism 🌀", "Pop Art 🌈", "Sketch Art ✏️", "Digital Art 🧑🏻‍🎨"], key="style")
        quality = st.selectbox("⭐ Select Quality:", ["low", "medium", "high"], key="quality")
        num_images = st.selectbox("📸 Number of Images to Generate:", options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], key="num_images")

    # Advanced Parameters Section
    with st.expander("⚙️ Advanced Parameters"):
        st.markdown("-----")
        col3, col4 = st.columns(2)
        with col3:
            temperature = st.slider(
                "🌡️ Temperature:",
                min_value=0.0,
                max_value=2.0,
                step=0.1,
                value=1.0,
                key="temperature"
            )

        with col4:
            variance = st.slider(
                "📊 Variance:",
                min_value=0.0,
                max_value=2.0,
                step=0.1,
                value=1.0,
                key="variance"
            )

    # Button to generate images from a prompt
    submit_generate = st.button("🎨 Generate Images from Prompt")
    st.markdown("------")
    if submit_generate and input_text:
        progress_bar = st.progress(0)  # Initialize the progress bar
        with st.spinner('⏳ Generating images... Please wait...'):
            images_bytes = query_hf_model(
                input_text,
                theme if theme != "None" else None,
                style if style != "None" else None,
                size,
                quality,
                creativity,
                temperature,
                variance,
                num_images
            )
            
            # Simulate the progress percentage over time (Example: 10% increase each second)
            for i in range(1, 11):
                time.sleep(0.5)  # Simulate loading time
                progress_bar.progress(i * 10)  # Update progress bar
                if images_bytes:
                    st.session_state.generated_images = []  # Clear previous images
                    for i, img_bytes in enumerate(images_bytes):
                        try:
                            img = Image.open(io.BytesIO(img_bytes))
                            st.session_state.generated_images.append(img)  # Save image to session state
                        except Exception as e:
                             st.error(f"Error processing image: {e}")

# Organize thumbnails in responsive columns
if st.session_state.generated_images:
    cols = st.columns(min(num_images, 10))  # Show in max 10 columns or fewer based on number of images
    for idx, img in enumerate(st.session_state.generated_images):
        with cols[idx]:
            st.image(img, caption=f"Generated Image {idx+1}", use_column_width=True)

            # Provide download link with a unique key for each button
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            buf.seek(0)
            st.download_button(
                label=f"📥 Download Image {idx+1}",
                data=buf,
                file_name=f"generated_image_{idx+1}.png",
                mime="image/png",
                key=f"download_button_{idx}"  # Unique key for each button
            )
         
    # File uploader for image
    st.markdown("------")
    uploaded_file = st.file_uploader("📂 Choose an image...", type=["jpg", "jpeg", "png", "webp", "gif", "bmp", "tiff", "ico", "heif", "jfif", "svg", "exif", "psd", "raw"])
    image = None
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)

# Button to toggle full-screen images
if st.session_state.generated_images:
    if st.button("🪟 Full-Screen Images"):
        st.session_state.full_screen_mode = not st.session_state.full_screen_mode

    # Display images based on the toggle state
    if st.session_state.full_screen_mode:
        for i, img in enumerate(st.session_state.generated_images):
            st.image(img, caption=f"Full-Screen Generated Image {i+1}", use_column_width=True)

    # Button to get response about the image
    submit_analyze = st.button("🔍 Tell me about the image")
    if submit_analyze:
        if input_text and image is not None:
            response = get_gemini_response(input_text, image)
        elif image is not None:
            response = get_gemini_response("", image)
        elif input_text:
            response = get_gemini_response(input_text)
        else:
            response = "Please provide an input prompt or upload an image."
        st.subheader("📝 Result ")
        st.markdown("-----")
        st.write(response)


st.markdown("---")
linkedin_url = "https://www.linkedin.com/in/aditya-pandey-896109224"
st.markdown("  Created with 🤗💖 By Aditya Pandey  " f"[  LinkedIn 🔗]({linkedin_url})")
