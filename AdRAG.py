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

# Import library
import os
import faiss
import numpy as np
import pandas as pd
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
import re
import json
from google.api_core.exceptions import GoogleAPIError
import speech_recognition as sr
from collections import defaultdict

# Streamlit configuration
st.set_page_config(
    page_title="OxSecure RAG",
    page_icon="🤿",
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
            model = genai.GenerativeModel('gemini-1.5-pro-latest')
            response = model.generate_content([context + prompt, image])
        else:
            model = genai.GenerativeModel('gemini-1.5-pro-latest')
            response = model.generate_content(context + prompt)
        
        if hasattr(response, 'candidates') and response.candidates:
            return ' '.join(part.text for part in response.candidates[0].content.parts)
        else:
            st.error("Unexpected response format from Gemini API.")
            return None
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

# Function to extract text from CSV
def extract_text_from_csv(file):
    try:
        df = pd.read_csv(file)
        return df.to_string(index=False)
    except Exception as e:
        st.error(f"An error occurred while extracting text from CSV: {e}")
        return ""

# Function to extract text from Excel
def extract_text_from_excel(file):
    try:
        df = pd.read_excel(file)
        return df.to_string(index=False)
    except Exception as e:
        st.error(f"An error occurred while extracting text from Excel: {e}")
        return ""

# Function to extract text from JSON
def extract_text_from_json(file):
    try:
        json_data = json.load(file)
        formatted_text = json.dumps(json_data, indent=4)
        return formatted_text
    except Exception as e:
        st.error(f"An error occurred while extracting text from JSON: {e}")
        return ""

# Remove special characters and improve formatting
def clean_text(text):
    # Retain only alphabetic characters, numbers, punctuation, and spaces
    clean_text = re.sub(r'[^a-zA-Z0-9.,!?;:()\'\" \n]', '', text)
    return re.sub(r'\s+', ' ', clean_text).strip()

# Placeholder function to create embeddings
def embed_text(text):
    # This should be replaced with the actual embedding generation logic
    # For demonstration, return a dummy vector
    return np.random.rand(512).astype('float32')

# Function to create embeddings and store in FAISS
def store_embeddings(text):
    chunks = [text[i:i+512] for i in range(0, len(text), 512)]
    vectors = [embed_text(chunk) for chunk in chunks]
    dimension = vectors[0].shape[0]
    index = faiss.IndexFlatL2(dimension)
    index.add(np.array(vectors))
    return index, chunks

# Function to search embeddings and retrieve relevant text
def search_embeddings(index, query, top_k):
    query_vector = embed_text(query)  # Replace with actual embedding generation
    D, I = index.search(np.array([query_vector]), k=top_k)
    return I[0]

# Function to handle Q&A
def handle_qa(query, faiss_index, document_chunks, top_k):
    if faiss_index:
        retrieved_indices = search_embeddings(faiss_index, query, top_k)
        context = " ".join([document_chunks[i] for i in retrieved_indices])
        response = query_gemini(context, query)
    else:
        response = query_gemini(st.session_state.context, query)
    return response

# Function for speech recognition
def recognize_speech():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            st.info("Listening...")
            audio = r.listen(source)
            text = r.recognize_google(audio)
            st.success(f"You said: {text}")
            return text
    except sr.UnknownValueError:
        st.error("Could not understand audio")
        return None
    except sr.RequestError as e:
        st.error(f"Could not request results from Google Speech Recognition service; {e}")
        return None
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None

# Function to analyze log file
def analyze_log_file(file):
    log_summary = {
        'total_lines': 0,
        'error_count': 0,
        'warning_count': 0,
        'info_count': 0,
        'error_details': defaultdict(int),
        'warning_details': defaultdict(int),
        'info_details': defaultdict(int),
    }

    error_pattern = re.compile(r'\bERROR\b')
    warning_pattern = re.compile(r'\bWARNING\b')
    info_pattern = re.compile(r'\bINFO\b')

    with open(file, 'r') as file:
        for line in file:
            log_summary['total_lines'] += 1

            if error_pattern.search(line):
                log_summary['error_count'] += 1
                log_summary['error_details'][line.strip()] += 1
            elif warning_pattern.search(line):
                log_summary['warning_count'] += 1
                log_summary['warning_details'][line.strip()] += 1
            elif info_pattern.search(line):
                log_summary['info_count'] += 1
                log_summary['info_details'][line.strip()] += 1

    return log_summary

# Main App Function
def render_main_app():
    st.title('OxSecure RAG ♨️')
    st.divider()
    st.markdown('**By :- Aditya Pandey 🧑🏻‍💻**')

    input_prompt = st.text_input("Input Prompt: ", key="input")

    uploaded_file = st.file_uploader("Choose a file (image, PDF, CSV, Excel, JSON, or LOG)...", type=["jpg", "jpeg", "png", "pdf", "csv", "xlsx", "json", "log"])
    uploaded_url = st.text_input("Or enter an article URL:")

    image = None
    file_text = ""

    if uploaded_file is not None:
        if uploaded_file.type in ["image/jpeg", "image/png", "image/jpg", "image/webp"]:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image.", use_column_width=True)
        elif uploaded_file.type == "application/pdf":
            file_text = extract_text_from_pdf(uploaded_file)
            st.text_area("Extracted Text from PDF:", file_text, height=300)
        elif uploaded_file.type == "text/csv":
            df = pd.read_csv(uploaded_file)
            st.dataframe(df)
            file_text = df.to_string(index=False)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet":
            df = pd.read_excel(uploaded_file)
            st.dataframe(df)
            file_text = df.to_string(index=False)
        elif uploaded_file.type == "application/json":
            df = pd.read_json(uploaded_file)
            st.json(df.to_dict())
            file_text = df.to_string(index=False)
        elif uploaded_file.type == "text/plain":
            if uploaded_file.name.endswith(".log"):
                file_text = uploaded_file.read().decode("utf-8")
                log_summary = analyze_log_file(file_text.splitlines())
                st.write("Log Summary:")
                st.write(f"Total Lines: {log_summary['total_lines']}")
                st.write(f"Error Count: {log_summary['error_count']}")
                st.write(f"Warning Count: {log_summary['warning_count']}")
                st.write(f"Info Count: {log_summary['info_count']}")

                st.write("\nError Details:")
                for error, count in log_summary['error_details'].items():
                    st.write(f"{count} occurrence(s): {error}")

                st.write("\nWarning Details:")
                for warning, count in log_summary['warning_details'].items():
                    st.write(f"{count} occurrence(s): {warning}")

                st.write("\nInfo Details:")
                for info, count in log_summary['info_details'].items():
                    st.write(f"{count} occurrence(s): {info}")
            else:
                st.error("Please upload a valid log file.")
        else:
            st.error("Unsupported file type.")
    elif uploaded_url:
        file_text = extract_text_from_url(uploaded_url)
        st.text_area("Extracted Text from URL:", file_text, height=300)

    # Initialize or update session state for context
    if "context" not in st.session_state:
        st.session_state.context = ""
    if "faiss_index" not in st.session_state:
        st.session_state.faiss_index = None
    if "document_chunks" not in st.session_state:
        st.session_state.document_chunks = []

    def clear_previous_data():
        st.session_state.faiss_index = None
        st.session_state.document_chunks = []
        st.session_state.context = ""

    submit = st.button("Start Deep Diving 🤿", key="start_button")

    if submit:
        if input_prompt or file_text:
            clear_previous_data()
            
            prompt = input_prompt if input_prompt else ""
            st.session_state.context += " " + file_text  # Update the context with new extracted text
            
            if file_text:
                st.session_state.faiss_index, st.session_state.document_chunks = store_embeddings(file_text)
            
            # Start spinner before processing
            spinner = st.spinner("Processing..... Getting Results ⏳")
            with spinner:
                response = query_gemini(st.session_state.context, prompt, image)
            
            # Stop spinner after processing
            if response:
                st.subheader("Extracted Data 📡")
                st.write(response)
                
                clean_response = clean_text(response)

                # Text-to-Speech conversion
                tts = gTTS(clean_response)
                audio_file = BytesIO()
                tts.write_to_fp(audio_file)
                st.audio(audio_file, format='audio/mp3')
        else:
            st.warning("Please provide an input prompt or upload a file.")

    # Q&A section with slider and radio button
    st.markdown("-----")
    st.markdown("**Q/A Section 🤔**")

    query = st.text_input("Enter your query:", key="qa_query")
    top_k = st.slider("Select the number of document chunks to retrieve:", min_value=1, max_value=10, value=5, step=1)
    response_mode = st.radio("Select response mode:", ("Text", "Text-to-Speech"))

    qa_button = st.button("Ask", key="qa_button")
    
    if qa_button:
        if query:
            spinner = st.spinner("Processing your query...")
            with spinner:
                response = handle_qa(query, st.session_state.faiss_index, st.session_state.document_chunks, top_k)
            if response:
                st.divider()
                st.markdown("**Q&A Response 🤖**")
                
                clean_response = clean_text(response)
                
                if response_mode == "Text":
                    st.write(response)
                else:
                    st.write(response)
                    tts = gTTS(clean_response)
                    audio_file = BytesIO()
                    tts.write_to_fp(audio_file)
                    st.audio(audio_file, format='audio/mp3')
        else:
            st.warning("Please enter a query to ask.")
    
    st.markdown("-----")
    
    # Voice recognition section
#    st.markdown("**Voice Input 🗣️**")
#    query = recognize_speech()
#    if st.button("Start Voice Recognition") and query:
#        with st.spinner("Processing your voice query..."):
#            response = handle_qa(query, st.session_state.faiss_index, st.session_state.document_chunks, top_k)
#        if response:
#            st.divider()
#            st.markdown("**Voice Q&A Response 🤖**")
            
#            clean_response = clean_text(response)
#            st.write(clean_response)
#            tts = gTTS(clean_response)
#            audio_file = BytesIO()
#            tts.write_to_fp(audio_file)
#            st.audio(audio_file, format='audio/mp3')
#    st.markdown("---")
    linkedin_url = "https://www.linkedin.com/in/aditya-pandey-896109224"
    st.markdown(f"Created with 🤗 💖 By Aditya Pandey [ LinkedIn 🔗 ]({linkedin_url})")

# Description and Framework Section
def render_description_and_framework():
    st.title("OxSecure RAG - Description and Framework")
    st.markdown("----")
    st.markdown("""
    ## 🚀 ***Project Description*** 
    ----------------
    **OxSecure RAG** is your cybersecurity research companion! Powered by the Gemini API and crafted with smart prompts, it can analyze various documents, extract key insights, create embeddings, and support question-answering (Q&A) like never before. 🔍🛡️
    
     🛠️ ***Framework Used***
    - **Streamlit**: The sleek and interactive interface 🎨.
    - **FAISS**: Super-efficient similarity search and clustering for dense vectors ⚡.
    - **Pandas**: Handling and processing data files like a pro (CSV, Excel) 📊.
    - **PyPDF2**: Extracting text from PDFs with ease 📄.
    - **BeautifulSoup**: Scraping web data with precision 🌐.
    - **gTTS**: Giving the bot a voice with text-to-speech 🎙️.
    - **Google Generative AI (genai)**: Querying the powerful Gemini API 🧠.
    - **SpeechRecognition**: Turning your voice into input for hands-free interaction 🎧.
                
    ----------------

     🏗️ ***Architecture***
    1. **Input Handling**:
        - Upload various file types (PDF, CSV, Excel, JSON) or provide a URL 🔗.
        - Input text prompts directly 📝.
        - Speak your query using voice recognition 🎤.
    2. **Text Extraction**:
        - Extract text from uploaded files or URLs using the right tools 📄🌐.
    3. **Text Embedding**:
        - Split extracted text into chunks and convert them into embeddings 🧩.
        - Store embeddings in a FAISS index for fast, relevant search results 🚀.
    4. **Q&A System**:
        - Ask questions based on uploaded or entered context ❓.
        - Retrieve relevant text chunks from the FAISS index and query the Gemini API 🔍.
    5. **Response Generation**:
        - View the response from the Gemini API 🧑‍💻.
        - Convert the response to speech for audio playback 🔊.
                
    ----------------

     📋 ***Instructions for Use***
    1. **Input**:
        - Upload a file (PDF, CSV, Excel, or JSON), provide a URL, or enter a text prompt 💻.
    2. **Processing**:
        - Click "Start Deep Diving" to process the input and extract valuable insights 💡.
    3. **Q&A**:
        - Enter a query, choose how many document chunks to retrieve, and select response mode (Text or Text-to-Speech) 🎯.
        - Click "Ask" to get your answer 🧠.
    4. **Voice Input**:
        - Use "Start Voice Recognition" to ask a question verbally 🎙️.
        - The answer will be generated and spoken aloud 🗣️.
    5. **Results**:
        - View extracted data and responses in a clear, readable format 📑.
        - If Text-to-Speech is selected, listen to the response 🎧.
    """)

    if st.button("Go to Main App", key="description_go_to_main_app"):
        st.session_state.show_main_app = True
        st.experimental_rerun()
        
    st.markdown("---")
    linkedin_url = "https://www.linkedin.com/in/aditya-pandey-896109224"
    st.markdown(f"Created with 🤗 💖 By Aditya Pandey [ LinkedIn 🔗 ]({linkedin_url})")

# Initialize the app with the description and framework
if "show_main_app" not in st.session_state:
    st.session_state.show_main_app = False

if st.session_state.show_main_app:
    render_main_app()
else:
    render_description_and_framework()

