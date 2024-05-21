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
def query_gemini(prompt, image=None):
    model = genai.GenerativeModel('gemini-pro-vision')
    if image:
        response = model.generate_content([prompt, image])
    else:
        response = model.generate_content(prompt)
    return response.text

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

submit = st.button("Tell me about the image/text")

if submit:
    if input_prompt or file_text:
        prompt = input_prompt if input_prompt else file_text
        response = query_gemini(prompt, image)
        st.subheader("The Response is:")
        st.write(response)

        # Text-to-Speech conversion
        tts = gTTS(response)
        audio_file = BytesIO()
        tts.write_to_fp(audio_file)
        st.audio(audio_file, format='audio/mp3')
    else:
        st.warning("Please provide an input prompt or upload a file.")
