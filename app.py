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
# This code is for a chatbot crafted with powerful prompts, File analysis designed to
# utilize the Gemini API. It is tailored to assist cybersecurity researchers.
#
# Author: Aditya Pandey
# =============================================================================

import os
import streamlit as st
from PIL import Image
import textwrap
from io import BytesIO
import io
import chardet
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
    **Welcome to OxSecure Intelligence** 🔐 your ultimate destination for comprehensive and up-to-date information on cybersecurity. Whether you're a professional, student, or enthusiast, this app is designed to empower you with the knowledge and tools needed to navigate the complex world of cybersecurity.

    **Features**

    **📖 In-Depth Information on Cybersecurity Topics:**
    
    Explore a wide range of topics in cybersecurity with detailed articles and guides. This app covers everything from basic concepts to advanced techniques, ensuring you have access to the information you need to stay informed and secure.

    **💻 Secure Coding Principles:**
    
    Learn the best practices for secure coding to protect your software from vulnerabilities. These guides provide practical tips and examples to help you write code that is both functional and secure.

    **🚨 Major Cyberattacks:**
    
    Stay updated on major cyberattacks and learn from real-world cases. Understand the methods used by attackers, the impact of these attacks, and the measures you can take to protect yourself and your organization.

    **⚙️ Security Misconfiguration:**
    
    Identify common security misconfigurations and learn how to fix them. These resources help you ensure that your systems are configured correctly to prevent breaches and unauthorized access.

    **🔎 VirusTotal File Analysis:**
    
    Upload your files for in-depth malware scanning using the VirusTotal API. Instantly analyze your files and receive reports with threat intelligence on potential malware, ensuring your files are clean and secure.

    **🔐 Comprehensive File Analysis:**
    
    Use this app to scan a variety of file types like PDFs, images, executables, and logs. From extracting metadata to analyzing file content, OxSecure Intelligence ensures thorough and real-time security analysis.

    **🤖 Powered by Gemini LLM:**
    
    This app leverages the powerful Gemini LLM to provide you with accurate and relevant information. Gemini LLM enhances the content with cutting-edge insights and helps you get the answers you need quickly and efficiently.

    **🖼️ Image Analysis with Imagen:**
    
    Utilize the Imagen feature to extract detailed information from images. Simply upload an image, and our app will analyze it and provide responses tailored to your queries. Perfect for identifying vulnerabilities, assessing security measures, and more.

    **Why Choose OxSecure Intelligence?**

    - **🌐 Comprehensive Coverage:** From basic concepts to advanced practices, this app covers all aspects of cybersecurity.
    - **📚 Expert Guidance:** Learn from detailed articles and guides written by cybersecurity experts.
    - **⚡ Advanced Tools:** Use powerful AI tools like Gemini LLM, Imagen, and VirusTotal to enhance your learning and problem-solving capabilities.
    - **🔄 Stay Updated:** Keep up with the latest trends, threats, and best practices in the cybersecurity field.

    Join OxSecure Intelligence today and take your cybersecurity knowledge to the next level! 🚀
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
            st.experimental_rerun()
            render_main_program()
        else:
            st.error("Invalid username or password. Please try again.")

# Features Section
def features():
    st.write("***🔑 Key Features of OxSecure Intelligence***")
    
    with st.expander("📖 In-Depth Information on Cybersecurity Topics"):
        st.write("""
            **Expand Your Cybersecurity Knowledge**  
            Stay informed with detailed articles and guides covering a wide range of cybersecurity topics. Whether you're 
            learning basic concepts or exploring advanced techniques, this resource ensures you're well-equipped to handle 
            the latest cybersecurity challenges.
        """)
        
    with st.expander("💻 Secure Coding Principles"):
        st.write("""
            **Write Code that Stands the Test of Time**  
            Learn essential best practices for writing secure, reliable code. Our secure coding guides offer practical tips 
            and real-world examples to help you minimize vulnerabilities in your software.
        """)
        
    with st.expander("🚨 Major Cyberattacks"):
        st.write("""
            **Stay Informed on Critical Threats**  
            Keep up-to-date on the most significant cyberattacks around the world. Analyze real-world incidents, learn the 
            attack vectors used, and discover defensive strategies to protect against similar threats.
        """)
        
    with st.expander("⚙️ Security Misconfiguration"):
        st.write("""
            **Configure with Confidence**  
            Learn how to avoid common misconfigurations that leave systems exposed. This section provides a comprehensive 
            guide to correctly configuring security settings, protecting your organization from unnecessary risks.
        """)
        
    with st.expander("🔎 VirusTotal File Analysis"):
        st.write("""
            **Instant Malware Scanning**  
            Upload your files to run advanced malware scans via VirusTotal API. Get real-time reports with detailed threat 
            intelligence and analysis, ensuring your files are secure before you use or share them.
        """)
        
    with st.expander("🔐 Comprehensive File Analysis"):
        st.write("""
            **Analyze Multiple File Types**  
            OxSecure Intelligence allows you to scan PDFs, images, executables, and logs with ease. From extracting metadata 
            to conducting thorough file content analysis, you'll have all the tools you need to secure your files.
        """)
        
    with st.expander("🤖 Powered by Gemini LLM"):
        st.write("""
            **AI-Powered Insights**  
            Harness the cutting-edge power of Gemini LLM to get instant, accurate answers to your cybersecurity queries. 
            With AI-driven insights, you can navigate complex data and extract valuable knowledge faster than ever before.
        """)
        
    with st.expander("🖼️ Image Analysis with Imagen"):
        st.write("""
            **Visual Intelligence at Your Fingertips**  
            Upload images for detailed analysis using the Imagen feature. Whether you're assessing a security measure or 
            scanning for vulnerabilities, this tool ensures you get the most out of every image.
        """)
# Help and Use Section
def use_app():
    st.write("""
     🚀 ***OxSecure Intelligence: Use Cases***

OxSecure Intelligence is a comprehensive cybersecurity tool designed to provide in-depth information on various security topics, analyze images, and perform detailed file analysis. The app consists of three powerful tools:

🛡️ **1. OxSecure Chat**

 ***Use Case:***
**OxSecure Chat** allows users to gain a deep understanding of cybersecurity topics by generating detailed outputs based on the entered topics. This tool is ideal for:

- **Learning and Research:** Enter any cybersecurity topic to receive a thorough explanation, including secure coding principles and major attack vectors.
- **Training and Development:** Use the detailed outputs to educate teams or individuals about specific security concepts and practices.
- **Consultation and Advisory:** Provide clients or stakeholders with well-researched and comprehensive information on cybersecurity issues.

**How It Works:**
1. Enter a security topic related to cybersecurity.
2. Receive a detailed response including:
   - **Secure Coding Principles:** Best practices and guidelines.
   - **Major Attacks:** Common threats and attack methods.

🖼️ **2. OxSecure ImaGen**

 ***Use Case:***
**OxSecure ImaGen** offers advanced image analysis by allowing users to input prompts and retrieve detailed information about the image. This tool is perfect for:

- **Image Verification:** Analyze images to extract metadata and ensure they are authentic and unaltered.
- **Content Analysis:** Understand the content and context of images through custom prompts.
- **Forensic Analysis:** Utilize the tool in digital forensics to scrutinize image details for investigative purposes.

 **How It Works:**
1. Upload an image.
2. Enter prompts to specify the desired output.
3. Receive detailed information and insights based on the image content.

 📂 **3. File Analysis**

***Use Case:***
**File Analysis** is designed for thorough examination of files, providing essential metadata, hash information, and integrating with VirusTotal for comprehensive security analysis. This tool is valuable for:

- **File Verification:** Extract metadata and hash information to verify file integrity and authenticity.
- **Threat Detection:** Communicate with VirusTotal API to assess the file’s security status and identify potential threats.
- **Visual Analytics:** Obtain graphical representations of file analysis results to visualize threat levels and security metrics.

**How It Works:**
1. Upload a file.
2. Extract metadata and hash information.
3. Integrate with VirusTotal API for detailed security analysis.
4. View graphical reports and insights about the file.

---
**OxSecure Intelligence** empowers you with detailed insights and robust analysis tools to enhance your cybersecurity practices and ensure data integrity. Explore these tools to stay ahead of potential threats and make informed decisions!
     
**Why Choose OxSecure Intelligence?**
- **💡 Expert-Level Knowledge:** Powered by cutting-edge AI tools and deep research.
- **🔍 Thorough File Analysis:** Scanning and reporting for multiple file types.
- **🔐 Stay Secure:** Stay ahead of threats with real-time insights and expert guidance.
    """)

## Function to load Gemini vision model and get response
def get_gemini_response(input_prompt, image):
    Model = genai.GenerativeModel('gemini-1.5-pro')
    if input_prompt != "":
        response = Model.generate_content([input_prompt, image])
    else:
        response = Model.generate_content(image)
    return response.text

# Main App section
def render_main_program():
    st.markdown("# 🔒 Unlock the Future of Cybersecurity with OxSecure")
    st.divider()
    st.markdown("**Where Knowledge Meets Innovation! 🚀 Dive into Cyber Brilliance with OxSecure** 🤖 🌟")
    st.markdown("----")

    # Sidebar for navigation
    app_choice = st.sidebar.radio("Choose App", 
         ("Features 🤹🏻‍♀️", 
          "OxSecure Chat 🤖", 
          "OxSecure ImaGen 🎨", 
          "File Analysis 📁", 
          "Help & Uses 💁🏻"))
    
    #Main content selector
    # app_choice = st.selectbox(
    #     "Choose App",
    #     ["Features 🤹🏻‍♀️", "OxSecure Chat 🤖", "OxSecure ImaGen 🎨", "File Analysis 📁", "Help & Uses 💁🏻"]
    # )

    # Render the selected app based on user's choice
    if app_choice == "OxSecure Chat 🤖":
        render_gemini_api_app()
    elif app_choice == "OxSecure ImaGen 🎨":
        render_gemini_vision_app()
    elif app_choice == "File Analysis 📁":
        render_file_analysis_app()
    elif app_choice == "Features 🤹🏻‍♀️":
        features()
    elif app_choice == "Help & Uses 💁🏻":
        use_app()

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
    # Simplified regex to capture any log entry
    log_entry_regex = re.compile(r'(.*)')

    log_entries = []

    for line in log_content.splitlines():
        match = log_entry_regex.match(line)
        if match:
            log_entries.append({'Log Entry': match.group(1)})

    # Convert to DataFrame
    log_df = pd.DataFrame(log_entries)

    # Return the DataFrame with all log entries
    return log_df
    
# Function to create charts from VirusTotal results
def create_virus_total_charts(virus_total_results):
    if not virus_total_results:
        return None
    
    stats = virus_total_results['data']['attributes']['last_analysis_stats']
    labels = list(stats.keys())
    values = list(stats.values())

    fig, ax = plt.subplots(figsize=(5, 2))
    sns.barplot(x=labels, y=values, palette="viridis", ax=ax)
    ax.set_title("VirusTotal Analysis Results", fontsize=9, fontweight='bold')
    ax.set_xlabel("Analysis Types", fontsize=8)
    ax.set_ylabel("Count", fontsize=10)

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

def read_file_with_fallback(byte_data):
    try:
        # Attempt to read the file with UTF-8 encoding
        return byte_data.decode("utf-8")
    except UnicodeDecodeError:
        # If UTF-8 decoding fails, try to detect encoding
        byte_stream = io.BytesIO(byte_data)
        detected_encoding = chardet.detect(byte_data)['encoding']
        byte_stream.seek(0)  # Reset stream pointer
        return byte_stream.read().decode(detected_encoding, errors='replace')

def render_file_analysis_app():
    st.title("🔍 File Analysis 🗃️")
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
            st.image(image, width=240, caption='Uploaded Image', use_column_width=True)
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


        elif file_extension == 'pdf':
            st.write("### 📄 PDF File")
            st.write("PDF preview is not supported. Please use other tools to view.")
            st.download_button(label="Download PDF", data=uploaded_file, file_name=uploaded_file.name)
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

        elif file_extension in ['txt', 'log']:
            st.write("### 📝 Log File Content")
            log_content = read_file_with_fallback(uploaded_file.getvalue())
            log_analysis = analyze_log_file(log_content)
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
            
            log_analysis = analyze_log_file(log_content)

        elif file_extension in ['zip', 'rar']:
            st.write("### 📦 Compressed File")
            st.write("Compressed files require further extraction and analysis.")
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
