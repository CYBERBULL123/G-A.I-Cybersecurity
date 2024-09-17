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
    page_title="ImaGen 🎨",
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
        # Apply slight random variation to temperature and variance
        payload["temperature"] = temperature + (0.05 * _)
        payload["variance"] = variance + (0.05 * _)
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

# Initialize session state for images if not already done
if "generated_images" not in st.session_state:
    st.session_state.generated_images = []
if "full_screen_mode" not in st.session_state:
    st.session_state.full_screen_mode = False  # Add full-screen toggle state

# Streamlit Main Framework
st.header('Oxsecure ImaGen 🎨/FLUX-Dev ♨️')
st.markdown("--------")

# Text input for prompt
input_text = st.text_input("🖋️ Input Prompt: ", key="input")

# Layout for parameters
col1, col2 = st.columns(2)

with col1:
    theme = st.selectbox("🎭 Select Theme:", ["None", "Nature 🌳", "Sci-Fi 🚀", "Abstract 🌀", "Fantasy 🧚‍♀️"], key="theme")
    size = st.selectbox("📏 Select Image Size:", ["256x256", "512x512", "1024x1024"], key="size")
    creativity = st.selectbox("🎨 Select Creativity Level:", ["low", "medium", "high"], key="creativity")

with col2:
    style = st.selectbox("🖼️ Select Art Style:", ["None", "Impressionism 🎨", "Cubism 🎭", "Surrealism 🌀", "Pop Art 🌈"], key="style")
    quality = st.selectbox("⭐ Select Quality:", ["low", "medium", "high"], key="quality")
    num_images = st.selectbox("📸 Number of Images to Generate:", options=[1, 2, 3, 4, 5], key="num_images")

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
    cols = st.columns(min(num_images, 5))  # Show in max 5 columns or fewer based on number of images
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
uploaded_file = st.file_uploader("📂 Choose an image...", type=["jpg", "jpeg", "png"])
image = None
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)


# Button to toggle full-screen images
if st.session_state.generated_images:
    if st.button("🔍 Toggle Full-Screen Images"):
        st.session_state.full_screen_mode = not st.session_state.full_screen_mode

    # Display images based on the toggle state
    if st.session_state.full_screen_mode:
        for i, img in enumerate(st.session_state.generated_images):
            st.image(img, caption=f"Full-Screen Generated Image {i+1}", use_column_width=True)
    else:
        cols = st.columns(min(num_images, 5))  # Organize thumbnails in columns
        for idx, img in enumerate(st.session_state.generated_images):
            with cols[idx]:
                st.image(img, caption=f"Generated Image {idx+1}", use_column_width=True)

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
