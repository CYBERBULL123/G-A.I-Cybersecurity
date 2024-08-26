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
# This code is for a chatbot , Malware check crafted with powerful prompts, designed to
# utilize the Gemini API. It is tailored to assist cybersecurity researchers.
#
# Author: Aditya Pandey
# =============================================================================

import os
import streamlit as st
from PIL import Image
import textwrap
from io import BytesIO
from constants import gemini_key
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain
import google.generativeai as genai
from langchain.memory import ConversationBufferMemory
from google.generativeai.types import HarmCategory, HarmBlockThreshold, HarmProbability
from google.generativeai import GenerativeModel
from langchain.chains import SequentialChain
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import requests
from pefile import PE, PEFormatError
import re
import hashlib

# VirusTotal API details
VIRUSTOTAL_API_KEY = 'ed48e6407e0b7975be7d19c797e1217f500183c9ae84d1119af8628ba4c98c3d'


# API configuration
os.environ["GOOGLE_API_KEY"] = gemini_key
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Define correct username and password
CORRECT_USERNAME = "Oxsecure"
CORRECT_PASSWORD = "Oxsecure@123"

# Streamlit framework
st.set_page_config(
    page_title="OxSecure",
    page_icon="🔒",
    layout="wide"
)

# Load custom CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the CSS file
load_css("ui/Style.css")

def render_login_page():
    st.title("Oxsecure 🧠 - Your Companion! 🔒")
    st.markdown("---")
    st.image('ui/Ox.jpg', width=200, use_column_width='always')
    st.write("Unlock the realm of cybersecurity expertise with OxSecure 🧠 🚀 Safeguarding your data. 🔒 Let's chat about security topics and empower your knowledge! Product of CyberBULL 👁️")
    st.markdown("---")
    st.write("Please log in to continue.")
    st.write("💳 Default Credentials  Username = Oxsecure , Password = Oxsecure@123 ")
    st.divider()
    st.markdown("""
    **Welcome to OxSecure Intelligence** your ultimate destination for comprehensive and up-to-date information on cybersecurity. Whether you're a professional, student, or enthusiast, This app is designed to empower you with the knowledge and tools needed to navigate the complex world of cybersecurity.

    **Features**

    **In-Depth Information on Cybersecurity Topics:**
    
    Explore a wide range of topics in cybersecurity with detailed articles and guides. This app covers everything from basic concepts to advanced techniques, ensuring you have access to the information you need to stay informed and secure.

    **Secure Coding Principles:**
    
    Learn the best practices for secure coding to protect your software from vulnerabilities. This guides provide practical tips and examples to help you write code that is both functional and secure.

    **Major Cyberattacks:**
    
    Stay updated on major cyberattacks and learn from real-world cases. Understand the methods used by attackers, the impact of these attacks, and the measures you can take to protect yourself and your organization.

    **Security Misconfiguration:**
    
    Identify common security misconfigurations and learn how to fix them. This resources help you ensure that your systems are configured correctly to prevent breaches and unauthorized access.

    **Powered by Gemini LLM:**
    
    This app leverages the powerful Gemini LLM to provide you with accurate and relevant information. Gemini LLM enhances This content with cutting-edge insights and helps you get the answers you need quickly and efficiently.

    **Image Analysis with Imagen:**
    
    Utilize Imagen feature to extract detailed information from images. Simply upload an image, and our app will analyze it and provide responses tailored to your queries. This tool is perfect for identifying vulnerabilities, assessing security measures, and more.

    **Why Choose OxSecure Intelligence?**
    
    - **Comprehensive Coverage:** From basic concepts to advanced practices, This app covers all aspects of cybersecurity.
    - **Expert Guidance:** Learn from detailed articles and guides written by cybersecurity experts.
    - **Advanced Tools:** Use powerful AI tools like Gemini LLM and Imagen to enhance your learning and problem-solving capabilities.
    - **Stay Updated:** Keep up with the latest trends, threats, and best practices in the cybersecurity field.

    Join OxSecure Intelligence today and take your cybersecurity knowledge to the next level!
    """)
    st.markdown("---")
    linkedin_url = "https://www.linkedin.com/in/aditya-pandey-896109224"
    st.markdown("  Created with 🤗💖 By Aditya Pandey  " f"[  LinkedIn 🔗]({linkedin_url})")

    username = st.sidebar.text_input("Username 👤")
    password = st.sidebar.text_input("Password 🔑", type="password")
    login_button = st.sidebar.button("Login 🫢")

    if login_button:
        if username == CORRECT_USERNAME and password == CORRECT_PASSWORD:
            st.session_state.authenticated = True
            st.success("Login successful!")
            render_main_program()
        else:
            st.error("Invalid username or password. Please try again.")

## Function to load Gemini vision model and get response
def get_gemini_response(input_prompt, image):
    Model = genai.GenerativeModel('gemini-1.5-pro')
    if input_prompt != "":
        response = Model.generate_content([input_prompt, image])
    else:
        response = Model.generate_content(image)
    return response.text


def render_main_program():
    st.markdown("# 🔒 Unlock the Future of Cybersecurity with OxSecure ")
    st.divider()
    st.markdown("**Where Knowledge Meets Innovation! 🚀 Dive into Cyber Brilliance with OxSecure** 🤖 🌟")
    st.markdown("----")
    app_choice = st.sidebar.radio("Choose App", ("OxSecure Chat 🤖", "OxSecure ImaGen 🎨", "File Analysis 📁"))

    if app_choice == "OxSecure Chat 🤖":
        render_gemini_api_app()
    elif app_choice == "OxSecure ImaGen 🎨":
        render_gemini_vision_app()
    elif app_choice == "File Analysis 📁":
        render_file_analysis_app()

def render_gemini_api_app():
    st.caption("🚀 Empower Tomorrow, 🛡️ Secure Today: Unleash the Power of Cybersecurity Brilliance! 💻✨ 🛡️💬  ")
    st.markdown("---")

    st.title("OxSecure Intelligence 🧠")
    st.markdown("-----")
    input_text = st.text_input("Search your Security Related Topic 🔍")

    # Prompt Templates
    first_input_prompt = PromptTemplate(
        input_variables=['Topic'],
        template=textwrap.dedent("""
            As an experienced cybersecurity researcher, provide a comprehensive and detailed explanation about {Topic}. Cover the following aspects:
            1. Introduction and Importance in well informative
            2. Key Concepts and Terminologies
            3. Historical Background and Evolution
            4. Its Architecture and Types
            5. Current Trends and Best Practices
            6. Major Threats and Vulnerabilities
            7. Case Studies and Real-world Examples
            8. Future Outlook and Predictions
            
            Ensure the information is professional, well-structured, key conceptual  and suitable for someone with an advanced understanding and Beginner of cybersecurity.
        """)
    )

    # Select the model
    model = genai.GenerativeModel('gemini-1.5-pro')
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUAL: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_TOXICITY: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmProbability.HIGH
    }

    # Memory
    Topic_memory = ConversationBufferMemory(input_key='Topic', memory_key='chat_history')
    Policy_memory = ConversationBufferMemory(input_key='secure coding', memory_key='chat_history')
    Practice_memory = ConversationBufferMemory(input_key='Practice', memory_key='description_history')

    ## GEMINI LLMS
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro")
    chain = LLMChain(
        llm=llm, prompt=first_input_prompt, verbose=True, output_key='secure coding', memory=Topic_memory)
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUAL: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_TOXICITY: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmProbability.HIGH
    }
    # Prompt Templates
    second_input_prompt = PromptTemplate(
        input_variables=['secure coding'],
        template="write best {secure coding} and perfect code snippet for implementing secure coding to this {Topic} in well detailed and descriptive way use code snippets for each point and describe code."
    )

    chain2 = LLMChain(
        llm=llm, prompt=second_input_prompt, verbose=True, output_key='Practice', memory=Policy_memory)
    # Prompt Templates
    third_input_prompt = PromptTemplate(
        input_variables=['Practice'],
        template="Implement major best Cybersecurity {Practice} for this {Topic} that helps better security postures into any business. illustrate Major cyberattack which is done by misconfiguration of {Topic} and give the informative info about the malware which caused this"
    )
    chain3 = LLMChain(llm=llm, prompt=third_input_prompt, verbose=True, output_key='description', memory=Practice_memory)
    parent_chain = SequentialChain(
        chains=[chain, chain2, chain3], input_variables=['Topic'], output_variables=['secure coding', 'Practice',
                                                                                     'description'], verbose=True)

    if input_text:
        with st.spinner('Processing.... ⏳'):
            st.text(parent_chain({'Topic': input_text}))

        with st.expander('Your Topic'):
            st.info(Topic_memory.buffer)

        with st.expander('Major Practices'):
            st.info(Practice_memory.buffer)
    st.markdown("---")
    linkedin_url = "https://www.linkedin.com/in/aditya-pandey-896109224"
    st.markdown("  Created with 🤗💖 By Aditya Pandey   "  f"[  LinkedIn 🔗]({linkedin_url})")


def render_gemini_vision_app():
    st.title('OxSecure ImaGen 🎨')
    st.markdown("----")
    input_prompt = st.text_input("Input Prompt: ", key="input")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    image = ""
    submit = False  # Initialize submit variable

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)
        submit = st.button("Tell me about the image")

    if submit:
        response = get_gemini_response(input_prompt, image)
        st.subheader("The Response is")
        st.write(response)

    st.markdown("---")
    linkedin_url = "https://www.linkedin.com/in/aditya-pandey-896109224"
    st.markdown("  Created with 🤗💖 By Aditya Pandey  " f"[  LinkedIn 🔗]({linkedin_url})")


def get_file_hash(file):
    file.seek(0)  # Reset file pointer to the beginning
    file_hash = hashlib.sha256(file.read()).hexdigest()
    file.seek(0)  # Reset file pointer to the beginning
    return file_hash

# Function to analyze the file using VirusTotal
def virustotal_analysis(file_hash):
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    headers = {"x-apikey": VIRUSTOTAL_API_KEY}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Error with VirusTotal API request. Please check your API key or the file hash.")
        return None

# Function to extract metadata from PE files
def extract_metadata(file):
    try:
        pe = PE(data=file.read())
        metadata = {
            "Number of Sections": pe.FILE_HEADER.NumberOfSections,
            "Time Date Stamp": pe.FILE_HEADER.TimeDateStamp,
            "Characteristics": pe.FILE_HEADER.Characteristics,
        }
        return metadata
    except PEFormatError:
        st.error("Uploaded file is not a valid PE format.")
        return None

# Function to analyze log files
def analyze_log_file(log_content):
    errors = re.findall(r'ERROR.*', log_content)
    return pd.DataFrame(errors, columns=["Errors"])

# Function to create charts from VirusTotal results
def create_virus_total_charts(virus_total_results):
    if not virus_total_results:
        return None
    
    stats = virus_total_results['data']['attributes']['last_analysis_stats']
    labels = list(stats.keys())
    values = list(stats.values())

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=labels, y=values, palette="viridis", ax=ax)
    ax.set_title("VirusTotal Analysis Results", fontsize=16, fontweight='bold')
    ax.set_xlabel("Analysis Types", fontsize=14)
    ax.set_ylabel("Count", fontsize=14)

    return fig

# Function to create detailed tables from JSON data
def create_detailed_table(data, title):
    st.write(f"{title}")
    
    # Normalize JSON data into a DataFrame
    df = pd.json_normalize(data)
    
    # Debug: Show raw data and DataFrame
    st.write("Raw Data:", data)

    if df.empty:
        st.write("No data available.")
    else:
        # Apply minimal styling for debugging
        styled_df = df.style.background_gradient(cmap='viridis') \
                          .format(na_rep='N/A', precision=2)
        
        # Display the styled DataFrame
        st.dataframe(styled_df)

# Function to display the analysis results on the dashboard
def display_analysis_results(metadata, virus_total_results, log_analysis=None):
    st.write("## Analysis Results")

    # Metadata
    if metadata:
        st.write("### 📂 PE File Metadata")
        create_detailed_table(metadata, "PE File Metadata")

    # VirusTotal Results
    if virus_total_results:
        st.write("### 🦠 VirusTotal Results")
        create_detailed_table(virus_total_results['data'], "VirusTotal Results")
        st.write("#### 📊 VirusTotal Analysis Stats")
        fig = create_virus_total_charts(virus_total_results)
        if fig:
            st.pyplot(fig)

    # Log Analysis
    if log_analysis is not None:
        st.write("### 📝 Log Analysis")
        st.table(log_analysis)


def render_file_analysis_app():
    st.title("🔍 File Analysis Dashboard")
    st.markdown("---")
    st.image('ui/antivirus.png', width=80, use_column_width='none')

    uploaded_file = st.file_uploader("Upload any file for analysis", type=["exe", "dll", "log", "pdf", "png", "jpg", "jpeg", "gif", "txt", "zip", "rar", "apk"])

    if uploaded_file:
        file_hash = get_file_hash(uploaded_file)
        st.write(f"SHA-256 Hash: {file_hash}")

        file_extension = uploaded_file.name.split('.')[-1].lower()

        # Handle different file types
        if file_extension in ['png', 'jpg', 'jpeg', 'gif']:
            st.write("### 📄 Image Preview")
            image = Image.open(uploaded_file)
            image.thumbnail((512, 512))  # Resize for preview
            st.image(image, caption='Uploaded Image', use_column_width=True)
            metadata = None
            virus_total_results = None
            log_analysis = None

        elif file_extension == 'pdf':
            st.write("### 📄 PDF File")
            st.write("PDF preview is not supported. Please use other tools to view.")
            st.download_button(label="Download PDF", data=uploaded_file, file_name=uploaded_file.name)
            metadata = None
            virus_total_results = None
            log_analysis = None

        elif file_extension in ['txt', 'log']:
            st.write("### 📝 Log File Content")
            log_content = uploaded_file.getvalue().decode("utf-8")
            log_analysis = analyze_log_file(log_content)
            metadata = None
            virus_total_results = None

        elif file_extension in ['zip', 'rar']:
            st.write("### 📦 Compressed File")
            st.write("Compressed files require further extraction and analysis.")
            metadata = None
            virus_total_results = None
            log_analysis = None

        elif file_extension in ['apk', 'exe', 'dll']:
            # Save uploaded file temporarily
            file_path = f"./temp/{uploaded_file.name}"
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            try:
                with open(file_path, "rb") as file:
                    file_hash = get_file_hash(file)
                    metadata = extract_metadata(file)
                    virus_total_results = virustotal_analysis(file_hash)

            finally:
                # Clean up
                os.remove(file_path)
            
            log_analysis = None

        else:
            st.error("Unsupported file type.")
            metadata = None
            virus_total_results = None
            log_analysis = None

        display_analysis_results(metadata, virus_total_results, log_analysis)
                

    st.markdown("---")
    linkedin_url = "https://www.linkedin.com/in/aditya-pandey-896109224"
    st.markdown("  Created with 🤗💖 By Aditya Pandey  " f"[  LinkedIn 🔗]({linkedin_url})")


def main():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        render_main_program()
    else:
        render_login_page()

if __name__ == "__main__":
    main()
