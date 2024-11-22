import os
import streamlit as st
import google.generativeai as genai
from google.api_core.exceptions import GoogleAPIError
import time


st.set_page_config(page_title="AtmaVeda - Gateway to Wisdom", page_icon="🕉️", layout="wide")

def load_css(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the CSS file
load_css("ui/test.css")


# Set your Google Gemini API Key
os.environ["GOOGLE_API_KEY"] = "AIzaSyC2U-0TEQAHMJPBKIeevjnQzEp6FaxGkTE"
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

# State management for page navigation
if "current_page" not in st.session_state:
    st.session_state.current_page = "landing"

# Query Gemini function
def query_gemini(context, prompt, language="en"):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(context + prompt)
        
        if hasattr(response, 'candidates') and response.candidates:
            answer = ' '.join(part.text for part in response.candidates[0].content.parts)
            # Translate to Hindi if selected
            if language == "hi":
                translated_answer = query_gemini(
                    "Translate this to Hindi:", f"\n\n{answer}"
                )
                return translated_answer or answer
            return answer
        else:
            st.error("Unexpected response format from Gemini API.")
            return None
    except GoogleAPIError as e:
        st.error(f"An error occurred while querying the Gemini API: {e}")
        return None

# Enhanced Knowledge Base
@st.cache_data
def load_knowledge_base():
    return {
        "Vedas": {
            "description": "The Vedas are the foundation of Sanatan Dharma, containing hymns, rituals, and spiritual philosophy. They are divided into four major Vedas: Rig Veda, Yajur Veda, Sama Veda, and Atharva Veda. Each Veda consists of various mandals (books) which contain hymns, prayers, rituals, and philosophical teachings.",
            "examples": [
            {
                "title": "Rig Veda",
                "content": "The oldest Veda, focusing on hymns dedicated to cosmic powers and natural elements. It includes the famous Gayatri Mantra.",
                "mandals": [
                {"mandal": 1, "description": "Hymns dedicated to Agni, Indra, and other deities."},
                {"mandal": 2, "description": "Prayers to the deities of the sky, including the sun and moon."},
                {"mandal": 3, "description": "Hymns dedicated to the gods of nature and cosmic order."},
                {"mandal": 4, "description": "Hymns to Indra and other deities in the form of praise and worship."},
                {"mandal": 5, "description": "Hymns focusing on the philosophical aspects of the Vedic rituals."},
                {"mandal": 6, "description": "Chants related to the fire ritual (Agni) and the importance of the elements."},
                {"mandal": 7, "description": "Further hymns on philosophical ideas and cosmology."},
                {"mandal": 8, "description": "Hymns on cosmic creation and the metaphysical concepts."},
                {"mandal": 9, "description": "The famous Gayatri Mantra and philosophical reflections on the universe."},
                {"mandal": 10, "description": "Hymns on the nature of existence and the transcendental elements of reality."}
                ]
            },
            {
                "title": "Yajur Veda",
                "content": "A guide for rituals and sacrifices, blending prose and verse. It provides instructions on sacrificial rituals.",
                "mandals": [
                {"mandal": 1, "description": "Instructions for the performance of rituals and sacrifices."},
                {"mandal": 2, "description": "Detailed prayers for the proper execution of yajnas (sacrificial offerings)."}
                ]
            },
            {
                "title": "Sama Veda",
                "content": "Melodies and chants for devotional practices and meditation. It is considered the 'Veda of Chants.'",
                "mandals": [
                {"mandal": 1, "description": "Chants dedicated to various gods, especially the chanting of Soma hymns."},
                {"mandal": 2, "description": "Prayers for health, prosperity, and spiritual elevation."},
                {"mandal": 3, "description": "Chants for meditation and the invocation of cosmic forces."}
                ]
            },
            {
                "title": "Atharva Veda",
                "content": "Prayers and incantations addressing everyday concerns, such as healing, protection, and well-being.",
                "mandals": [
                {"mandal": 1, "description": "Hymns focused on healing, health, and protection from disease."},
                {"mandal": 2, "description": "Magical incantations for securing prosperity and protection."},
                {"mandal": 3, "description": "Prayers for personal and community well-being, including marriage and fertility."},
                {"mandal": 4, "description": "Incantations for protection from evil spirits and negative forces."},
                {"mandal": 5, "description": "Hymns related to the blessings of wealth, peace, and prosperity."}
                ]
            }
            ]
        },
        "Upanishads": {
            "description": "The Upanishads discuss metaphysical truths and the unity of Atman (soul) and Brahman (universal consciousness). They form the philosophical core of Hinduism.",
            "examples": [
                {"title": "Isa Upanishad", "content": "Explains the interconnectedness of the self with the universe and teaches the realization of the divine in everything."},
                {"title": "Katha Upanishad", "content": "A conversation between Nachiketa and Yama (the god of death), discussing immortality, the nature of the soul, and the path to liberation."},
                {"title": "Mundaka Upanishad", "content": "Teaches the difference between the higher knowledge (Brahman) and lower knowledge (material sciences)." },
                {"title": "Taittiriya Upanishad", "content": "Describes the layers of human existence (koshas) and emphasizes the ultimate goal of self-realization."},
            ],
        },
        "Puranas": {
            "description": "The Puranas are a genre of ancient Hindu texts that elaborate on the creation of the universe, cosmology, and various gods and their stories.",
            "examples": [
                {"title": "Vishnu Purana", "content": "Describes the creation of the world, the avatars of Lord Vishnu, and the stories of various kings and sages."},
                {"title": "Shiva Purana", "content": "Narrates the stories of Lord Shiva's birth, his family, and his teachings on the nature of reality."},
                {"title": "Bhagavata Purana", "content": "Contains the story of Lord Krishna, his childhood exploits, and the philosophical teachings he imparted to his devotees."},
                {"title": "Markandeya Purana", "content": "Describes the legend of Markandeya and the cosmic destruction and rebirth of the universe."},
                {"title": "Garuda Purana", "content": "Deals with the creation of the universe, the cosmology of the divine, and the details of death, reincarnation, and moksha."},
            ],
        },
        "Bhagavad Gita": {
            "description": "The Bhagavad Gita is a 700-verse scripture, part of the Indian epic Mahabharata. It presents a conversation between Prince Arjuna and Lord Krishna on the battlefield of Kurukshetra.",
            "examples": [
                {"title": "Chapter 1: Arjuna Vishada Yoga", "content": "Arjuna's despair on the battlefield and his refusal to fight, leading to his dialogue with Lord Krishna."},
                {"title": "Chapter 2: Sankhya Yoga", "content": "Lord Krishna imparts the philosophy of selflessness, the immortality of the soul, and the path of karma."},
                {"title": "Chapter 3: Karma Yoga", "content": "The yoga of selfless action, focusing on performing one's duty without attachment to the results."},
                {"title": "Chapter 4: Jnana Karma Sanyasa Yoga", "content": "The yoga of knowledge and action, emphasizing the importance of divine wisdom in one’s actions."},
                {"title": "Chapter 5: Karma Sanyasa Yoga", "content": "The yoga of renunciation, discussing the importance of renouncing desires while still engaging in the world."},
                {"title": "Chapter 6: Dhyana Yoga", "content": "The yoga of meditation, describing the practice of focusing the mind on the divine."},
                {"title": "Chapter 7: Jnana Vijnana Yoga", "content": "The yoga of knowledge and wisdom, discussing the supreme nature of the divine."},
                {"title": "Chapter 8: Aksara Brahma Yoga", "content": "Describes the ultimate, imperishable nature of the soul and the path to liberation."},
                {"title": "Chapter 9: Raja Vidya Raja Guhya Yoga", "content": "The yoga of royal knowledge and royal secret, where Krishna reveals his divine form and teaches devotion."},
                {"title": "Chapter 10: Vibhuti Yoga", "content": "The yoga of divine glories, where Krishna reveals the many divine manifestations of the supreme."},
                {"title": "Chapter 11: Visvarupa Darshana Yoga", "content": "Krishna shows Arjuna his universal form, revealing the vastness of his divine nature."},
                {"title": "Chapter 12: Bhakti Yoga", "content": "The yoga of devotion, explaining the importance of devotion to God in achieving liberation."},
                {"title": "Chapter 13: Kshetra Kshetragna Vibhaga Yoga", "content": "Describes the distinction between the physical body (kshetra) and the soul (kshetragna)." },
                {"title": "Chapter 14: Gunatraya Vibhaga Yoga", "content": "Explains the three gunas (qualities) of nature: sattva, rajas, and tamas."},
                {"title": "Chapter 15: Purushottama Yoga", "content": "Describes the nature of the eternal soul and the supreme being (Purushottama)."},
                {"title": "Chapter 16: Daivasura Sampad Vibhaga Yoga", "content": "The division between the divine and demoniacal qualities in human beings."},
                {"title": "Chapter 17: Sraddhatraya Vibhaga Yoga", "content": "Describes the three types of faith based on the gunas (sattva, rajas, tamas)."},
                {"title": "Chapter 18: Moksha Sanyasa Yoga", "content": "The final chapter summarizing the teachings of the Gita, focusing on renunciation, surrender, and liberation."},
            ],
        },
         "Mythology & Divine Powers": {
            "description": "Hindu mythology is rich with divine tales, cosmic forces, and celestial beings, embodying spiritual and ethical principles.",
            "examples": [
                {"title": "Shiva", "content": "The destroyer and transformer."},
                {"title": "Lakshmi", "content": "The goddess of wealth and prosperity."},
                {"title": "Krishna Leela", "content": "Divine play of Lord Krishna."},
            ],
         },
        "Spritual Places": {
            "description": "Learn about the significance of sacred places in Hinduism, where spiritual practices are believed to attain higher levels of consciousness.",
            "examples": [
                {"title": "Varanasi", "content": "A sacred city believed to liberate souls from the cycle of rebirth. Known for its ghats on the banks of the Ganges."},
                {"title": "Rameshwaram", "content": "A pilgrimage site connected to the story of Lord Rama. It is one of the Char Dham (four sacred pilgrimage sites)."},
                {"title": "Tirupati", "content": "Famous for the Sri Venkateswara Temple, where devotees visit to seek blessings from Lord Vishnu."},
                {"title": "Haridwar", "content": "A holy city on the banks of the Ganges, considered one of the seven holiest places in Hinduism."},
                {"title": "Dwarka", "content": "The ancient city associated with Lord Krishna, located in Gujarat. It is one of the Char Dham pilgrimage sites."},
                {"title": "Kedarnath", "content": "Famous for the Kedarnath Temple, dedicated to Lord Shiva, located in the Himalayan mountains."},
                {"title": "Amarnath", "content": "A sacred cave shrine dedicated to Lord Shiva, known for the naturally occurring ice Shiva Lingam."},
                {"title": "Badarinath", "content": "Part of the Char Dham, this temple is dedicated to Lord Vishnu and located in the Himalayas."},
                {"title": "Somnath", "content": "The Somnath Temple in Gujarat, known for its historical significance and as one of the twelve Jyotirlinga temples of Lord Shiva."},
            ],
        },
        "Sanatan Dharma": {
            "description": "Sanatan Dharma, also known as Hinduism, is the eternal and universal way of life. It encompasses rituals, philosophies, and teachings that promote spiritual development and liberation.",
            "examples": [
                {"title": "Dharma", "content": "The righteous path and moral order in life, which includes concepts like karma, dharma, and moksha."},
                {"title": "Karma", "content": "The law of cause and effect. Every action has consequences, and one’s actions determine their future life circumstances."},
                {"title": "Moksha", "content": "The liberation from the cycle of birth and rebirth, the ultimate goal in Hindu philosophy."},
            ],
        },
    }

# Load the expanded knowledge base
knowledge_base = load_knowledge_base()

# Recommendation function (using Gemini to provide suggestions)
def generate_recommendations_based_on_input(user_input, language="en"):
    context = ""
    for category in knowledge_base.values():
        for example in category["examples"]:
            context += example["content"] + "\n"
    
    # Gemini will generate a recommendation based on the content
    prompt = f"Based on the user's interest in the following topics, recommend related spiritual texts, practices, or concepts. Provide at least 5 specific suggestions and article url for user readings  from the same domain:\n\n{user_input}\n\nBased on the content above, what other resources would you suggest?"
    
    recommendation = query_gemini(context, prompt, language)
    if recommendation:
        # Split the recommendations into a list for easier processing
        recommendations = recommendation.split("\n")
        return recommendations  # Return top 5 recommendations
    else:
        return ["No recommendations available at the moment."]

# Landing Page
if st.session_state.current_page == "landing":
    # Title of the app
    st.title("🕉️ AtmaVeda")

    # Animated Caption
    caption_placeholder = st.empty()
    caption_text = "Gateway to Eternal Wisdom 🙇🏻"

    for i in range(len(caption_text) + 1):
        caption_placeholder.subheader(caption_text[:i])
        time.sleep(0.05)  # Simulates typing effect

    # Catchy Introduction
    st.markdown("""
    Welcome to **AtmaVeda**, your **spiritual companion** for exploring the profound wisdom of Sanatan Dharma.  
    Uncover insights from sacred texts, timeless philosophies, and divine teachings — all powered by advanced AI, 
    offering guidance as if from an enlightened Pandit. 🌟  
    """)
    st.markdown("""
    **AtmaVeda** is a digital platform designed to bring the timeless knowledge of Sanatan Dharma into the modern age. 
    Combining AI with ancient wisdom, VedaGPT serves as an accessible resource for spiritual exploration and learning.
    
    **Features**:
    - Explore the Vedas, Upanishads, and other sacred texts.
    - Engage in Q&A with an AI-powered intellectual Pandit.
    - Gain deep insights into Hindu philosophy and spiritual practices.

    Created with a vision to spread the profound teachings of Sanatan Dharma to the world.
    """)

    st.write("🙏 **May the wisdom of the divine guide you.**")

    # Get Started button
    if st.button("Get Started 🧘‍♂️"):
        st.session_state.current_page = "main"  # Navigate to main content
        st.rerun()


# Main Content (Knowledge Base & VedaGPT)
elif st.session_state.current_page == "main":

    # Language selection section
    st.markdown("#### 🌐 Language Preferences")
    language_code = st.radio(
        "Choose your preferred language for responses:",
        options=["English", "Hindi"],
        index=0,
        horizontal=True,
        format_func=lambda lang: "English (Default)" if lang == "English" else "Hindi (हिंदी)",
        label_visibility="collapsed"  # Hides the label
    )

    # Map language selection to a language code
    language_code = "hi" if language_code == "Hindi" else "en"

    # Display a message based on the selected language
    st.info(f"🌟 Responses will be provided in **{'Hindi' if language_code == 'hi' else 'English'}**.")


    # Tabs for navigation
    tab1, tab2 = st.tabs(["📖 Knowledge Base", "🧐 VedaGPT"])

    # Tab 1: Knowledge Base
    with tab1:
        st.header("📖 Explore the Sacred Knowledge")
        
        # Select a knowledge area (e.g., Vedas)
        selected_category = st.selectbox(
            "Choose a knowledge area to explore:",
            list(knowledge_base.keys())
        )
        
        if selected_category:
            st.subheader(f"🔍 About {selected_category}")
            category_info = knowledge_base[selected_category]
            st.write(category_info["description"])
            
            # Select a specific example (e.g., Veda, Mandal)
            selected_example = st.selectbox(
                f"Select a specific {selected_category.lower()} to learn about:",
                [example["title"] for example in category_info["examples"]]
            )
            
            # Check if the selected category is "Vedas" and display mandals
            if selected_category == "Vedas":
                selected_mandal = None
                for example in category_info["examples"]:
                    if selected_example == example["title"]:
                        selected_mandal = st.selectbox(
                            f"Select a Mandal from the {selected_example}",
                            [f"Mandal {mandal['mandal']}: {mandal['description']}" for mandal in example["mandals"]]
                        )
                        break
                    
                # Generate insights for the selected mandal
                if selected_mandal and st.button(f"Generate Insights on {selected_mandal}", key="insights"):
                    with st.spinner("Generating insights..."):
                        progress = st.progress(0)
                        
                        # Simulate processing time for visual feedback
                        for i in range(100):
                            time.sleep(0.02)  # Simulated delay
                            progress.progress(i + 1)

                        context = f"{category_info['description']}\n"
                        mandal_description = selected_mandal.split(":")[1].strip()  # Get mandal description
                        prompt = f"Explain the spiritual and practical wisdom of the Mandal selected: {mandal_description}, focusing on its significance in Sanatan Dharma."
                        response = query_gemini(context, prompt, language_code)
                        
                        if response:
                            st.success(f"### Insights on {selected_mandal}:")
                            st.write(response)

                            # Ask for AI recommendations
                            st.write("### Recommendations Based on Your Interest:")
                            recommendations = generate_recommendations_based_on_input(response, language_code)
                            
                            # Save recommendations to session state
                            if "recommendations" not in st.session_state:
                                st.session_state.recommendations = recommendations
                            else:
                                st.session_state.recommendations = recommendations
                            
                            # Display recommendations in an expander
                            with st.expander("🔍 Expand to see Recommendations"):
                                for rec in st.session_state.recommendations:
                                    st.write(f"- {rec}")
            else:
                if st.button(f"Generate Insights on {selected_example}", key="insights"):
                    with st.spinner("Generating insights..."):
                        progress = st.progress(0)
                        
                        # Simulate processing time for visual feedback
                        for i in range(100):
                            time.sleep(0.02)  # Simulated delay
                            progress.progress(i + 1)

                        context = f"{category_info['description']}\n"
                        prompt = f"Explain the spiritual and practical wisdom of {selected_example} in detail, focusing on its significance in Sanatan Dharma."
                        response = query_gemini(context, prompt, language_code)
                        
                        if response:
                            st.success(f"### Insights on {selected_example}:")
                            st.write(response)

                            # Ask for AI recommendations
                            st.write("### Recommendations Based on Your Interest:")
                            recommendations = generate_recommendations_based_on_input(response, language_code)
                            
                            # Save recommendations to session state
                            if "recommendations" not in st.session_state:
                                st.session_state.recommendations = recommendations
                            else:
                                st.session_state.recommendations = recommendations
                            
                            # Display recommendations in an expander
                            with st.expander("🔍 Expand to see Recommendations"):
                                for rec in st.session_state.recommendations:
                                    st.write(f"- {rec}")


    # Tab 2: VedaGPT Q&A
    with tab2:
        st.title("🛕 VedaGPT")
        st.markdown("""
        **Namaste! 🙏 Welcome to VedaGPT.**  
        I'm here to guide you through the profound knowledge of Sanatan Dharma, including sacred texts like the Vedas, Upanishads, Bhagavad Gita, Puranas, and more.  
        Feel free to ask your questions on spirituality, philosophy, or Hindu traditions, and I’ll provide insights with the wisdom of an enlightened sage. 🌟  
        """)
        
        # User Question Input
        user_question = st.text_input(
            "What would you like to know?",
            placeholder="E.g., What is the significance of meditation in Sanatan Dharma?",
        )

        if st.button("Ask VedaGPT"):
            if user_question.strip():
                with st.spinner("Let me ponder your question..."):
                    # Simulate processing with progress feedback
                    progress = st.progress(0)
                    for i in range(100):
                        time.sleep(0.02)
                        progress.progress(i + 1)

                    # Context for AI Query
                    context = (
                        "You are VedaGPT, an advanced spiritual AI with a profound understanding of Sanatan Dharma, "
                        "including its sacred texts, teachings, and philosophies. Provide articulate, compassionate, and "
                        "contextually rich responses to the user's question, maintaining a tone of wisdom and professionalism."
                    )
                    
                    # Simulate querying the AI model
                    response = query_gemini(context, user_question, language_code)
                    
                    # Display Response
                    if response:
                        st.write("#### 🙏 VedaGPT's Response:")
                        st.markdown(f"> {response}")
                        
                        # Add Follow-up Conversation
                        st.write("💡 *Would you like to ask something else or discuss this further?*")
                        
                        # Recommendations Section
                        st.markdown("### 🔍 Additional Insights & Suggestions")
                        recommendations = generate_recommendations_based_on_input(user_question, language_code)
                        if "recommendations" not in st.session_state:
                            st.session_state.recommendations = recommendations
                        
                        with st.expander("📜 Explore Related Topics and Practices"):
                            for rec in st.session_state.recommendations:
                                st.markdown(f"- **{rec}**")
                        
                    else:
                        st.error("I couldn't provide an answer this time. Could you try rephrasing your question?")
            else:
                st.warning("Please type your question before clicking 'Ask VedaGPT'.")



# Footer Section
st.divider()
with st.container():
    st.markdown("""
        <div style="text-align: center; padding: 20px; color: #555;">
            <p style="font-size: 14px; font-weight: bold;">Developed with Passion and Precision</p>
            <p style="font-size: 12px;">Crafted by Aditya Pandey | Building the Future of AI & Spiritual Wisdom</p>
            <p style="font-size: 10px; color: #777;">Innovating with technology, rooted in tradition.</p>
        </div>
    """, unsafe_allow_html=True)
