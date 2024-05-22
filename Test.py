# Import necessary libraries
import streamlit as st
from transformers import ImageGenerationPipeline

# Function to generate images based on prompts using Hugging Face's models
def generate_image_hf(prompt, model_name, temperature=1.0, top_k=50, top_p=0.95, max_length=32, num_return_sequences=1):
    try:
        # Initialize the ImageGenerationPipeline with the specified model
        generator = ImageGenerationPipeline(model_name)
        
        # Generate images based on the prompt with user-defined parameters
        images = generator(
            prompt,
            max_length=max_length,
            num_return_sequences=num_return_sequences,
            temperature=temperature,
            top_k=top_k,
            top_p=top_p
        )
        return images
    except Exception as e:
        st.error(f"An error occurred while generating the image: {e}")
        return []

# Streamlit main framework
st.header('Image Generation with Hugging Face 🖼️')
st.write('By: Aditya Pandey')

# Input prompt for image generation
prompt = st.text_input("Image Prompt:", key="image_input")

# Model selection dropdown
model_name = st.selectbox("Select Model:", ["openai/clip-vit-base-patch32", "openai/clip-vit-base-patch16"])

# Parameters for image generation
temperature = st.slider("Temperature:", min_value=0.1, max_value=2.0, value=1.0, step=0.1, format="%.1f")
top_k = st.slider("Top-k:", min_value=1, max_value=100, value=50, step=1)
top_p = st.slider("Top-p:", min_value=0.1, max_value=1.0, value=0.95, step=0.05, format="%.2f")

# Generate button
generate_button = st.button("Generate Image")

if generate_button:
    if prompt:
        # Generate images based on the prompt using the selected model and user-defined parameters
        images = generate_image_hf(prompt, model_name, temperature, top_k, top_p)
        
        if images:
            # Display the generated images
            for i, image in enumerate(images):
                st.image(image, caption=f"Generated Image {i+1}", use_column_width=True)
        else:
            st.error("Failed to generate images.")
    else:
        st.warning("Please provide a prompt for image generation.")
