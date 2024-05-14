## Integrate our code Gemini API
import os
import pathlib
import textwrap
from PIL import Image
from constants import gemini_key
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from google.generativeai import GenerativeModel
from langchain.chains import SequentialChain
import google.generativeai as genai
import streamlit as st


# streamlit framework
st.set_page_config(
    page_title="OxSecure Images",
    page_icon="🎨",
    layout="wide"
)

#API configuration
os.environ["GOOGLE_API_KEY"]=gemini_key
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])


## Function to load Gemini vision model and get respones
def get_gemini_response(input,image):
    model = genai.GenerativeModel('gemini-pro-vision')
    if input!="":
       response = model.generate_content([input,image])
    else:
       response = model.generate_content(image)
    return response.text

#Streamlit Main Framework

st.header('OxSecure ImaGen 🎨')
st.title('GenAI ImaGen powers ♨️ ')
st.subheader('By :- Aadi 🧑‍💻')
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