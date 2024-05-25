import streamlit.components.v1 as components

# Declare the component ( HTML file is in a 'public' folder)
voice_recognition_component = components.declare_component(
    "voice_recognition",
    path="public"
)

def get_voice_input():
    return voice_recognition_component()
