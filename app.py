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
import streamlit as st
from PIL import Image
import textwrap
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

#API configuration
os.environ["GOOGLE_API_KEY"]=gemini_key
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

# Define correct username and password
CORRECT_USERNAME = "Oxsecure"
CORRECT_PASSWORD = "Oxsecure@123"

# streamlit framework
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
    Model = genai.GenerativeModel('gemini-pro-vision')
    if input_prompt != "":
        response = Model.generate_content([input_prompt, image])
    else:
        response = Model.generate_content(image)
    return response.text

def render_main_program():
    st.markdown("# 🔒 Unlock the Future of Cybersecurity with OxSecure , **Where Knowledge Meets Innovation! 🚀 Dive into Cyber Brilliance with OxSecure** 🤖 🌟")
    st.markdown("----")
    app_choice = st.sidebar.radio("Choose App", ("OxSecure Chat 🤖", "OxSecure ImaGen 🎨"))

    if app_choice == "OxSecure Chat 🤖":
        render_gemini_api_app()
    elif app_choice == "OxSecure ImaGen 🎨":
        render_gemini_vision_app()

def render_gemini_api_app():
    st.caption("🚀 Empower Tomorrow, 🛡️ Secure Today: Unleash the Power of Cybersecurity Brilliance! 💻✨ 🛡️💬  ")
    st.markdown("---")

    st.title("OxSecure Intelligence 🧠")
    st.markdown("-----")
    input_text = st.text_input("Search your Security Related Topic 🔍")

    # Prompt Templates
    first_input_prompt = PromptTemplate(
        input_variables=['Topic'],
        template = textwrap.dedent("""
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
    model = genai.GenerativeModel('gemini-pro')
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
    llm = ChatGoogleGenerativeAI(model="gemini-pro")
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

def main():
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    # If not authenticated, display login portal
    if not st.session_state.authenticated:
        render_login_page()
    else:
        render_main_program()

if __name__ == "__main__":
    main()
