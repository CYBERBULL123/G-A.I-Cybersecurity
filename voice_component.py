import os
import streamlit.components.v1 as components

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the path to the 'public' directory
build_dir = os.path.join(current_dir, "public")

# Declare the component
voice_recognition_component = components.declare_component(
    "voice_recognition",
    path=build_dir
)

def get_voice_input():
    return voice_recognition_component()
