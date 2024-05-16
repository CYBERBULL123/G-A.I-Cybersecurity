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
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain
import google.generativeai as genai
from langchain.memory import ConversationBufferMemory
from google.generativeai.types import HarmCategory, HarmBlockThreshold, HarmProbability
from google.generativeai import GenerativeModel
from langchain.chains import SequentialChain

# Define correct username and password
CORRECT_USERNAME = "Oxsecure"
CORRECT_PASSWORD = "Oxsecure@123"

# streamlit framework
st.set_page_config(
    page_title="OxSecure A.I",
    page_icon="🔒",
    layout="wide"
)


def main():
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    # If not authenticated, display login portal
    if not st.session_state.authenticated:
        login_portal()
    else:
        render_main_program()

## Function to load Gemini vision model and get respones
def get_gemini_response(input,image):
    Model = genai.GenerativeModel('gemini-pro-vision')
    if input!="":
       response = Model.generate_content([input,image])
    else:
       response = model.generate_content(image)
    return response.text

def login_portal():
    st.title("Oxsecure 🧠 - Your Companion! 🔒")
    st.markdown("---")
    st.write("Unlock the realm of cybersecurity expertise with OxSecure Intelligence 🧠 🚀 Safeguarding your data, one prompt at a time. 🔒 Let's chat about security topics and empower your knowledge! 💡 Product of CyberBULL 👁️")
    st.markdown("---")
    st.write("Please log in to continue.")
    st.write("💳 Default Credentials  Username = Oxsecure , Password = Oxsecure@123 ")
    st.image('ui/Ox.jpg', width=200, use_column_width='always')
   

    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")
    login_button = st.sidebar.button("Login")

    if login_button:
        if username == CORRECT_USERNAME and password == CORRECT_PASSWORD:
            st.session_state.authenticated = True
            st.success("Login successful!")
            render_main_program()
        else:
            st.error("Invalid username or password. Please try again.")


def render_main_program():
    st.write("🚀 Empower Tomorrow, 🛡️ Secure Today: Unleash the Power of Cybersecurity Brilliance! 💻✨ 🛡️💬  ")
    st.markdown("---")

    st.title("OxSecure Intelligence 🧠")
    st.subheader('By :- Aadi 🧑‍💻')
    input_text = st.text_input("Search your Security Related Topic 🔍")
    input_prompt = st.text_input("Input Prompt:")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    image = ""
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)
    submit = st.button("Tell me about the image")
    if submit:
        response = get_gemini_response(input_prompt, image)
        st.subheader("The Response is")
        st.write(response)

    # Prompt Templates
    first_input_prompt = PromptTemplate(
        input_variables=['Topic'],
        template="Tell me everything about and explain in so informative descriptive way about {Topic}"
    )

    # API key configurations
    os.environ['GOOGLE_API_KEY'] = "AIzaSyAe5KT9cu1I4BOBXN5NsSxChF3_A1AA--s"
    genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

    # Select the model
    model = genai.GenerativeModel('gemini-pro')
    safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUAL: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_TOXICITY: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT:HarmProbability.HIGH
    }
    

    # Memory
    Topic_memory = ConversationBufferMemory(input_key='Topic', memory_key='chat_history')
    Policy_memory = ConversationBufferMemory(input_key='security policies', memory_key='chat_history')
    Practice_memory = ConversationBufferMemory(input_key='Practice', memory_key='description_history')

    ## GEMINI LLMS
    llm = ChatGoogleGenerativeAI(model="gemini-pro")
    chain = LLMChain(
        llm=llm, prompt=first_input_prompt, verbose=True, output_key='security policies', memory=Topic_memory)
    safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUAL: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_TOXICITY: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT:HarmProbability.HIGH
    }

    # Prompt Templates
    second_input_prompt = PromptTemplate(
        input_variables=['Policy'],
        template="write best {security policies} and perfect code snippet for implementing secure coding to this {Topic} in well detailed and descriptive "
    )

    chain2 = LLMChain(
        llm=llm, prompt=second_input_prompt, verbose=True, output_key='Practice', memory=Policy_memory)
    # Prompt Templates
    third_input_prompt = PromptTemplate(
        input_variables=['Practice'],
        template="Implement  5 major best Cybersecurity {Practice} for this {Topic} that helps better security postures into any business.  Major cyberattack which is done by misconfiguration of {Topic} and give the informative details , date , losses  that causes in this attack"
    )
    chain3 = LLMChain(llm=llm, prompt=third_input_prompt, verbose=True, output_key='description', memory=Practice_memory)
    parent_chain = SequentialChain(
        chains=[chain, chain2, chain3], input_variables=['Topic'], output_variables=['security policies', 'Practice',
                                                                                     'description'], verbose=True)

    if input_text:
        st.text(parent_chain({'Topic': input_text}))

        with st.expander('Your Topic'):
            st.info(Topic_memory.buffer)

        with st.expander('Major Practices'):
            st.info(Practice_memory.buffer)
    st.markdown("---")
    linkedin_url = "https://www.linkedin.com/in/aditya-pandey-896109224"
    st.markdown("  Created with 🤗 💖 By Aditya Pandey  "  f"[ LinkedIn 🔗 ]({linkedin_url})")

if __name__ == "__main__":
    main()
