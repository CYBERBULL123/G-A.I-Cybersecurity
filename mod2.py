## Integrate our code OpenAI API
import os
import pathlib
import textwrap
from PIL import Image
from constants import gemini_key
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain

import google.generativeai as genai

from langchain.memory import ConversationBufferMemory
from google.generativeai import GenerativeModel
from langchain.chains import SequentialChain

import streamlit as st

os.environ["GOOGLE_API_KEY"]=gemini_key
genai.configure(api_key = os.environ['GOOGLE_API_KEY'])

## Function to load OpenAI model and get respones

def get_gemini_response(input,image):
    model = genai.GenerativeModel('gemini-pro-vision')
    if input!="":
       response = model.generate_content([input,image])
    else:
       response = model.generate_content(image)
    return response.text

# streamlit framework
st.header('LLM 2nd MOD')
st.title('Cybersecurity Best practices for Infrastructure')
st.subheader('By :- Aadi OP ')
st.text('API key is valid Gemini-pro  :) ')
input_text=st.text_input("Search Your Desire Security Policy")
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
    template="Tell me everything about {Topic}"
)

# Memory

Topic_memory = ConversationBufferMemory(input_key='Topic', memory_key='chat_history')
Policy_memory = ConversationBufferMemory(input_key='Policy', memory_key='chat_history')
Practice_memory = ConversationBufferMemory(input_key='Practice', memory_key='description_history')

## GEMINI LLMS
llm = ChatGoogleGenerativeAI(model="gemini-pro")
chain=LLMChain(
    llm=llm,prompt=first_input_prompt,verbose=True,output_key='Policy',memory=Topic_memory)

# Prompt Templates

second_input_prompt=PromptTemplate(
    input_variables=['Policy'],
    template="when was {Policy} Discoverd and by Whom"
)

chain2=LLMChain(
    llm=llm,prompt=second_input_prompt,verbose=True,output_key='Practice',memory=Policy_memory)
# Prompt Templates

third_input_prompt=PromptTemplate(
    input_variables=['Practice'],
    template="Implement  5 major best Cybersecurity {Practice} in the business Infrastructure world"
)
chain3=LLMChain(llm=llm,prompt=third_input_prompt,verbose=True,output_key='description',memory=Practice_memory)
parent_chain=SequentialChain(
    chains=[chain,chain2,chain3],input_variables=['Topic'],output_variables=['Policy','Practice','description'],verbose=True)


if input_text:
    st.text(parent_chain({'Topic':input_text}))

    with st.expander('Your Topic'): 
        st.info(Topic_memory.buffer)

    with st.expander('Major Practices'): 
        st.info(Practice_memory.buffer)

