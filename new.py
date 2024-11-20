import googletrans
import streamlit as st

# Available Indian regional languages
languages = {
    "English": "en",
    "Hindi": "hi",
    "Bengali": "bn",
    "Gujarati": "gu",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Marathi": "mr",
    "Punjabi": "pa",
    "Tamil": "ta",
    "Telugu": "te"
}

def translate_content(content, target_language):
    try:
        translator = googletrans.Translator()
        translated = translator.translate(content, dest=target_language)
        return translated.text
    except Exception as e:
        st.error(f"Translation failed: {e}")
        return content  # If translation fails, return the original content

# Example usage
language = st.selectbox("Select a language", list(languages.keys()))
content = "Hello, how are you?"  # Replace with your content
target_language = languages[language]
translated_content = translate_content(content, target_language)
st.write(translated_content)

