import os
import streamlit as st
from PIL import Image
import google.generativeai as genai
import aiohttp
import asyncio
import random
from gtts import gTTS
import re
import io
from io import BytesIO
import uuid
import time
import logging
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

# Style list with different art styles
style_list = [
    {
        "name": "None",
        "prompt": "{prompt}",
        "negative_prompt": "",
    },
    {
        "name": "Cinematic 🎥",
        "prompt": "cinematic still {prompt} . emotional, harmonious, vignette, highly detailed, high budget, bokeh, cinemascope, moody, epic, gorgeous, film grain, grainy",
        "negative_prompt": "anime, cartoon, graphic, text, painting, crayon, graphite, abstract, glitch, deformed, mutated, ugly, disfigured",
    },
    {
        "name": "Photographic 📸",
        "prompt": "cinematic photo {prompt} . 35mm photograph, film, bokeh, professional, 4k, highly detailed",
        "negative_prompt": "drawing, painting, crayon, sketch, graphite, impressionist, noisy, blurry, soft, deformed, ugly",
    },
    {
        "name": "Anime 🎨",
        "prompt": "anime artwork {prompt} . anime style, key visual, vibrant, studio anime, highly detailed",
        "negative_prompt": "photo, deformed, black and white, realism, disfigured, low contrast",
    },
    {
        "name": "Manga 📚",
        "prompt": "manga style {prompt} . vibrant, high-energy, detailed, iconic, Japanese comic style",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, realism, photorealistic, Western comic style",
    },
    {
        "name": "Digital Art 🧑🏻‍🎨",
        "prompt": "concept art {prompt} . digital artwork, illustrative, painterly, matte painting, highly detailed",
        "negative_prompt": "photo, photorealistic, realism, ugly",
    },
    {
        "name": "Pixel Art 🕹️",
        "prompt": "pixel-art {prompt} . low-res, blocky, pixel art style, 8-bit graphics",
        "negative_prompt": "sloppy, messy, blurry, noisy, highly detailed, ultra textured, photo, realistic",
    },
    {
        "name": "Fantasy Art 🧚‍♀️",
        "prompt": "ethereal fantasy concept art of {prompt} . magnificent, celestial, ethereal, painterly, epic, majestic, magical, fantasy art, cover art, dreamy",
        "negative_prompt": "photographic, realistic, realism, 35mm film, dslr, cropped, frame, text, deformed, glitch, noise, noisy, off-center, deformed, cross-eyed, closed eyes, bad anatomy, ugly, disfigured, sloppy, duplicate, mutated, black and white",
    },
    {
        "name": "Neonpunk 🌆",
        "prompt": "neonpunk style {prompt} . cyberpunk, vaporwave, neon, vibes, vibrant, stunningly beautiful, crisp, detailed, sleek, ultramodern, magenta highlights, dark purple shadows, high contrast, cinematic, ultra detailed, intricate, professional",
        "negative_prompt": "painting, drawing, illustration, glitch, deformed, mutated, cross-eyed, ugly, disfigured",
    },
    {
        "name": "3D Model 🏆",
        "prompt": "professional 3d model {prompt} . octane render, highly detailed, volumetric, dramatic lighting",
        "negative_prompt": "ugly, deformed, noisy, low poly, blurry, painting",
    },
    {
        "name": "Impressionism 🎨",
        "prompt": "impressionist artwork {prompt} . vibrant, expressive brushstrokes, rich colors, painterly",
        "negative_prompt": "photo, photorealistic, clean lines, abstract",
    },
    {
        "name": "Cubism 🎭",
        "prompt": "cubist artwork {prompt} . fragmented, geometric, abstract forms, multiple perspectives",
        "negative_prompt": "realistic, smooth, conventional forms",
    },
    {
        "name": "Surrealism 🌀",
        "prompt": "surrealistic artwork {prompt} . dreamlike, bizarre, imaginative, otherworldly",
        "negative_prompt": "realistic, conventional, mundane",
    },
    {
        "name": "Pop Art 🌈",
        "prompt": "pop art {prompt} . bold colors, graphic design, comic-style, modern culture",
        "negative_prompt": "traditional art, subdued colors, abstract",
    },
    {
        "name": "Sketch Art ✏️",
        "prompt": "sketch art {prompt} . pencil drawings, detailed lines, rough texture",
        "negative_prompt": "colorful, digital, polished",
    },
]


def generate_content_from_image(image, theme):
    if not image:
        return "No image provided for content generation."

    # Prepare the content generation prompt based on theme
    theme_prompts = {
    "None": "Simple",
    
    "Adventure 🏔️": """
    🌄 **Embark on an Epic Adventure!** 🏞️
    
    Create an exhilarating story set in wild landscapes and untamed frontiers. Your characters will face thrilling challenges, mysterious discoveries, and a final showdown that tests their courage and resolve. 
    Let their journey be one of excitement, danger, and triumph!. use proper emojis and make it more intresting, immersive and catchy. Use more than 500 words.
    """,
    
    "Sci-Fi 🚀": """
    👽 **Journey into the Future!** 🌌
    
    Imagine a far-off world filled with advanced technology and unknown lifeforms. Your story will unfold with groundbreaking innovations, shocking twists, and a quest that challenges the limits of the imagination. 
    Explore strange galaxies and futuristic adventures that leave readers on the edge of their seats!. use proper emojis and make it more intresting, immersive and catchy. Use more than 500 words.
    """,
    
    "Fantasy 🧚‍♀️": """
    🏰 **Step into a Magical Realm!** 🦄
    
    Enter a world where magic is real and legends come to life. Write about brave heroes, enchanted creatures, and epic quests. Your story will take readers on a journey through enchanted forests, mystical lands, and ancient prophecies. 
    Will good conquer evil in the ultimate battle of magic?. use proper emojis and make it more intresting, immersive and catchy. Use more than 500 words.
    """,
    
    "Mystery 🕵️‍♂️": """
    🧐 **Crack the Code of a Dark Mystery!** 🔍
    
    Start with an eerie scene and dive into a web of secrets and clues. Red herrings, hidden motives, and spine-chilling revelations will lead to a climactic resolution that no one saw coming. 
    Can your characters solve the mystery before it's too late?. use proper emojis and make it more intresting, immersive and catchy. Use more than 500 words.
    """,
    
    "Romance 💕": """
    💖 **Feel the Magic of Love Unfold!** 🌹
    
    Create a beautiful and heartwarming story of love, loss, and reconciliation. Build the tension and passion between your characters as they navigate the highs and lows of a romantic journey.
    Will their love overcome all obstacles to reach a perfect happy ending?. use proper emojis and make it more intresting, immersive and catchy. Use more than 500 words.
    """,
    
    "ComicBook 🤠": """
    🦸‍♂️ **Unleash Superhero Action!** ⚡
    
    Dive into a thrilling, fast-paced adventure with superpowered heroes and sinister villains. Your comicbook-style story should be filled with dramatic battles, heroic moments, and epic plot twists. 
    Will the forces of good prevail in this action-packed tale? .use proper emojis and make it more intresting, immersive and catchy. Use more than 500 words .
    """
}

    prompt = theme_prompts.get(theme, theme_prompts["None"])


    # Call Google Gemini API
    try:
        response = get_gemini_response(prompt, image)
        return response
    except Exception as e:
        st.error(f"Content generation failed: {e}")
        return "Content generation failed."

# Remove special characters and improve formatting
def clean_text(text):
    # Retain only alphabetic characters, numbers, punctuation, and spaces
    clean_text = re.sub(r'[^a-zA-Z0-9.,!?;:()\'\" \n]', '', text)
    return re.sub(r'\s+', ' ', clean_text).strip()

# API configuration
os.environ["GOOGLE_API_KEY"] = gemini_key
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Hugging Face API configuration
HF_API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
HF_HEADERS = {"Authorization": "Bearer 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"}

# Function to query Hugging Face model with parameters
async def query_hf_model_async(prompt, text, theme=None, style=None, size="512x512", dimension="512x512", quality="high", creativity="medium", temperature=1.0, variance=1.0, num_images=1):
    images = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(num_images):
            payload = {"inputs": prompt}
            if input_text:
                payload["text"] = text
            if theme:
                payload["theme"] = theme
            if style:
                payload["style"] = style
            if size:
                payload["size"] = size
            if dimension:
                payload["dimension"] = dimension
            if quality:
                payload["quality"] = quality
            if creativity:
                payload["creativity"] = creativity
            payload["temperature"] = temperature + (0.05 * _)  # Apply slight variation
            payload["variance"] = variance + (0.05 * _)  # Apply slight variation
            payload["seed"] = str(uuid.uuid4())  # Ensure unique seed for different images

            task = asyncio.create_task(fetch_image(session, payload))
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        for img_bytes in results:
            if img_bytes:
                images.append(img_bytes)
    return images

# Helper function to fetch image
async def fetch_image(session, payload):
    try:
        async with session.post(HF_API_URL, headers=HF_HEADERS, json=payload) as response:
            response.raise_for_status()
            return await response.read()
    except aiohttp.ClientError as e:
<<<<<<< HEAD
        st.error(f"API request failed")
=======
        st.error(f"API request failed: {e}")
>>>>>>> main
        return None

# Helper function to get the style prompt and negative prompt based on the selected style
def get_style_prompts(style_name):
    for style in style_list:
        if style['name'] == style_name:
            return style['prompt'], style['negative_prompt']
    return "{prompt}", ""  # Default no style


def get_gemini_response(input_text, image=None):
    model = genai.GenerativeModel('gemini-1.5-flash')
    if image is not None:
        response = model.generate_content([input_text, image])
    else:
        response = model.generate_content(input_text)
    return response.text

# Function to generate and store audio in session state
def generate_and_store_audio(content):
    clean_response = clean_text(content)
    tts = gTTS(clean_response)
    audio_file = BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)  # Reset file pointer to the beginning
    st.session_state.generated_audio = audio_file

# Initialize session state for images and project info
if "generated_images" not in st.session_state:
    st.session_state.generated_images = []
if "full_screen_mode" not in st.session_state:
    st.session_state.full_screen_mode = False
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = ""
if 'generated_audio' not in st.session_state:
    st.session_state.generated_audio = None
if "show_info" not in st.session_state:
    st.session_state.show_info = True  # Start with project info

# Functions to handle main app and project info
def show_main_app():
    st.session_state.show_info = False
<<<<<<< HEAD
    st.rerun()

def show_project_info():
    st.session_state.show_info = True
    st.rerun()
=======
    st.experimental_rerun()

def show_project_info():
    st.session_state.show_info = True
    st.experimental_rerun()
>>>>>>> main

# Function to run asyncio event loop within Streamlit app
def run_async_function(async_func, *args, **kwargs):
    if callable(async_func):  # Ensure async_func is a function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(async_func(*args, **kwargs))
    else:
        raise TypeError(f"{async_func} is not a function or coroutine. Check for conflicts in your variable names.")

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
    - **`generate_story_from_image(image)`**: Generates a story based on the uploaded image using natural language processing techniques. 📝
    - **`generate_image_from_story(story)`**: Generates an image based on the provided story using computer vision techniques. 🖼️

    ***🔍 Inference Calling 🔬***
                
    Inference in OxImaGen involves:
    1. **Image Generation:** Users provide a text prompt and optional parameters. The `query_hf_model` function sends these details to the Hugging Face API, which generates and returns an image. 🖼️
    2. **Image Analysis:** Once an image is generated or uploaded, the `get_gemini_response` function sends the image URL to the Google Gemini API for analysis, returning insights or detailed reports based on the analysis type specified. 🔍
    3. **Story Generation:** Users can upload an image, and the `generate_story_from_image` function generates a story based on the image. 📝
    4. **Image Generation from Story:** Users can provide a story, and the `generate_image_from_story` function generates an image based on the story. 🖼️

    ***📚 Use Cases 🛠️***
                
    OxImaGen provides several practical use cases, including:
    1. **Image Generation:** Create images from textual descriptions with various themes, styles, and resolutions to suit different needs. 🎨
    2. **Image Analysis:** Analyze uploaded images to gain insights, detect patterns, or retrieve content-specific information. 🔎
    3. **Interactive UI:** Engage users with a friendly and intuitive interface for generating, viewing, and downloading images. Explore project details and functionalities effortlessly. 🖥️
    4. **Story Generation:** Generate stories based on uploaded images, and vice versa. 📝

    ***🛠️ Frameworks Used 🧰***
                
    OxImaGen is built using a blend of powerful frameworks and technologies:
    - **Streamlit:** Enables the creation of an interactive and user-friendly web app interface. 💻
    - **Hugging Face:** Utilized for its FLUX.1-dev model to generate high-quality images from text prompts. 🖼️
    - **Google Gemini:** Provides advanced capabilities for content generation and image analysis, enhancing the overall functionality of the app. 🔍
    - **Natural Language Processing (NLP) Libraries:** Used for story generation and analysis. 📝
    - **Computer Vision Libraries:** Used for image analysis and generation. 🖼️

    ***🔄 Full Workflow 🔄***
                
    Here's a step-by-step breakdown of the image generation workflow in OxImaGen:
    1. **User Input:** The user provides a text prompt and optional parameters (style, resolution) through the app interface. 📝
    2. **Image Generation Request:** The `query_hf_model` function sends these inputs to the Hugging Face API. 📩
    3. **Image Generation:** The Hugging Face API processes the request and generates an image based on the provided prompt and parameters. 🖼️
    4. **Image Retrieval:** The generated image is retrieved and displayed to the user. 👀
    5. **Image Analysis Request:** If the user opts for analysis, the `get_gemini_response` function sends the image URL to the Google Gemini API. 🌐
    6. **Analysis Results:** The Google Gemini API processes the image and returns insights or reports based on the specified analysis type. 📈
    7. **Display Results:** The analysis results are presented to the user through the app interface. 📊

    ***🔥 Key Features 🔥***
                
    - **Image Generation:** Generate high-quality images from text prompts with customizable styles and resolutions.
    - **Image Analysis:** Analyze uploaded images to gain insights, detect patterns, or retrieve content-specific information.
    - **Interactive UI:** Engage users with a friendly and intuitive interface for generating, viewing, and downloading images.
    - **Advanced APIs:** Leverage the power of Hugging Face and Google Gemini APIs for image generation and analysis.
    - **Robust Data Handling:** Efficiently manage image inputs and outputs through robust data pipelines.
    - **Story Generation:** Generate stories based on uploaded images, and vice versa.

    ***🔄 Navigation 🏠***
                
    Want to go main app, click the button below: 🏡
    """)
    if st.button("🏠 Go to Main App"):
        show_main_app()

else:
    # Main App content (Once the user navigates from the info section)
    st.header('🎨 Oxsecure ImaGen 🎨 / FLUX-Dev ♨️')
    st.markdown("***Image & Story Generation Section 🖼️***")

    # Text input for prompt
    input_text = st.text_input("🖋️ Input Prompt For Image Generation & Analysis", key="input")

    # Layout for parameters
    col1, col2 = st.columns(2)

    with col1:
        theme = st.selectbox("🎭 Select Theme:", ["None", "Nature 🌳", "Sci-Fi 🚀", "Abstract 🌀", "Fantasy 🧚‍♀️", "Spectular 👓"], key="theme")
        style_name = st.selectbox("🖼️ Select Art Style:", [style['name'] for style in style_list], key="style")
        creativity = st.selectbox("🎨 Select Creativity Level:", ["low", "medium", "high"], key="creativity")

    with col2:
        
        quality = st.selectbox("⭐ Select Quality:", ["low", "medium", "high"], key="quality")
        num_images = st.selectbox("📸 Number of Images to Generate:", options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], key="num_images")
        size = st.selectbox("📏 Select Image Size:", ["256x256", "512x512", "1024x1024"], key="size")


    # Advanced Parameters Section
    with st.expander("⚙️ Advanced Parameters"):
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

            variance = st.slider(
                "📊 Variance:",
                min_value=0.0,
                max_value=2.0,
                step=0.1,
                value=1.0,
                key="variance"
            )


        with col4:
            width = st.slider("📏 Adjust Image Width:", min_value=100, max_value=1024, value=512, step=64)
            height = st.slider("📏 Adjust Image Height:", min_value=100, max_value=1024, value=512, step=64)
            dimension = f"{width}x{height}"

    # Button to generate images from a prompt
    story_theme = st.selectbox("📚 Choose Story Theme:",["None", "ComicBook 🤠", "Adventure 🏔️", "Sci-Fi 🚀", "Fantasy 🧚‍♀️", "Mystery 🕵️‍♂️", "Romance 💕"],key="story_theme")
    st.divider()
    col1, col2 , col3 = st.columns(3)  # Create two columns

    with col1:
        submit_generate = st.button("🎨 Generate Images and Story")

    with col2:
        if st.button("🪟 Full-Screen Images"):
            st.session_state.full_screen_mode = not st.session_state.full_screen_mode
    
    with col3:
        if st.button("🔄 clear Audio "):
            st.session_state.generated_audio = None
            st.session_state.story_regenerated = True

    st.divider()

    # Display images based on the toggle state
    if st.session_state.full_screen_mode:
        for i, img in enumerate(st.session_state.generated_images):
            st.image(img, caption=f"Full-View {i+1}", use_column_width=True)

    if submit_generate and input_text:
        progress_bar = st.progress(0)  # Initialize the progress bar
        with st.spinner('⏳ Generating images... Please wait...'):
            style_prompt, negative_prompt = get_style_prompts(style_name)
            final_prompt = style_prompt.format(prompt=input_text)

            images_bytes = run_async_function(
                query_hf_model_async,
                input_text,
                final_prompt,
                theme if theme != "None" else None,
                style_name if style_name != "(No style)" else None,
                size,
                dimension,
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
                    st.session_state.generated_images = [] 
                    for i, img_bytes in enumerate(images_bytes):
                        try:
                            img = Image.open(io.BytesIO(img_bytes))
                            st.session_state.generated_images.append(img)
                        except Exception as e:
                            st.error(f"Error processing image: {e}")

        if st.session_state.generated_images:
            if len(st.session_state.generated_images) > 0:
                selected_image = random.choice(st.session_state.generated_images)  # Choose one image randomly
                if 'story_theme' in locals() or 'story_theme' in globals():
                    content = generate_content_from_image(selected_image, story_theme)  # Generate content from the chosen image
                    st.session_state.generated_content = content
                    # Display the generated content
                    st.markdown(f"***📜 Generated Story***")
                    st.markdown(st.session_state.generated_content)
                    if st.session_state.generated_audio is None:
                        generate_and_store_audio(content)
                    if st.session_state.generated_audio is not None:
                       st.session_state.generated_audio.seek(0)
                       st.audio(st.session_state.generated_audio, format='audio/mp3')
                else:
                    st.error("story_theme is not defined")
            else:
                st.error("No images to choose from")
        else:
            st.error("No generated images")


    # Organize thumbnails in responsive columns
    if st.session_state.generated_images:
        cols = st.columns(min(num_images, 10))  # Show in max 10 columns or fewer based on number of images
        for idx, img in enumerate(st.session_state.generated_images[:len(cols)]):
            with cols[idx]:
                st.image(img, caption=f"🪄 Img {idx+1}", use_column_width=True)

                # Provide download link with a unique key for each button
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                buf.seek(0)
                st.download_button(
                    label=f"📥",
                    data=buf,
                    file_name=f"OxImaGen_{idx+1}.png",
                    mime="image/png",
                    key=f"download_button_{idx}"  # Unique key for each button
                )

        if st.session_state.generated_content:
            with st.expander("Generated Content ✏️"):
                st.markdown(f"***📜 Generated Story***")
                st.markdown(st.session_state.generated_content)
                if st.session_state.generated_audio is not None:
                    st.session_state.generated_audio.seek(0)
                    st.audio(st.session_state.generated_audio, format='audio/mp3')
                else:
                    st.error("Audio generation failed.")

    # File uploader for image
    st.markdown("***File Upload Section 📤***")
    st.divider()
    uploaded_file = st.file_uploader("📂 Choose an image...", type=["jpg", "jpeg", "png", "webp", "gif", "bmp", "tiff", "ico", "heif", "jfif", "svg", "exif", "psd", "raw"])
    image = None
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", width=250, use_column_width=False)
        st.markdown("-----")

    # Button to get response about the image
    submit_analyze = st.button("🔍 Tell me about the image")
    if submit_analyze:
        if input_text and image is not None:
            response = get_gemini_response(input_text, image)
            st.markdown("***📝 Result***")
            st.write(response)
        elif image is not None:
            content = generate_content_from_image(image, story_theme)
            st.markdown(f"***📜 Generated Content for Uploded Image***")
            st.markdown(content)
        elif image and input_text is None:
            content = generate_content_from_image(image, story_theme)
            st.markdown(f"***📜 Generated Content for Uploded Image***")
            st.markdown(content)     
        elif input_text:
            response = get_gemini_response(input_text)
            st.markdown("***📝 Result***")
            st.write(response)
        else:
            st.write("Please provide an input prompt or upload an image.")

st.markdown("---")
linkedin_url = "https://www.linkedin.com/in/aditya-pandey-896109224"
<<<<<<< HEAD
st.markdown("  Created with 🤗💖 By Aditya Pandey  " f"[  LinkedIn 🔗]({linkedin_url})")
=======
st.markdown("  Created with 🤗💖 By Aditya Pandey  " f"[  LinkedIn 🔗]({linkedin_url})")
>>>>>>> main
