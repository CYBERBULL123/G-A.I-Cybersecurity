## Integrate our code GEMINI API
import os
import pathlib
import textwrap
from PIL import Image
from constants import gemini_key
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import PromptTemplate
from langchain.chains import LLMChain

import google.generativeai as genai

from langchain.memory import ConversationBufferMemory
from google.generativeai import GenerativeModel
from google.generativeai.types import HarmCategory, HarmBlockThreshold, HarmProbability
from langchain.chains import SequentialChain

import streamlit as st

# streamlit framework
st.set_page_config(
    page_title="OxSecure A.I",
    page_icon="🔒",
    layout="wide"
)

# Load custom CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the CSS file
load_css("ui/Style.css")

#API configuration

os.environ["GOOGLE_API_KEY"]=gemini_key
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

## Function to load OpenAI model and get respones

def get_gemini_response(input, image):
<<<<<<< HEAD
    model = genai.GenerativeModel('gemini-1.5-pro')
=======
    model = genai.GenerativeModel('gemini-1.5-pro-latest')
>>>>>>> main
    if input != "":
        response = model.generate_content(
            [input, image],
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                HarmProbability:HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
            }
        )
    else:
        response = model.generate_content(
            image,
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
                HarmProbability:HarmBlockThreshold.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
            }
        )
    return response.text


st.title('OxSecure Intelligence 🧠')
st.caption('Cybersecurity Best practices for Infrastructure')
st.subheader('By :- Aadi 🧑‍💻')
st.text('🚀 Empower Tomorrow, 🛡️ Secure Today: Unleash the Power of Cybersecurity Brilliance! 💻✨ ')
input_text=st.text_input("Search Your Desire Security Related Topic 🔍")
input=st.text_input("Input Prompt: ",key="input")
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
image=""
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)
submit=st.button("Tell me about the image")
if submit:
    
    response=get_gemini_response(input,image)
    st.subheader("The Response is")
    st.write(response)

# Prompt Templates

first_input_prompt=PromptTemplate(
    input_variables=['Topic'],
    template="Tell me everything about and explain in so informative descriptive way about {Topic} "
)

# Memory

Topic_memory = ConversationBufferMemory(input_key='Topic', memory_key='chat_history')
Policy_memory = ConversationBufferMemory(input_key='security policies', memory_key='chat_history')
Practice_memory = ConversationBufferMemory(input_key='Practice', memory_key='description_history')

# GEMINI LLMS
llm = ChatGoogleGenerativeAI(
<<<<<<< HEAD
    model="gemini-1.5-pro",
=======
    model="gemini-1.5-pro-latest",
>>>>>>> main
    safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        HarmProbability:HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE
    }
)
chain=LLMChain(llm=llm,prompt=first_input_prompt,verbose=True,output_key='security policies',memory=Topic_memory)

# Prompt Templates

second_input_prompt=PromptTemplate(
    input_variables=['security policies'],
    template="write best {security policies} and perfect code snippet for implementing secure coding to this {Topic} and give me all important full secure coding principles about {Topic} use codes snippet for every countersome points . "
)
chain2=LLMChain(
    llm=llm,prompt=second_input_prompt,verbose=True,output_key='Practice',memory=Policy_memory)
# Prompt Templates

third_input_prompt=PromptTemplate(
    input_variables=['Practice'],
    template="Implement  5 major best Cybersecurity {Practice} for this {Topic} that helps better security postures into infrastructure business. give Major cyberattack which is done by this {Topic} and write about malware which is developed by this {Topic}"
)
chain3=LLMChain(llm=llm,prompt=third_input_prompt,verbose=True,output_key='description',memory=Practice_memory)
parent_chain=SequentialChain(
    chains=[chain,chain2,chain3],input_variables=['Topic'],output_variables=['security policies','Practice','description'],verbose=True)



if input_text:
    st.text(parent_chain({'Topic':input_text}))

    with st.expander('Your Topic'): 
        st.info(Topic_memory.buffer)

    with st.expander('Major Practices'): 
        st.info(Practice_memory.buffer)
st.markdown("---")
st.markdown("                           Created with ❤️ by Aditya Pandey ")

