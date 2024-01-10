## Integrate our code OpenAI API
import os
from constants import openai_key
from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain

from langchain.memory import ConversationBufferMemory

from langchain.chains import SequentialChain

import streamlit as st

os.environ["OPENAI_API_KEY"]=openai_key

# streamlit framework
st.header('LLM 1st MOD')
st.title('Cybersecurity Best practices for Infrastructure')
st.subheader('By :- Aadi OP ')
st.text('API key is not  valid because I did not Buy  :( ')
input_text=st.text_input("Search Your Desire Security Policy")

# Prompt Templates

first_input_prompt=PromptTemplate(
    input_variables=['Topic'],
    template="Tell me everything about {Topic}"
)

# Memory

Topic_memory = ConversationBufferMemory(input_key='Topic', memory_key='chat_history')
Policy_memory = ConversationBufferMemory(input_key='Policy', memory_key='chat_history')
Practice_memory = ConversationBufferMemory(input_key='Practice', memory_key='description_history')

## OPENAI LLMS
llm=OpenAI(temperature=0.8)
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
    st.write(parent_chain({'Topic':input_text}))

    with st.expander('Your Topic'): 
        st.info(person_memory.buffer)

    with st.expander('Major Practices'): 
        st.info(descr_memory.buffer)
