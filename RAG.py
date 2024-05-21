import os
import requests
from PIL import Image
from PyPDF2 import PdfReader
import streamlit as st
from gtts import gTTS
from io import BytesIO
import google.generativeai as genai
from constants import gemini_key
from bs4 import BeautifulSoup
import urllib.request
from google.api_core.exceptions import GoogleAPIError

# Streamlit configuration
st.set_page_config(
    page_title="OxSecure Images & Text",
    page_icon="🎨",
    layout="wide"
)

# API configuration
os.environ["GOOGLE_API_KEY"] = gemini_key
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Function to query Gemini model
def query_gemini(context, prompt, image=None):
    try:
        if image:
            model = genai.GenerativeModel('gemini-pro-vision')
            response = model.generate_content([context + prompt, image])
        else:
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(context + prompt)
        return response.text
    except GoogleAPIError as e:
        st.error(f"An error occurred while querying the Gemini API: {e}")
        return None

# Function to extract text from PDF
def extract_text_from_pdf(file):
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

# Function to extract text from URL
def extract_text_from_url(url):
    response = urllib.request.urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    paragraphs = soup.find_all('p')
    text = ' '.join([para.get_text() for para in paragraphs])
    return text

# Streamlit main framework
st.header('OxSecure ImaGen 🎨')
st.title('GenAI ImaGen powers ♨️')
st.subheader('By :- Aadi 🧑‍💻')

input_prompt = st.text_input("Input Prompt: ", key="input")

uploaded_file = st.file_uploader("Choose an image or PDF file...", type=["jpg", "jpeg", "png", "pdf"])
uploaded_url = st.text_input("Or enter an article URL:")

image = None
file_text = ""

if uploaded_file is not None:
    if uploaded_file.type in ["image/jpeg", "image/png", "image/jpg"]:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)
    elif uploaded_file.type == "application/pdf":
        file_text = extract_text_from_pdf(uploaded_file)
        st.text_area("Extracted Text from PDF:", file_text, height=300)

if uploaded_url:
    file_text = extract_text_from_url(uploaded_url)
    st.text_area("Extracted Text from URL:", file_text, height=300)

# Initialize or update session state for context
if "context" not in st.session_state:
    st.session_state.context = ""

submit = st.button("Tell me about the image/text")

if submit:
    if input_prompt or file_text:
        prompt = input_prompt if input_prompt else ""
        st.session_state.context += " " + file_text  # Update the context with new extracted text
        st.write(f"Prompt being sent to Gemini API: {prompt}")  # Debugging line to see the prompt content
        response = query_gemini(st.session_state.context, prompt, image)
        if response:
            st.subheader("The Response is:")
            st.write(response)

            # Text-to-Speech conversion
            tts = gTTS(response)
            audio_file = BytesIO()
            tts.write_to_fp(audio_file)
            st.audio(audio_file, format='audio/mp3')
    else:
        st.warning("Please provide an input prompt or upload a file.")
    st.markdown("---")
    linkedin_url = "https://www.linkedin.com/in/aditya-pandey-896109224"
    st.markdown("  Created with 🤗 💖 By Aditya Pandey  "  f"[ LinkedIn 🔗 ]({linkedin_url})")



