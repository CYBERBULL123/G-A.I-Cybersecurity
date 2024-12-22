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
# This code is for Oximagen, a project focused on leveraging AI to 
# enhance imaging Genertation and storytelling.
#
# Author: Aditya Pandey
# =============================================================================

import os
import streamlit as st
from PIL import Image
import google.generativeai as genai
import aiohttp
import asyncio
import random
from gtts import gTTS
import re
import io
from io import BytesIO
import uuid
import time
import logging
from constants import gemini_key , huggingface_key
from googletrans import Translator


# Load custom CSS
def load_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the CSS file
load_css("ui/Style.css")

# Style list with different art styles
style_list = [
    {
        "name": "None",
        "prompt": "{prompt}",
        "negative_prompt": "",
    },
    {
        "name": "Cinematic 🎥",
        "prompt": "cinematic still {prompt} . emotional, harmonious, vignette, highly detailed, high budget, bokeh, cinemascope, moody, epic, gorgeous, film grain, grainy",
        "negative_prompt": "anime, cartoon, graphic, text, painting, crayon, graphite, abstract, glitch, deformed, mutated, ugly, disfigured",
    },
    {
        "name": "Photographic 📸",
        "prompt": "cinematic photo {prompt} . 35mm photograph, film, bokeh, professional, 4k, highly detailed",
        "negative_prompt": "drawing, painting, crayon, sketch, graphite, impressionist, noisy, blurry, soft, deformed, ugly",
    },
    {
        "name": "Anime 🎨",
        "prompt": "anime artwork {prompt} . anime style, key visual, vibrant, studio anime, highly detailed",
        "negative_prompt": "photo, deformed, black and white, realism, disfigured, low contrast",
    },
    {
        "name": "Manga 📚",
        "prompt": "manga style {prompt} . vibrant, high-energy, detailed, iconic, Japanese comic style",
        "negative_prompt": "ugly, deformed, noisy, blurry, low contrast, realism, photorealistic, Western comic style",
    },
    {
        "name": "Digital Art 🧑🏻‍🎨",
        "prompt": "concept art {prompt} . digital artwork, illustrative, painterly, matte painting, highly detailed",
        "negative_prompt": "photo, photorealistic, realism, ugly",
    },
    {
        "name": "Pixel Art 🕹️",
        "prompt": "pixel-art {prompt} . low-res, blocky, pixel art style, 8-bit graphics",
        "negative_prompt": "sloppy, messy, blurry, noisy, highly detailed, ultra textured, photo, realistic",
    },
    {
        "name": "Fantasy Art 🧚‍♀️",
        "prompt": "ethereal fantasy concept art of {prompt} . magnificent, celestial, ethereal, painterly, epic, majestic, magical, fantasy art, cover art, dreamy",
        "negative_prompt": "photographic, realistic, realism, 35mm film, dslr, cropped, frame, text, deformed, glitch, noise, noisy, off-center, deformed, cross-eyed, closed eyes, bad anatomy, ugly, disfigured, sloppy, duplicate, mutated, black and white",
    },
    {
        "name": "Neonpunk 🌆",
        "prompt": "neonpunk style {prompt} . cyberpunk, vaporwave, neon, vibes, vibrant, stunningly beautiful, crisp, detailed, sleek, ultramodern, magenta highlights, dark purple shadows, high contrast, cinematic, ultra detailed, intricate, professional",
        "negative_prompt": "painting, drawing, illustration, glitch, deformed, mutated, cross-eyed, ugly, disfigured",
    },
    {
        "name": "3D Model 🏆",
        "prompt": "professional 3d model {prompt} . octane render, highly detailed, volumetric, dramatic lighting",
        "negative_prompt": "ugly, deformed, noisy, low poly, blurry, painting",
    },
    {
        "name": "Impressionism 🎨",
        "prompt": "impressionist artwork {prompt} . vibrant, expressive brushstrokes, rich colors, painterly",
        "negative_prompt": "photo, photorealistic, clean lines, abstract",
    },
    {
        "name": "Cubism 🎭",
        "prompt": "cubist artwork {prompt} . fragmented, geometric, abstract forms, multiple perspectives",
        "negative_prompt": "realistic, smooth, conventional forms",
    },
    {
        "name": "Surrealism 🌀",
        "prompt": "surrealistic artwork {prompt} . dreamlike, bizarre, imaginative, otherworldly",
        "negative_prompt": "realistic, conventional, mundane",
    },
    {
        "name": "Pop Art 🌈",
        "prompt": "pop art {prompt} . bold colors, graphic design, comic-style, modern culture",
        "negative_prompt": "traditional art, subdued colors, abstract",
    },
    {
        "name": "Sketch Art ✏️",
        "prompt": "sketch art {prompt} . pencil drawings, detailed lines, rough texture",
        "negative_prompt": "colorful, digital, polished",
    },
    {
        "name": "Graffiti 🎨",
        "prompt": "graffiti art {prompt} . urban, colorful, bold strokes, street art, spray paint effects",
        "negative_prompt": "realistic, subdued colors, traditional",
    },
    {
        "name": "Art Nouveau 🌸",
        "prompt": "art nouveau {prompt} . flowing lines, organic forms, intricate patterns, floral elements",
        "negative_prompt": "modern, geometric, minimalist",
    },
    {
        "name": "Baroque 🕯️",
        "prompt": "baroque artwork {prompt} . dramatic lighting, rich colors, ornate details, grandeur",
        "negative_prompt": "minimalist, abstract, contemporary",
    },
    {
        "name": "Realism 🌍",
        "prompt": "realistic painting of {prompt} . true-to-life, detailed, accurate representation, everyday life",
        "negative_prompt": "abstract, surreal, exaggerated, stylized",
    },
    {
        "name": "Futurism 🚀",
        "prompt": "futuristic artwork {prompt} . dynamic, movement, energy, technology, speed",
        "negative_prompt": "static, traditional, slow, classic",
    },
    {
        "name": "Collage 🖼️",
        "prompt": "collage art of {prompt} . mixed media, layered textures, various materials, visual storytelling",
        "negative_prompt": "clean, polished, digital, smooth",
    },
    {
        "name": "Retro Vintage 📻",
        "prompt": "retro vintage style {prompt} . nostalgic, faded colors, classic design, old-school charm",
        "negative_prompt": "modern, high-tech, flashy, new",
    },
    {
        "name": "Conceptual Art 💡",
        "prompt": "conceptual artwork {prompt} . thought-provoking, idea-driven, avant-garde, experimental",
        "negative_prompt": "traditional, realistic, conventional, mainstream",
    },
    {
        "name": "Bauhaus 🏢",
        "prompt": "bauhaus style {prompt} . functional, geometric, minimalistic, industrial design",
        "negative_prompt": "ornate, decorative, complex, traditional",
    },
    {
        "name": "Minimalism ➖",
        "prompt": "minimalist artwork of {prompt} . simplicity, clean lines, few colors, essential forms",
        "negative_prompt": "complex, detailed, busy, ornate",
    },
    {
        "name": "Expressionism 🎭",
        "prompt": "expressionist art of {prompt} . emotional, subjective, vivid colors, distorted forms",
        "negative_prompt": "realism, precise, clean, conventional",
    },
    {
        "name": "Traditional Chinese 🏮",
        "prompt": "traditional Chinese painting of {prompt} . delicate brushwork, ink wash, natural subjects, harmony",
        "negative_prompt": "modern, abstract, digital",
    },
    {
        "name": "Traditional Japanese 🎋",
        "prompt": "traditional Japanese art of {prompt} . ukiyo-e style, woodblock prints, nature themes, elegance",
        "negative_prompt": "modern, Western, chaotic",
    },
    {
        "name": "Victorian 🎩",
        "prompt": "victorian style {prompt} . ornate, detailed, romantic, historical elements",
        "negative_prompt": "minimalist, modern, abstract",
    },
    {
        "name": "Indian Traditional 🪬",
        "prompt": "traditional Indian artwork of {prompt} . intricate patterns, rich colors, cultural elements, folk art style, detailed brushwork",
        "negative_prompt": "modern, abstract, minimalistic, digital",
    },
    {
        "name": "Logo Making 🖊️",
        "prompt": "professional logo design for {prompt} . clean, modern, vector-based, suitable for branding, visually appealing",
        "negative_prompt": "messy, overly complex, low resolution, handwritten",
    },
    {
        "name": "Vector Art 📐",
        "prompt": "vector art of {prompt} . sharp lines, flat colors, scalable design, clean and minimalistic, suitable for printing",
        "negative_prompt": "photographic, raster graphics, blurry, pixelated",
    },
    {
        "name": "NFT Creation 💎",
        "prompt": "NFT art piece of {prompt} . unique, vibrant, engaging, digital collectibles, futuristic, suitable for digital marketplace",
        "negative_prompt": "low quality, generic, traditional art styles, realism",
    },
]

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

# Initialize Google Translator
translator = Translator()


def generate_content_from_image(image, theme):
    if not image:
        return "No image provided for content generation."

    # Prepare the content generation prompt based on theme
    theme_prompts = {
        "None": "Simple",

        "Nature 🌳": """
        🌿 **Celebrate the Beauty of Nature!** 🌼
        
        Write a reflective piece that highlights the wonders of the natural world. Explore themes of harmony, balance, and the interconnectedness of all living things. 
        🍃🌍 Describe the vivid landscapes, the intricate details of flora and fauna, and the emotional impact of nature on your characters. use proper emojis and make it more intresting, immersive and catchy. Craft a narrative of over 500 words that evokes a sense of wonder and appreciation for the Earth!
        """,

        "Sci-Fi 🚀": """
        👽 **Journey into the Future!** 🌌
        
        Imagine a far-off world filled with advanced technology and unknown lifeforms. Your story will unfold with groundbreaking innovations, shocking twists, and a quest that challenges the limits of imagination. 
        🌌💫 Explore strange galaxies and futuristic adventures that leave readers on the edge of their seats! Paint a vivid picture of alien landscapes, mind-bending technologies, and thrilling interstellar battles. use proper emojis and make it more intresting, immersive and catchy. Craft a tale that sparks wonder and curiosity, aiming for more than 500 words!
        """,

        "Abstract 🌀": """
        🎨 **Dive into the Realm of the Abstract!** ✨
        
        Create a narrative that explores complex themes and emotions through a non-linear structure. Utilize vivid imagery, symbolism, and metaphor to express abstract concepts. 
        🌈🔮 Your story can challenge traditional storytelling norms, inviting readers to interpret the meaning in their own way. use proper emojis and make it more intresting, immersive and catchy. Aim for a thought-provoking piece of over 500 words that captivates the imagination!
        """,

        "Fantasy 🧚‍♀️": """
        🏰 **Step into a Magical Realm!** 🦄
        
        Enter a world where magic is real and legends come to life. Write about brave heroes, enchanted creatures, and epic quests. 
        🌳✨ Your story will take readers on a journey through enchanted forests, mystical lands, and ancient prophecies. Will good conquer evil in the ultimate battle of magic? Describe stunning magical spells, mythical beings, and enchanting landscapes. use proper emojis and make it more intresting, immersive and catchy. *Create a captivating narrative with more than 500 words!* 
        """,

        "Adventure 🏔️": """
        🌄 **Embark on an Epic Adventure!** 🏞️
        
        Create an exhilarating story set in wild landscapes and untamed frontiers. Your characters will face thrilling challenges, mysterious discoveries, and a final showdown that tests their courage and resolve. 
        🏇🌌 Let their journey be one of excitement, danger, and triumph! Describe the breathtaking vistas, the pulse of the wild, and the unbreakable bonds forged through trials. Use rich, immersive language and engage the senses. use proper emojis and make it more intresting, immersive and catchy. *Aim for more than 500 words, and make it unforgettable!* 
        """,

        "Mystery 🕵️‍♂️": """
        🧐 **Crack the Code of a Dark Mystery!** 🔍
        
        Start with an eerie scene and dive into a web of secrets and clues. Red herrings, hidden motives, and spine-chilling revelations will lead to a climactic resolution that no one saw coming. 
        🌒🔑 Can your characters solve the mystery before it's too late? Build tension with atmospheric descriptions, intriguing characters, and shocking twists. use proper emojis and make it more intresting, immersive and catchy.  *Weave a compelling story that keeps readers guessing, aiming for over 500 words!* 
        """,

        "Romance 💕": """
        💖 **Feel the Magic of Love Unfold!** 🌹
        
        Create a beautiful and heartwarming story of love, loss, and reconciliation. Build the tension and passion between your characters as they navigate the highs and lows of a romantic journey. 
        🌸💞 Will their love overcome all obstacles to reach a perfect happy ending? Describe the spark of attraction, the sweetness of first kisses, and the heart-wrenching moments of doubt. use proper emojis and make it more intresting, immersive and catchy. *Craft an emotional narrative that resonates deeply, aiming for more than 500 words!* 
        """,

        "Comic Book 🤠": """
        🦸‍♂️ **Unleash Superhero Action!** ⚡
        
        Dive into a thrilling, fast-paced adventure with superpowered heroes and sinister villains. Your comic book-style story should be filled with dramatic battles, heroic moments, and epic plot twists. 
        🌪️🦹‍♀️ Will the forces of good prevail in this action-packed tale? Capture the excitement of high-stakes confrontations, daring rescues, and jaw-dropping abilities. use proper emojis and make it more intresting, immersive and catchy.  *Make it a vibrant, action-filled narrative with over 500 words!* 
        """,

        "Horror 👻": """
        🕷️ **Enter the Abyss of Fear!** 🌑
        
        Craft a chilling tale that grips the reader’s imagination and plunges them into a world of terror. Use suspense, eerie settings, and unsettling characters to create a spine-tingling atmosphere.
        🕯️😱 From haunted houses to dark secrets, describe the moments that make hearts race and skin crawl. use proper emojis and make it more intresting, immersive and catchy.  *Aim for over 500 words that haunt the mind long after reading!* 
        """,

        "Thriller 🎬": """
        ⚡ **Feel the Adrenaline Surge!** 🔥
        
        Write a fast-paced story filled with twists, turns, and unexpected moments that keep readers on the edge of their seats. Develop complex characters who find themselves in perilous situations.
        🚨🕵️‍♀️ As the plot unfolds, layer in suspense and high stakes. use proper emojis and make it more intresting, immersive and catchy. *Create a gripping narrative that delivers thrills and chills, aiming for over 500 words!* 
        """,

        "Historical 📜": """
        🏛️ **Travel Through Time!** ⏳
        
        Set your story in a significant historical period, immersing readers in the sights, sounds, and culture of the time. Create characters who navigate the challenges and triumphs of their era.
        ⚔️📜 From epic battles to everyday life, detail the events and emotions that shaped history. use proper emojis and make it more intresting, immersive and catchy. *Weave a rich tapestry of narrative that exceeds 500 words and enlightens the reader!* 
        """,

        "Superhero 🦸‍♂️": """
        🦸‍♀️ **Rise of the Heroes!** 🌟
        
        Create a thrilling story of extraordinary individuals with unique powers facing formidable villains. Explore the complexities of heroism, sacrifice, and the responsibility that comes with great power. 
        💥⚡ Detail their journeys, the challenges they encounter, and the moral dilemmas they face. use proper emojis and make it more intresting, immersive and catchy. *Craft an inspiring tale that highlights the triumphs and struggles of heroes, aiming for over 500 words!* 
        """,

        "Western 🤠": """
        🐎 **Ride into the Wild West!** 🌵
        
        Set your story in the rugged landscapes of the Wild West, filled with cowboys, outlaws, and lawmen. Explore themes of justice, revenge, and survival against the backdrop of an untamed frontier.
        🌞🔫 Describe the grit, the dust, and the raw emotions of the characters as they navigate a world of danger and adventure. use proper emojis and make it more intresting, immersive and catchy. *Craft a gripping tale of over 500 words that captures the spirit of the West!* 
        """,

        "Mythology 🏺": """
        🌌 **Explore the Legends of Old!** 📖
        
        Dive into the rich tapestry of myth and legend, creating a story that blends ancient tales with modern interpretations. Feature gods, demigods, and mythical creatures in epic quests.
        🌊⚔️ Describe the heroic deeds, moral lessons, and timeless themes found in mythology. use proper emojis and make it more intresting, immersive and catchy. *Create a captivating narrative of over 500 words that brings mythological stories to life!* 
        """,

        "Cyberpunk 🌆": """
        🌐 **Dive into a High-Tech Future!** ⚙️
        
        Set in a dystopian world where advanced technology and societal collapse coexist, your story should explore themes of corporate greed, identity, and rebellion.
        🕶️🚀 Describe neon-lit streets, hackers, and the struggle against oppressive forces. use proper emojis and make it more intresting, immersive and catchy. *Create a thrilling narrative that exceeds 500 words and explores the dark side of innovation!* 
        """,

        "Dystopian 🏙️": """
        🌪️ **Survive in a Broken World!** 🌍
        
        Envision a future where society has crumbled and chaos reigns. Your story should explore themes of survival, resilience, and the human spirit amidst adversity.
        🛡️🔥 Describe the stark realities of a dystopian setting and the characters' struggles against oppressive regimes or catastrophic events. use proper emojis and make it more intresting, immersive and catchy. *Craft a narrative that challenges and inspires, exceeding 500 words!* 
        """,

        "Steampunk ⚙️": """
        🕰️ **Venture into a Steam-Powered World!** 🚂
        
        Set in an alternate Victorian era filled with steam-powered inventions and fantastical machinery, your story should combine adventure with a touch of the whimsical.
        🌪️🛠️ Explore themes of innovation, societal change, and the clash between tradition and progress. use proper emojis and make it more intresting, immersive and catchy. *Create a richly detailed narrative of over 500 words that transports readers to a world where anything is possible!* 
        """,

        "Slice of Life 🌅": """
        🌇 **Capture the Essence of Everyday Life!** ☕
        
        Write a poignant story that focuses on the small moments that make life beautiful and meaningful. Explore characters' relationships, emotions, and experiences in a realistic setting.
        🌻📖 Detail the mundane yet profound aspects of daily life, inviting readers to connect with the universal human experience. use proper emojis and make it more intresting, immersive and catchy. *Aim for a heartfelt narrative of over 500 words that resonates with the reader's own experiences!* 
        """,

        "Magical Realism ✨": """
        🌈 **Blend Reality with the Magical!** 🌌
        
        Weave a narrative where the extraordinary is part of everyday life. Your story should explore themes of identity, culture, and the human experience through a lens of magic and wonder.
        🍃🦋 Create vivid characters and settings that blur the lines between the real and the magical. use proper emojis and make it more intresting, immersive and catchy. *Aim for a beautifully crafted tale of over 500 words that lingers in the imagination!* 
        """,

        "Crime 🕵️": """
        🚔 **Unravel a Gripping Crime Story!** 🔍
        
        Create a narrative centered around a crime, whether it be a heist, murder, or an intricate conspiracy. Explore the minds of both the criminals and those trying to bring them to justice.
        💼📖 Detail the investigation, the motivations, and the consequences of the characters' actions. use proper emojis and make it more intresting, immersive and catchy. *Craft a thrilling story of over 500 words that keeps readers guessing until the very end!* 
        """,

        "Family 👨‍👩‍👦": """
        👪 **Delve into the Dynamics of Family!** ❤️
        
        Write a touching story that explores the bonds, conflicts, and love within a family unit. Highlight the relationships between family members, their struggles, and the lessons learned.
        🌸🏡 Describe the warmth, challenges, and complexities of family life. use proper emojis and make it more intresting, immersive and catchy. *Aim for a heartfelt narrative of over 500 words that reflects the intricacies of familial love and connection!* 
        """,

        "Drama 🎭": """
        🎬 **Create a Compelling Dramatic Narrative!** 🌟
        
        Focus on intense emotions and conflict between characters, exploring themes of love, betrayal, and redemption. Your story should draw readers into the lives of your characters and their struggles.
        🎤💔 Build tension through dialogue, actions, and the characters' inner thoughts. use proper emojis and make it more intresting, immersive and catchy. *Craft a powerful drama of over 500 words that resonates with the reader’s emotions!* 
        """,

        "Sports ⚽": """
        🏅 **Celebrate the Spirit of Competition!** 🏆
        
        Write an inspiring story centered around sports, capturing the thrill of competition, teamwork, and perseverance. Explore the journey of athletes as they strive for greatness.
        ⚽🏃‍♂️ Describe the challenges they face, the camaraderie of teammates, and the joy of victory or the lessons learned from defeat. use proper emojis and make it more intresting, immersive and catchy. *Aim for an energetic narrative of over 500 words that celebrates the world of sports!* 
        """,

        "Adventure Fantasy 🏕️": """
        ⚔️ **Embark on a Fantastical Adventure!** 🧙‍♂️
        
        Combine elements of fantasy with thrilling adventures. Your characters should embark on a quest filled with danger, mythical creatures, and magical realms.
        🏞️🦄 Describe the challenges they face, the friendships they forge, and the discoveries they make along the way. use proper emojis and make it more intresting, immersive and catchy. *Craft an enchanting narrative of over 500 words that transports readers to a world of adventure!* 
        """,

        "Apocalyptic ☠️": """
        🌍 **Survive in a World Gone Wrong!** 🌪️
        
        Envision a post-apocalyptic landscape where survivors must navigate the challenges of a devastated world. Your story should explore themes of survival, loss, and hope.
        🏚️🔦 Describe the characters' struggles to find food, shelter, and safety while confronting dangers from other survivors or the environment.use proper emojis and make it more intresting, immersive and catchy. *Create a gripping narrative of over 500 words that captures the resilience of the human spirit in dire circumstances!* 
        """
    }


    prompt = theme_prompts.get(theme, theme_prompts["None"])


    # Call Google Gemini API
    try:
        response = get_gemini_response(prompt, image)
        return response
    except Exception as e:
        st.error(f"Content generation failed: {e}")
        return "Content generation failed."

def split_text(text, max_length=500):
    """Splits text into smaller chunks to handle large content."""
    if not text:
        return []  # Return an empty list if text is None or empty
    
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', text)
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) < max_length:
            current_chunk += sentence + "\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + "\n"
    
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks


# Translate content into the desired language using Google Translate
def translate_content(content, target_language):
    """Translates the content into the specified language chunk by chunk."""
    try:
        # Split content into smaller chunks if it's too long
        content_chunks = split_text(content)
        translated_chunks = []
        
        # Translate each chunk separately
        for chunk in content_chunks:
            if not chunk:  # Check for empty chunks
                continue
            translated = translator.translate(chunk, dest=target_language)
            if translated is None or translated.text is None:
                raise ValueError("Received None from translation API")
            translated_chunks.append(translated.text)
        
        # Combine translated chunks back into one string
        translated_content = "\n".join(translated_chunks)
        
        # Store the translated content in the session state under the language
        if 'translated_contents' not in st.session_state:
            st.session_state['translated_contents'] = {}
        return translated_content
    
    except Exception as e:
        st.error(f"Translation failed: {e}")
        return content  # If translation fails, return the original content


# Speech synthesis function
def generate_speech(content, language_code):
    try:
        tts = gTTS(text=content, lang=language_code)
        audio_file = BytesIO()
        tts.write_to_fp(audio_file)
        audio_file.seek(0)
        st.audio(audio_file, format='audio/mp3')
        st.session_state.generated_audio = audio_file
    except Exception as e:
        st.error(f"Speech synthesis failed: {e}")

# Remove special characters and improve formatting
def clean_text(text):
    # Retain only alphabetic characters, numbers, punctuation, and spaces
    clean_text = re.sub(r'[^a-zA-Z0-9.,!?;:()\'\" \n]', '', text)
    return re.sub(r'\s+', ' ', clean_text).strip()

# API configuration
os.environ["GOOGLE_API_KEY"] = gemini_key
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# Hugging Face API configuration
HF_API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-dev"
HF_HEADERS = {"Authorization": huggingface_key}

# Function to query Hugging Face model with parameters
async def query_hf_model_async(prompt, text, theme=None, style=None, size="256x256", width=512, height=512, quality="high", creativity="medium", temperature=1.0, variance=1.0, num_images=1):
    images = []
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(num_images):
            payload = {"inputs": prompt}
            if input_text:
                payload["text"] = text
            if theme:
                payload["theme"] = theme
            if style:
                payload["style"] = style
            if size:
                payload["size"] = size
            if width:
                payload["width"] = width
            if height:
                payload["height"] = height
            if quality:
                payload["quality"] = quality
            if creativity:
                payload["creativity"] = creativity
            payload["temperature"] = temperature + (0.05 * _)  # Apply slight variation
            payload["variance"] = variance + (0.05 * _)  # Apply slight variation
            payload["seed"] = str(uuid.uuid4())  # Ensure unique seed for different images

            task = asyncio.create_task(fetch_image(session, payload))
            tasks.append(task)

        results = await asyncio.gather(*tasks)
        for img_bytes in results:
            if img_bytes:
                images.append(img_bytes)
            await asyncio.sleep(1)  # Adjust delay as needed
    return images

# Helper function to fetch image
async def fetch_image(session, payload):
    try:
        async with session.post(HF_API_URL, headers=HF_HEADERS, json=payload) as response:
            response.raise_for_status()
            return await response.read()
    except aiohttp.ClientError as e:
        st.error(f"API request failed: {e}")
        return None

# Helper function to get the style prompt and negative prompt based on the selected style
def get_style_prompts(style_name):
    for style in style_list:
        if style['name'] == style_name:
            return style['prompt'], style['negative_prompt']
    return "{prompt}", ""  # Default no style


def get_gemini_response(input_text, image=None):
    model = genai.GenerativeModel('gemini-1.5-flash')
    if image is not None:
        response = model.generate_content([input_text, image])
    else:
        response = model.generate_content(input_text)
    return response.text

# Function to generate and store audio in session state
def generate_and_store_audio(content):
    clean_response = clean_text(content)
    tts = gTTS(clean_response)
    audio_file = BytesIO()
    tts.write_to_fp(audio_file)
    audio_file.seek(0)  # Reset file pointer to the beginning
    st.session_state.generated_audio = audio_file

# Initialize session state for images and project info
if "generated_images" not in st.session_state:
    st.session_state.generated_images = []
if "full_screen_mode" not in st.session_state:
    st.session_state.full_screen_mode = False
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = ""
if 'generated_audio' not in st.session_state:
    st.session_state.generated_audio = None
if "show_info" not in st.session_state:
    st.session_state.show_info = True  # Start with project info
if 'translated_content' not in st.session_state:
    st.session_state['translated_contents'] = {}
if "translate_text" not in st.session_state:
    st.session_state['translated_text'] = True


# Functions to handle main app and project info
def show_main_app():
    st.session_state.show_info = False
    st.rerun()

def show_project_info():
    st.session_state.show_info = True
    st.rerun()

# Function to run asyncio event loop within Streamlit app
def run_async_function(async_func, *args, **kwargs):
    if callable(async_func):  # Ensure async_func is a function
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(async_func(*args, **kwargs))
    else:
        raise TypeError(f"{async_func} is not a function or coroutine. Check for conflicts in your variable names.")

# Project Information Section
if st.session_state.show_info:
    st.markdown("""
    ## 🚀 OxImaGen: Comprehensive Image Generation & Analysis 🌟
    ---------

    ***🏗️ Architecture 🏛️***
                
    OxImaGen integrates cutting-edge technologies to provide a comprehensive image generation and analysis solution. 🛠️ The architecture includes:
    - **Frontend:** Developed using Streamlit for a responsive and interactive user interface. 🌐
    - **Backend:** Utilizes Hugging Face and Google Gemini APIs for image generation and content analysis. 🔍
    - **Data Handling:** Efficiently manages image inputs and outputs through robust data pipelines. 📊

    ***🛠️ API Calling 📡***
                
    OxImaGen leverages the following APIs for various functionalities:
    1. **Hugging Face API:** Handles image generation with customizable parameters like style, resolution, and content. 🎨
    - **Endpoint:** `/generate-image` 🖼️
    - **Parameters:** `prompt`, `style`, `resolution` 📝
    2. **Google Gemini API:** Provides advanced content generation and analysis. 📈
    - **Endpoint:** `/analyze-image` 🖼️
    - **Parameters:** `image_url`, `analysis_type` 🔎

    ***⚙️ Function Calling 🔧***
                
    The core functions of OxImaGen include:
    - **`query_hf_model(prompt, style, resolution)`**: Communicates with the Hugging Face API to generate images based on user-defined prompts and styles. 📩
    - **`get_gemini_response(image_url, analysis_type)`**: Interacts with Google Gemini API to provide insights and analysis on the uploaded images. 📊
    - **`generate_story_from_image(image)`**: Generates a story based on the uploaded image using natural language processing techniques. 📝
    - **`generate_image_from_story(story)`**: Generates an image based on the provided story using computer vision techniques. 🖼️

    ***🔍 Inference Calling 🔬***
                
    Inference in OxImaGen involves:
    1. **Image Generation:** Users provide a text prompt and optional parameters. The `query_hf_model` function sends these details to the Hugging Face API, which generates and returns an image. 🖼️
    2. **Image Analysis:** Once an image is generated or uploaded, the `get_gemini_response` function sends the image URL to the Google Gemini API for analysis, returning insights or detailed reports based on the analysis type specified. 🔍
    3. **Story Generation:** Users can upload an image, and the `generate_story_from_image` function generates a story based on the image. 📝
    4. **Image Generation from Story:** Users can provide a story, and the `generate_image_from_story` function generates an image based on the story. 🖼️

    ***📚 Use Cases 🛠️***
                
    OxImaGen provides several practical use cases, including:
    1. **Image Generation:** Create images from textual descriptions with various themes, styles, and resolutions to suit different needs. 🎨
    2. **Image Analysis:** Analyze uploaded images to gain insights, detect patterns, or retrieve content-specific information. 🔎
    3. **Interactive UI:** Engage users with a friendly and intuitive interface for generating, viewing, and downloading images. Explore project details and functionalities effortlessly. 🖥️
    4. **Story Generation:** Generate stories based on uploaded images, and vice versa. 📝

    ***🛠️ Frameworks Used 🧰***
                
    OxImaGen is built using a blend of powerful frameworks and technologies:
    - **Streamlit:** Enables the creation of an interactive and user-friendly web app interface. 💻
    - **Hugging Face:** Utilized for its FLUX.1-dev model to generate high-quality images from text prompts. 🖼️
    - **Google Gemini:** Provides advanced capabilities for content generation and image analysis, enhancing the overall functionality of the app. 🔍
    - **Natural Language Processing (NLP) Libraries:** Used for story generation and analysis. 📝
    - **Computer Vision Libraries:** Used for image analysis and generation. 🖼️

    ***🔄 Full Workflow 🔄***
                
    Here's a step-by-step breakdown of the image generation workflow in OxImaGen:
    1. **User Input:** The user provides a text prompt and optional parameters (style, resolution) through the app interface. 📝
    2. **Image Generation Request:** The `query_hf_model` function sends these inputs to the Hugging Face API. 📩
    3. **Image Generation:** The Hugging Face API processes the request and generates an image based on the provided prompt and parameters. 🖼️
    4. **Image Retrieval:** The generated image is retrieved and displayed to the user. 👀
    5. **Image Analysis Request:** If the user opts for analysis, the `get_gemini_response` function sends the image URL to the Google Gemini API. 🌐
    6. **Analysis Results:** The Google Gemini API processes the image and returns insights or reports based on the specified analysis type. 📈
    7. **Display Results:** The analysis results are presented to the user through the app interface. 📊

    ***🔥 Key Features 🔥***
                
    - **Image Generation:** Generate high-quality images from text prompts with customizable styles and resolutions.
    - **Image Analysis:** Analyze uploaded images to gain insights, detect patterns, or retrieve content-specific information.
    - **Interactive UI:** Engage users with a friendly and intuitive interface for generating, viewing, and downloading images.
    - **Advanced APIs:** Leverage the power of Hugging Face and Google Gemini APIs for image generation and analysis.
    - **Robust Data Handling:** Efficiently manage image inputs and outputs through robust data pipelines.
    - **Story Generation:** Generate stories based on uploaded images, and vice versa.

                
    click the button below: 🎨
    """)
    if st.button("🎨 Click me"):
        show_main_app()

else:
    # Main App content (Once the user navigates from the info section)
    st.header('🎨 Oxsecure ImaGen 🎨 / FLUX-Dev ♨️')
    st.markdown("***Image & Story Generation Section 🖼️***")

    # Text input for prompt
    input_text = st.text_input("🖋️ Input Prompt For Image Generation & Analysis", key="input_image_gen")

    # Layout for parameters
    col1, col2 = st.columns(2)

    with col1:
        theme = st.selectbox("🎭 Select Theme:", ["None", "Nature 🌳", "Sci-Fi 🚀", "Abstract 🌀", "Fantasy 🧚‍♀️", "Spectular 👓"], key="theme")
        style_name = st.selectbox("🖼️ Select Art Style:", [style['name'] for style in style_list], key="style")
        creativity = st.selectbox("🎨 Select Creativity Level:", ["low", "medium", "high"], key="creativity")

    with col2:
        
        quality = st.selectbox("⭐ Select Quality:", ["low", "medium", "high"], key="quality")
        num_images = st.selectbox("📸 Number of Images to Generate:", options=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10], key="num_images")
        size = st.selectbox("📏 Select Image Size:", ["256x256", "512x512", "1024x1024"], key="size")


    # Advanced Parameters Section
    with st.expander("⚙️ Advanced Parameters"):
        col3, col4 = st.columns(2)
        with col3:
            temperature = st.slider(
                "🌡️ Temperature:",
                min_value=0.0,
                max_value=2.0,
                step=0.1,
                value=1.0,
                key="temperature"
            )

            variance = st.slider(
                "📊 Variance:",
                min_value=0.0,
                max_value=2.0,
                step=0.1,
                value=1.0,
                key="variance"
            )


        with col4:
            width = st.slider("📏 Adjust Image Width:", min_value=100, max_value=2048, value=512, step=64)
            height = st.slider("📏 Adjust Image Height:", min_value=100, max_value=2048, value=512, step=64)
            size = f"{width}x{height}"

    story_theme = [
        "None",
        "Nature 🌳",
        "Sci-Fi 🚀",
        "Abstract 🌀",
        "Fantasy 🧚‍♀️",
        "Adventure 🏔️",
        "Mystery 🕵️‍♂️",
        "Romance 💕",
        "Comic Book 🤠",
        "Horror 👻",
        "Thriller 🎬",
        "Historical 📜",
        "Superhero 🦸‍♂️",
        "Western 🤠",
        "Mythology 🏺",
        "Cyberpunk 🌆",
        "Dystopian 🏙️",
        "Steampunk ⚙️",
        "Slice of Life 🌅",
        "Magical Realism ✨",
        "Crime 🕵️",
        "Family 👨‍👩‍👦",
        "Drama 🎭",
        "Sports ⚽",
        "Adventure Fantasy 🏕️",
        "Apocalyptic ☠️",
    ]

    # Button to generate images from a prompt
    story_theme = st.selectbox("📚 Choose Story Theme:", story_theme, key="story_theme")
    st.divider()
    col1, col2 , col3 = st.columns(3)  # Create two columns

    with col1:
        submit_generate = st.button("🎨 Generate Images and Story")

    with col2:
        if st.button("🪟 Full-Screen Images"):
            st.session_state.full_screen_mode = not st.session_state.full_screen_mode
    
    with col3:
        if st.button("🔄 clear Audio "):
            st.session_state.generated_audio = None
            st.session_state.story_regenerated = True

    st.divider()

    # Display images based on the toggle state
    if st.session_state.full_screen_mode:
        for i, img in enumerate(st.session_state.generated_images):
            st.image(img, caption=f"Full-View {i+1}", use_column_width=True)

    if submit_generate and input_text:
        progress_bar = st.progress(0)  # Initialize the progress bar
        with st.spinner('⏳ Generating images... Please wait...'):
            style_prompt, negative_prompt = get_style_prompts(style_name)
            final_prompt = style_prompt.format(prompt=input_text)

            images_bytes = run_async_function(
                query_hf_model_async,
                final_prompt,
                input_text,
                theme if theme != "None" else None,
                style_name if style_name != "(No style)" else None,
                size,
                width,
                height,
                quality,
                creativity,
                temperature,
                variance,
                num_images
            )

            
            # Simulate the progress percentage over time (Example: 10% increase each second)
            for i in range(1, 11):
                time.sleep(0.5)  # Simulate loading time
                progress_bar.progress(i * 10)  # Update progress bar
                if images_bytes:
                    st.session_state.generated_images = [] 
                    for i, img_bytes in enumerate(images_bytes):
                        try:
                            img = Image.open(io.BytesIO(img_bytes))
                            st.session_state.generated_images.append(img)
                        except Exception as e:
                            st.error(f"Error processing image: {e}")

        if st.session_state.generated_images:
            if len(st.session_state.generated_images) > 0:
                selected_image = random.choice(st.session_state.generated_images)  # Choose one image randomly
                if 'story_theme' in locals() or 'story_theme' in globals():
                    content = generate_content_from_image(selected_image, story_theme)  # Generate content from the chosen image
                    st.session_state.generated_content = content
                    # Display the generated content
                    st.markdown(f"***📜 Generated Story***")
                    st.markdown(st.session_state.generated_content)
                    if st.session_state.generated_audio is None:
                        generate_and_store_audio(content)
                    if st.session_state.generated_audio is not None:
                        st.session_state.generated_audio.seek(0)
                    st.audio(st.session_state.generated_audio, format='audio/mp3')
                else:
                    st.error("story_theme is not defined")
            else:
                st.error("No images to choose from")
        else:
            st.error("No generated images")


    # Organize thumbnails in responsive columns
    if st.session_state.generated_images:
        cols = st.columns(min(num_images, 10))  # Show in max 10 columns or fewer based on number of images
        for idx, img in enumerate(st.session_state.generated_images[:len(cols)]):
            with cols[idx]:
                st.image(img, caption=f"🪄 Img {idx+1}", use_column_width=True)

                # Provide download link with a unique key for each button
                buf = io.BytesIO()
                img.save(buf, format="PNG")
                buf.seek(0)
                st.download_button(
                    label=f"📥",
                    data=buf,
                    file_name=f"OxImaGen_{idx+1}.png",
                    mime="image/png",
                    key=f"download_button_{idx}"  # Unique key for each button
                )

        if st.session_state.generated_content:
            with st.expander("Generated Content ✏️"):
                st.markdown(f"***📜 Generated Story***")
                st.markdown(st.session_state.generated_content)
                st.markdown(st.session_state.translated_contents)
                if st.session_state.generated_audio is not None:
                    st.session_state.generated_audio.seek(0)
                    st.audio(st.session_state.generated_audio, format='audio/mp3')
                
        for lang, translated_text in st.session_state['translated_contents'].items():
            if translated_text:
                with st.expander(f"Translated Content ({lang})"):
                    st.markdown(translated_text)

            else:
                st.error("Audio generation failed.")

    # Generate content and translate when button is clicked
    selected_language = st.selectbox("Select Language", list(languages.keys()))
    if st.button("Translate 🎙️"):
        language_code = languages[selected_language] if selected_language in languages else 'en'

        if 'generated_content' in st.session_state:
            english_content = st.session_state.generated_content

            if language_code != 'en':
                st.info(f"Translating content into {selected_language}...")
                translated_content = translate_content(english_content, language_code)
                st.markdown(f"### Translated Content ({selected_language})")
                
                # Show translated content inside an expander
                with st.expander(f"Translated Content ({selected_language})"):
                    st.markdown(translated_content)

                # Generate speech from the translated content
                generate_speech(translated_content, language_code)
                
                # # Show the translated audio
                # if st.session_state.generated_audio:
                #     st.audio(st.session_state.generated_audio, format='audio/mp3')
        else:
            st.error("No content available in session. Please generate content first.")

    # File uploader for image
    st.markdown("***File Upload Section 📤***")
    st.divider()
    uploaded_file = st.file_uploader("📂 Choose an image...", type=["jpg", "jpeg", "png", "webp", "gif", "bmp", "tiff", "ico", "heif", "jfif", "svg", "exif", "psd", "raw"])
    image = None
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", width=250, use_column_width=False)
        st.markdown("-----")

    # Button to get response about the image
    submit_analyze = st.button("🔍 Tell me about the image")
    if submit_analyze:
        if input_text and image is not None:
            response = get_gemini_response(input_text, image)
            st.markdown("***📝 Result***")
            st.write(response)
        elif image is not None:
            content = generate_content_from_image(image, story_theme)
            st.markdown(f"***📜 Generated Content for Uploded Image***")
            st.markdown(content)
        elif image and input_text is None:
            content = generate_content_from_image(image, story_theme)
            st.markdown(f"***📜 Generated Content for Uploded Image***")
            st.markdown(content)     
        elif input_text:
            response = get_gemini_response(input_text)
            st.markdown("***📝 Result***")
            st.write(response)
        else:
            st.write("Please provide an input prompt or upload an image.")
