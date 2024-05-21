# =============================================================================
# COPYRIGHT NOTICE
# -----------------------------------------------------------------------------
# This source code is the intellectual property of Aditya Pandey.
# Any unauthorized reproduction, distribution, or modification of this code
# is strictly prohibited.
# If you wish to use or modify this code for your project, please ensure
# to give full credit to Aditya Pandey.
#
# PROJECT DESCRIPTION
# -----------------------------------------------------------------------------
# This code is for a chatbot crafted with powerful prompts, designed to
# utilize the Gemini API. It is tailored to assist cybersecurity researchers.
#
# Author: Aditya Pandey
# =============================================================================

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

def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
# Load the CSS file
load_css("ui/Style.css")


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
    try:
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"An error occurred while extracting text from PDF: {e}")
        return ""

# Function to extract text from URL
def extract_text_from_url(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        request = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(request)
        html = response.read()
        soup = BeautifulSoup(html, 'html.parser')
        paragraphs = soup.find_all('p')
        text = ' '.join([para.get_text() for para in paragraphs])
        return text
    except Exception as e:
        st.error(f"An error occurred while extracting text from URL: {e}")
        return ""

# Remove Special characters
def clean_text(text):
    # Retain only alphabetic characters and spaces
    return re.sub(r'[^a-zA-Z ]', '', text)

# Streamlit main framework
st.header('OxSecure ImaGen 🎨')
st.divider()
st.title('GenAI ImaGen powers ♨️')
st.divider()
st.write('By :- Aadi 🧑‍💻')

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
        
        # Start spinner before processing
        spinner = st.spinner("Processing..... Getting Results ⏳")
        with spinner:
            response = query_gemini(st.session_state.context, prompt, image)
        
        # Stop spinner after processing
        if response:
            st.subheader("The Response is:")
            st.write(response)
            
            clean_response = clean_text(response)

            # Text-to-Speech conversion
            tts = gTTS(clean_response)
            audio_file = BytesIO()
            tts.write_to_fp(audio_file)
            st.audio(audio_file, format='audio/mp3')
    else:
        st.warning("Please provide an input prompt or upload a file.")
st.markdown("---")
linkedin_url = "https://www.linkedin.com/in/aditya-pandey-896109224"
st.markdown("  Created with 🤗 💖 By Aditya Pandey  "  f"[ LinkedIn 🔗 ]({linkedin_url})")
