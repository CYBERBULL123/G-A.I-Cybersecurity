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
    prompt = f"""
    The user is interested in the following topics: 
    {user_input}
    
    Based on the user's input and the following content from various spiritual and historical knowledge domains:
    
    {context}
    
    Provide detailed recommendations related to spiritual practices, texts, and historical concepts that align with the user's query. 
    Please offer at least 5 specific suggestions for further reading, including titles of texts, practices to explore, key concepts, and URLs to trusted resources for deeper understanding. Each suggestion should be accompanied by a brief explanation of why it is relevant to the user's interests. 

    Suggestions:
    """
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
    🌟 **Welcome to AtmaVeda** — Your gateway to the divine wisdom of **Sanatan Dharma** and the glorious legacy of **Indian history**!  
    Dive into the spiritual teachings of the **Vedas**, explore ancient philosophies, and uncover the stories of India’s rich past — all with the power of AI, guiding you like an enlightened Pandit. 🙏  
    """)

    st.markdown("""
    ### 🔮 **What is AtmaVeda?**
    AtmaVeda is a revolutionary platform that bridges the timeless knowledge of **Sanatan Dharma** with the advancements of modern technology.  
    With **VedaGPT** and **VedaBase**, embark on a journey to explore spirituality and history like never before! 🌼

    ### ✨ **Key Features**:

    1. **📚 VedaGPT**:  
    - 🤔 **Ask any question** and get insightful answers about Hindu philosophy, sacred texts, and spiritual practices.  
    - 🕉️ Learn about **Indian mythology**, rituals, and the essence of the **Upanishads** and **Bhagavad Gita**.  
    - 🔍 Get personalized spiritual guidance like an intellectual Pandit by your side.  

    2. **📖 VedaBase**:  
    - 🔥 Explore the **Vedas**, **Puranas**, and other sacred scriptures with ease.  
    - 🗺️ Discover detailed timelines and events from Indian history.  
    - 🕌 Learn about **spiritual landmarks** and their cultural significance.  

    3. **🌏 Indian History Explorer**:  
    - ⏳ Trace the **journey of Indian civilization**, from the **Vedic Age** to **Modern India**.  
    - 🛕 Learn about empires, cultural transformations, and spiritual movements.  
    - ✍️ Uncover the stories of how spirituality shaped India’s history and identity.  

    ---

    🎯 **Why AtmaVeda?**  
    AtmaVeda was created with a vision to bring the **profound teachings of Sanatan Dharma** and the **rich cultural heritage of India** to the modern world.  
    Whether you're a spiritual seeker, history enthusiast, or just curious, AtmaVeda has something for everyone. 🌺  

    ---

    🌸 **Let the divine wisdom and historical legacy inspire your journey!** 🙏
    """)
    
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
    tab1, tab2, tab3 = st.tabs(["📖 VedBase", "🧐 VedaGPT", "Indian History 🔱"])

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

    # Tab 3: Ancient Indian History
    with tab3:
        st.title("📜 **Explore the Glory of Ancient India** 🌟")
        st.markdown("""
            **✨ Welcome to the Knowledge Base of India's Rich Heritage!**  
            - 🌸 Embark on a journey through India's glorious past, from the **Vedic Period** to the **Modern Era**.  
            - 🕉️ Discover the spiritual milestones, cultural achievements, and historical events that shaped the soul of India.  
            - 📚 Explore a treasure trove of wisdom, from the sacred texts to the revolutionary movements that continue to inspire the world.  
            - 🌏 **Uncover the wisdom of Ancient India** and delve into its timeless knowledge, philosophy, and history.  
                    
            🚀 **Dive in to explore the profound legacy of India's ancient civilizations!**
        """)


       # Create sections for different eras
        st.subheader("📖 Select a Historical Era to Explore:")
        with st.expander("🕰️ Expand to choose an Era::", expanded=True):  # Provide a label for the expander
            era = st.radio(
                "🌟 Choose an Era:",
                options=[
                    "🕉️ Vedic Period (1500 BCE - 500 BCE)",
                    "🏛️ Mahajanapadas (600 BCE - 321 BCE)",
                    "🦁 Maurya Empire (321 BCE - 185 BCE)",
                    "🛡️ Gupta Empire (320 CE - 550 CE)",
                    "🏰 Medieval India (750 CE - 1200 CE)",
                    "👑 Mughal Empire (1526 CE - 1857 CE)",
                    "🌍 Colonial Period (1757 CE - 1947 CE)",
                    "🚀 Modern India (1947 CE - Present)"
                ],
                index=0
            )


        # Dynamic content based on the selected era
        st.write("### 📜 **Details of the Selected Era:**")
        if era == "🕉️ Vedic Period (1500 BCE - 500 BCE)":
            st.markdown("""
            ### 📜 **The Vedic Period (1500 BCE - 500 BCE)**  
            The **Vedic Period** marks the foundation of Indian civilization, with the composition of the four **Vedas** ***Rigveda***, ***Samaveda***, ***Yajurveda***, and ***Atharvaveda*** which laid the spiritual and philosophical foundations of India.

            ---
            ### 🔑 **Key Highlights**
            - **Emergence of the Caste System (Varna System)**:
                - A social structure based on division of labor that divided society into four primary varnas:
                - **Brahmins** (priests and scholars),
                - **Kshatriyas** (warriors and rulers),
                - **Vaishyas** (merchants and agriculturists),
                - **Shudras** (laborers and service providers).
            - **Rituals and Spiritual Knowledge**:
                - The composition of the **Vedas** formed the basis for Vedic religion, with sacred rituals (**yajnas**) and sacrifices central to religious practices.
            - **Development of Sanskrit**:
                - The Vedas were composed in **Sanskrit**, which became the sacred and literary language, setting the foundation for classical Indian literature.
            
            ---
            ### 🧘 **Philosophical Foundations**
            - **Dharma** (duty), **Karma** (action and its consequences), and **Moksha** (liberation) were central to Vedic philosophy.
            - The **Brahmanas** provided detailed explanations of the rituals and sacrifices to be performed by priests.
            - **Aranyakas** were texts that explored spiritual ideas related to asceticism and meditative practices in the forest, often linked to deeper philosophical insights.
            - The **Upanishads**, composed towards the end of the Vedic period, marked a shift towards more metaphysical questions, focusing on the nature of **Brahman** (the universal soul) and **Atman** (the individual soul), leading to the development of **Vedanta philosophy**.

            ---
            ### 🌿 **Society and Economy**
            - **Shift from Nomadic to Settled Life**: The Vedic people initially practiced nomadic pastoralism, but over time, they transitioned to settled agrarian communities.
            - **Agricultural Advancements**: The later Vedic period saw the introduction of **iron tools** that revolutionized agriculture and facilitated the expansion of settlements and trade.

            ---
            ### 🎶 **Cultural Developments**
            - **Indian Music and Dance**: This period laid the foundation for Indian music, dance, and oral traditions, which were intricately tied to religious rituals and celebrations.
            - **Worship of Nature Gods**:
                - The Vedic people worshipped **nature gods** like **Indra** (god of thunder and war), **Agni** (fire god), **Varuna** (god of cosmic order), and **Surya** (sun god), often invoking their blessings through elaborate yajnas (sacrificial offerings).

            ---
            ### 🌸 **Legacy of the Vedic Period**
            - The **Vedic Period** established the foundations of Hindu philosophy, religion, and social structures that would influence India for millennia.
            - The **Vedas** continue to be the most revered texts in Hinduism, and the **Upanishads** mark the intellectual transition towards deeper spiritual contemplation.
            - The cultural, philosophical, and religious developments during this time set the stage for the rise of later spiritual and intellectual traditions, including the **Mahabharata**, **Ramayana**, and the teachings of **Buddhism** and **Jainism**.

            The Vedic Period remains a cornerstone in the cultural and spiritual history of India, with lasting impacts on philosophy, social structure, and religious practices. 📜
            """)


        elif era == "🏛️ Mahajanapadas (600 BCE - 321 BCE)":
            st.markdown("""
            ### 🏛️ **The Mahajanapadas Period (600 BCE - 321 BCE)**  
            The **Mahajanapadas Period** marks a significant transition in Indian history from tribal societies to more structured state-based governance, with the emergence of 16 powerful kingdoms and republics. This era also saw the rise of new philosophical and religious movements, such as **Buddhism** and **Jainism**, that challenged the existing social and religious systems.

            ---
            ### 🏰 **Key Mahajanapadas and Rise of Kingdoms**
            The Mahajanapadas were 16 powerful kingdoms and republics, each playing a pivotal role in the political and cultural landscape of ancient India.

            | **Mahajanapada**          | **Capital**             | **Significance**                                       | **Key Figures**                    |
            |---------------------------|-------------------------|--------------------------------------------------------|-------------------------------------|
            | **Magadha**                | Rajgir, Pataliputra     | One of the most powerful, eventually founded the **Maurya Empire**. | **Bimbisara**, **Ajatashatru**     |
            | **Kosala**                 | Ayodhya                 | Birthplace of **Lord Rama**, significant in early Vedic and epic traditions. | **King Dasharatha**, **Rama**      |
            | **Vatsa**                  | Kausambi                | Prominent kingdom known for its strategic location.    | **King Udayana**                   |
            | **Avanti**                 | Ujjain, Mahishmati      | Important trade center in the northwest.               | **King Pradyota**                  |
            | **Vrijji Confederacy**     | Vaishali                | Early republic, democratic governance, birthplace of **Lord Mahavira**. | **Lichchhavis**, **Vajjis**        |
            | **Malla Republics**        | Kushinagara, Pava       | Significant for being the site where **Buddha** passed away. | **Mallas**                         |
            | **Kashi**                  | Varanasi                | Prominent center of Vedic learning and culture.        | **King Udayana**, **Varanasi**     |
            | **Anga**                   | Champa                  | Known for its trade and influence in the east.         | **King Srenika**                   |
            | **Magadh**                 | Rajgir                  | Birthplace of **Buddha** and major center of Buddhist monastic life. | **King Bimbisara**, **Ajatashatru**|
            | **Gandhara**               | Taxila                  | Center of ancient learning and trade, famous for Gandhara art. | **King Porus**                     |
            | **Kuru**                   | Hastinapura             | Associated with the **Mahabharata** and significant in Vedic traditions. | **King Shantanu**, **Dhritarashtra** |
            | **Panchala**               | Kampilya, Ahichhatra    | Known for its role in the Mahabharata, important in early history. | **King Drupada**                   |
            | **Chedi**                  | Shaktimati              | Known for its association with the epic **Mahabharata**. | **King Shishupala**                |
            | **Kekaya**                 | Vausali                 | Northern kingdom famous in epic tales and literature.  | **King Kambhoja**                  |
            | **Malloi**                 | Malla                   | Important center of trade and culture.                 | **King Malaya**                    |
            | **Shurasena**              | Mathura                 | Known for its commerce and religious significance.     | **King Kamsa**                     |

            ---
            ### 🌸 **Philosophical and Religious Movements**
            - **Rise of Buddhism**:
                - **Gautama Buddha**, the founder of Buddhism, emerged as a revolutionary spiritual leader challenging the ritualistic practices of Brahmanism. His **Four Noble Truths** and the **Eightfold Path** laid the foundation for Buddhism, emphasizing personal enlightenment, mindfulness, and detachment from suffering.
            - **Jainism and Mahavira**:
                - **Mahavira**, the 24th Tirthankara, revitalized the **Jain philosophy**, emphasizing **non-violence (Ahimsa)**, **truth (Satya)**, **non-possessiveness (Aparigraha)**, and **Anekantavada** (the doctrine of multiple viewpoints).
                - Jainism became one of the major spiritual paths of this period, advocating self-discipline and renunciation.
            - **Challenge to Brahmanism**:
                - Both Buddhism and Jainism opposed the established Vedic rituals and priestly authority, offering alternative paths to spiritual liberation.
        
            ---
            ### 🏙️ **Economic and Political Changes**
            - **Urbanization**:
                - The Mahajanapadas saw the rise of urban centers like **Rajgir**, **Varanasi**, and **Pataliputra**, which became hubs of trade, culture, and governance. These cities played a key role in the development of political and cultural life.
            - **Coinage and Trade**:
                - The use of **punch-marked coins** became widespread, facilitating trade across the region. This era saw the growth of commerce and a shift from barter to monetary exchange.
            - **Political Consolidation**:
                - The rise of **Magadha** as a powerful kingdom set the stage for future empires. Kings like **Bimbisara** and **Ajatashatru** played crucial roles in consolidating power and expanding their territories through diplomacy and warfare.
        
            ---
            ### 🎨 **Cultural Impact and Legacy**
            - **Art and Architecture**:
                - The Mahajanapada period saw the beginnings of **Buddhist** and **Jain art**. Stupas, sculptures, and cave monasteries began to emerge, marking the start of a rich artistic and architectural tradition that would continue for centuries.
                - **Stupa**: A significant architectural structure in Buddhism, the **stupa** symbolized the **Buddha's teachings**, becoming a place of meditation and worship.
            - **Codification of Laws**:
                - Early forms of codified laws emerged during this period. The **Arthashastra** by **Chanakya** is a notable work that outlines governance, diplomacy, economics, and military strategies, influencing later rulers like Chandragupta Maurya.
            - **Cultural Synthesis**:
                - The period also witnessed cultural synthesis, where different traditions, languages, and religious practices began to intermingle. **Sanskrit literature**, philosophy, and the rise of **Buddhist and Jain monasticism** contributed to the growth of an intellectual and cultural renaissance.

            ---
            ### 📜 **Legacy of the Mahajanapadas Period**
            - **Religious Revolution**: The rise of Buddhism and Jainism during this period had a profound impact on Indian society, challenging existing religious norms and offering new paths for spiritual and moral guidance.
            - **Political Foundation**: The **Mahajanapadas** set the stage for the rise of empires, particularly the **Maurya Empire**, which consolidated much of the subcontinent.
            - **Cultural Renaissance**: This period was a crucible for philosophical, religious, and cultural movements that laid the foundation for much of India's future development in the fields of art, literature, and governance.

            The **Mahajanapadas & Rise of Kingdoms** period was pivotal in shaping the political and spiritual landscape of ancient India, laying the foundation for a more centralized state and a flourishing of religious and philosophical thought that would influence the subcontinent for centuries. 🌸
            """)


        elif era == "🦁 Maurya Empire (321 BCE - 185 BCE)":
            st.markdown("""
            ### 🏰 **Maurya Empire (321 BCE - 185 BCE)**  
            The **Maurya Empire** was the first pan-Indian empire, founded by **Chandragupta Maurya** and expanded under the leadership of **Ashoka the Great**. It stands as a monumental period in Indian history, blending political brilliance with deep spiritual transformation.

            ---
            ### 🛡️ **Founding and Expansion**
            - **Chandragupta Maurya**:
                - Guided by **Chanakya** (author of the **Arthashastra**), Chandragupta united various smaller kingdoms into a single empire.
                - Expanded the empire across the Indian subcontinent, including territories of **Afghanistan** and parts of **Persia**.
            - **Territorial Conquests**:
                - The empire became one of the largest in the world at its peak, stretching from **Afghanistan** in the northwest to **Bangladesh** in the east and **central India** in the south.

            ---
            ### ✨ **Ashoka the Great: The Transformation**
            - **Kalinga War**:
                - After a brutal victory in the **Kalinga War** (261 BCE), Ashoka witnessed the devastating loss of life and suffering. This prompted him to renounce violence.
            - **Adoption of Buddhism**:
                - Ashoka embraced **Buddhism** and devoted his reign to the principles of **non-violence (Ahimsa)**, **compassion**, and **righteous living (Dhamma)**.
                - He worked towards spreading Buddhist values across Asia, sponsoring the construction of stupas, monasteries, and promoting the teachings of Buddha.

            ---
            ### 🏛️ **Administrative Brilliance**
            - **Centralized Governance**:
                - The empire was divided into **provinces (Janapadas)**, each governed by royal appointees, ensuring a centralized control while maintaining local governance.
            - **Efficiency and Surveillance**:
                - Ashoka developed a highly efficient **spy system** to monitor governance, ensuring fairness and compliance with his ideals.
            - **Taxation System**:
                - A fair taxation policy was implemented, with funds being used for public welfare and the construction of infrastructure, like roads, hospitals, and rest houses.

            ---
            ### 📜 **Cultural and Historical Contributions**
            - **Ashoka’s Edicts**:
                - Ashoka’s **Rock and Pillar Inscriptions** spread his Dhamma and Buddhist teachings, emphasizing **moral values**, **religious tolerance**, and **peaceful coexistence**.
                - The **Edicts of Ashoka** can still be seen in various locations across India, acting as a testament to his reign.
            - **Urban Development**:
                - Ashoka oversaw the development of well-planned cities, with infrastructure such as roads, **hospitals**, and **rest houses** for travelers, which were revolutionary at the time.
            - **Religious Harmony**:
                - Promoted religious tolerance, encouraging respect for all beliefs and emphasizing the importance of ethical living.

            ---
            ### 🕉️ **Spiritual Influence**
            - **Promotion of Buddhism**:
                - Ashoka played a key role in the spread of **Buddhism** across India and to distant lands like **Sri Lanka**, **Nepal**, **Central Asia**, and **Southeast Asia**.
            - **Dhamma (Righteous Living)**:
                - Ashoka’s philosophy, called **Dhamma**, focused on the welfare of his people, respect for elders, kindness to animals, and tolerance for all religions.
            - **Buddhist Architecture**:
                - Construction of **stupas**, **monasteries**, and **pillars**, including the famous **Sanchi Stupa**, which became centers of Buddhist learning and meditation.

            ---
            ### 🌍 **Legacy of the Maurya Empire**
            - **Political Unity**:
                - The Maurya Empire established the first **unified Indian subcontinent**, providing a foundation for later empires to build upon.
            - **Ashoka’s Reforms**:
                - Ashoka’s adoption of **non-violence** and **Buddhist principles** had a lasting impact on Indian culture and society, influencing rulers like **Kanishka** and beyond.
            - **Cultural Renaissance**:
                - The Maurya Empire ushered in an era of **cultural renaissance**, with profound impacts on Indian **art**, **architecture**, and **philosophy**.
            - **Spread of Buddhism**:
                - Ashoka’s missionary work and patronage helped spread Buddhism beyond India, establishing it as a world religion.

            ---
            ### 🛕 **Key Contributions of the Maurya Empire**
            Below is a table summarizing the Maurya Empire’s major contributions:

            | **Field**                    | **Key Achievements**                                        | **Key Figures/Examples**          |
            |------------------------------|------------------------------------------------------------|-----------------------------------|
            | **Founding of the Empire**   | Unified smaller kingdoms, forming India’s first pan-Indian empire. | **Chandragupta Maurya**, **Chanakya** |
            | **Buddhism**                  | Spread Buddhism across Asia, renounced violence.          | **Ashoka the Great**             |
            | **Governance**                | Centralized governance, provincial autonomy, efficient spy system. | **Ashoka**, **Royal Appointees** |
            | **Cultural Contributions**    | Ashoka’s Edicts promoting peace and religious harmony.     | **Ashoka’s Edicts**, **Stupas**  |
            | **Infrastructure**            | Developed roads, hospitals, rest houses, and cities.       | **Ashoka’s Infrastructure Projects** |
            | **Religious Tolerance**       | Promoted tolerance and respect for all faiths.             | **Ashoka**                       |

            ---
            ### 🌸 **The Enduring Legacy of Ashoka**
            - Ashoka’s reign, marked by his conversion to **Buddhism** and promotion of **Dhamma**, left a lasting legacy on India’s spiritual and political landscape.
            - His **Edicts**, scattered across the subcontinent, continue to inspire millions with their message of peace, tolerance, and righteous living.

            The **Maurya Empire** set the stage for a unified India, both culturally and politically, and Ashoka’s **transformational leadership** remains a beacon of moral governance and spiritual growth. 🌿
            """)


        elif era == "🛡️ Gupta Empire (320 CE - 550 CE)":
            st.markdown("""
            ### 🌟 **Gupta Empire (320 CE - 550 CE)**  
            Known as the **Golden Age of India**, the Gupta Empire witnessed unprecedented achievements in science, mathematics, culture, and spirituality.

            ---
            ### 🧠 **Scientific and Mathematical Achievements**
            - **Aryabhata**:
                - Introduced the concept of **zero** and **decimal system**.
                - Proposed the **heliocentric theory**, stating that the Earth rotates on its axis.
            - **Medicine**:
                - Compilation of detailed surgical techniques in the **Sushruta Samhita**.
                - Advances in herbal medicine, vaccinations, and veterinary sciences.
            - **Astronomy**:
                - Development of accurate astronomical calendars and instruments.

            ---
            ### 📚 **Cultural and Spiritual Flourishing**
            - **Sanskrit Literature**:
                - **Kalidasa**, the great poet and playwright, authored masterpieces like:
                    - **Shakuntala**: A love story of Shakuntala and King Dushyanta.
                    - **Meghaduta**: A lyrical poem about longing and separation.
                - Flourishing of fables like **Panchatantra** and **Hitopadesha**.
            - **Hindu Temple Architecture**:
                - Early examples of temple design like **Dashavatara Temple (Deogarh)** and **Udayagiri caves**.
                - Sculptures depicting Vishnu, Shiva, and Devi in elaborate forms.

            #### **Sanatan Dharma**
            - Revival and codification of **Vedic rituals** and **Hindu philosophy**.
            - Promotion of **Vaishnavism**, **Shaivism**, and **Shaktism**.
            - Sacred texts like **Puranas** were written and expanded during this era.

            ---
            ### 💰 **Political and Economic Prosperity**
            - **Centralized Administration**:
                - Efficient governance with local autonomy for provinces.
                - Strong military ensuring internal peace and stability.
            - **Trade and Commerce**:
                - Flourished with **Roman Empire**, **Southeast Asia**, and **China**.
                - Export of silk, spices, jewelry, and precious metals.
            - **Craftsmanship**:
                - Growth of guilds specializing in textiles, metalwork, and pottery.

            ---
            ### 🛕 **Key Contributions to Art and Architecture**
            - **Temple Architecture**:
                - **Dashavatara Temple (Deogarh)**: Early example of Gupta temple design.
                - Rock-cut caves at **Udayagiri**, depicting Vishnu in his **Varaha avatar**.
            - **Sculpture**:
                - Graceful depictions of Hindu deities, marked by intricate detailing and spiritual depth.
            - **Painting**:
                - Early murals at **Ajanta Caves**, showcasing Buddhist themes and Gupta artistry.

            ---
            ### 🕉️ **Spiritual Legacy**
            - Codification of **Yoga Sutras** and refinement of meditation techniques.
            - Expansion of **Hindu philosophy** and **Buddhist teachings** to Southeast Asia.
            - Creation of **Tantras** focusing on spirituality and rituals.

            ---
            ### 📜 **Key Contributions of the Gupta Empire**
            Below is a table summarizing the Gupta Empire’s major contributions:

            | **Field**                 | **Key Achievements**                                       | **Key Figures/Examples**            |
            |---------------------------|-----------------------------------------------------------|-------------------------------------|
            | **Mathematics**           | Decimal system, zero, value of pi.                        | **Aryabhata**                       |
            | **Astronomy**             | Heliocentrism, accurate planetary calculations.           | **Aryabhata**                       |
            | **Medicine**              | Surgical techniques, herbal treatments.                  | **Sushruta Samhita**                |
            | **Literature**            | Sanskrit epics, fables, lyrical poetry.                  | **Kalidasa**, **Panchatantra**      |
            | **Temple Architecture**   | Early Hindu temples, intricate rock-cut sculptures.       | **Dashavatara Temple**, **Udayagiri** |
            | **Trade and Economy**     | Roman trade, guild-based craftsmanship.                  | Silk, spices, jewelry exports       |
            | **Philosophy**            | Codification of Hindu texts, Buddhist expansion.          | **Puranas**, **Yoga Sutras**        |

            ---
            ### ✨ **Legacy of the Gupta Empire**
            - Pioneered a golden era of **science**, **spirituality**, and **culture**, influencing generations to come.
            - Spread Indian knowledge, traditions, and spirituality across **Asia**, leaving an indelible mark on history.
            - Symbolized a harmonious blend of **Sanatan Dharma** and cultural innovation. 🌺🕉️

            The Gupta Empire stands as a beacon of India’s rich and diverse heritage, celebrated for its spiritual and intellectual advancements.
            """)


        elif era == "🏰 Medieval India (750 CE - 1200 CE)":
            st.markdown("""
            ### 🏺 **Medieval India (750 CE - 1200 CE)**  
            This period was marked by the rise of powerful regional kingdoms, the flourishing of art and spirituality, and remarkable cultural advancements.

            ---
            ### 🛡️ **Prominent Kingdoms and Dynasties**
            - **Chola Dynasty (850 CE - 1250 CE)**:
                - Expanded through naval expeditions to **Sri Lanka** and **Southeast Asia**.
                - Established efficient administration and fostered economic prosperity.
            - **Rashtrakutas (753 CE - 982 CE)**:
                - Known for patronizing art, culture, and literature.
                - Built stunning rock-cut temples like **Kailasa Temple** at Ellora.
            - **Palas (8th - 12th Century)**:
                - Patrons of **Buddhism**, founded centers like **Nalanda** and **Vikramashila**.
                - Spread Indian culture to Southeast Asia.
            - **Rajput Kingdoms**:
                - Emerged as defenders of Hindu culture, resisting invasions and preserving traditions.

            ---
            ### 🌟 **Cultural and Spiritual Developments**
            #### **Bhakti Movement**
            - Saints like the **Alvars** and **Nayanars** in Tamil Nadu popularized devotion to Vishnu and Shiva.
            - Prominent figures:
                - **Andal**: Female Alvar saint known for her passionate devotion to Lord Vishnu.
                - **Appar** and **Sundarar**: Nayanar saints promoting Shaivism through Tamil hymns.
            - Key Teachings:
                - Emphasis on **personal devotion** over rituals and caste distinctions.
                - Promoted unity among followers of different social strata.

            #### **Sufi Movements**
            - Introduced mysticism, emphasizing **love and unity** across religions.
            - Early Sufi saints in India began spreading messages of harmony.

            ---
            ### 🛕 **Architectural and Artistic Achievements**
            - **Chola Temples**:
                - **Brihadeeswarar Temple** (Tanjore): A UNESCO World Heritage Site, showcasing exquisite Dravidian architecture.
                - **Gangaikonda Cholapuram Temple**: Symbol of Chola power and artistic brilliance.
            - **Ellora Caves**:
                - Rock-cut temples dedicated to Hinduism, Buddhism, and Jainism, built by the **Rashtrakutas**.
            - **Sculpture and Art**:
                - Detailed bronze idols of deities like **Nataraja (Lord Shiva)**, created by Chola artisans.

            ---
            ### 🌏 **Military Feats and Regional Influence**
            - **Chola Naval Expeditions**:
                - Established dominance over the **Bay of Bengal** and expanded trade to **Southeast Asia**.
                - Spread Indian culture, Hinduism, and Tamil scripts to **Indonesia**, **Malaysia**, and **Thailand**.
            - **Rajput Resistance**:
                - Defended northern India against early Islamic invasions, ensuring the survival of Hindu traditions.

            ---
            ### 📜 **Key Spiritual and Cultural Contributions**
            Below is a table summarizing the significant contributions of the medieval era:

            | **Dynasty/Movement**      | **Key Contributions**                                                                 | **Key Figures/Temples**                     |
            |---------------------------|---------------------------------------------------------------------------------------|---------------------------------------------|
            | **Cholas**                | Temple construction, bronze sculptures, naval dominance.                             | **Brihadeeswarar Temple**, Nataraja Idol    |
            | **Rashtrakutas**          | Patronage of art and rock-cut temples.                                               | **Kailasa Temple** at Ellora                |
            | **Palas**                 | Spread of Mahayana Buddhism, establishment of monasteries.                           | **Nalanda**, **Vikramashila**               |
            | **Bhakti Movement**       | Emphasis on devotion to Vishnu and Shiva, unity among castes.                        | **Andal**, **Appar**, **Sundarar**          |
            | **Sufi Movements**        | Promoted mysticism and religious harmony.                                            | Early Sufi saints                           |
            | **Rajputs**               | Preservation of Hindu culture and traditions through resilience against invasions.   | Forts like **Chittorgarh**                  |

            ---
            ### ✨ **Legacy of Medieval India**
            - Flourishing of art, architecture, and spirituality, showcasing the resilience of Sanatan Dharma.
            - Establishment of India’s cultural and spiritual influence across Asia.
            - A blend of devotion, resistance, and creativity that laid the groundwork for the cultural unity of India.

            The **Medieval Era** remains a testament to India’s spiritual and artistic heritage, where the essence of Sanatan Dharma thrived through trials and innovations. 🌺🕉️
            """)


        elif era == "👑 Mughal Empire (1526 CE - 1857 CE)":
            st.markdown("""
            ### 🏰 **Mughal Empire (1526 CE - 1857 CE)**  
            The Mughal Empire played a pivotal role in shaping Indian history, blending cultures, leaving a rich architectural legacy, and also witnessing destruction of temples and suppression of Vedic practices.

            ---
            ### ⚔️ **Political and Military Achievements**
            - **Foundation of the Empire**:
                - 🗓️ **1526**: **Babur** defeated Ibrahim Lodi in the **First Battle of Panipat**, establishing Mughal rule in India.
            - **Key Rulers**:
                - **Akbar the Great (1556-1605)**: Expanded the empire through diplomacy and military campaigns, introducing policies of **religious tolerance**.
                - **Shah Jahan (1628-1658)**: Focused on monumental architecture and the arts.
                - **Aurangzeb (1658-1707)**: Expanded the empire to its greatest territorial extent but followed a stricter, divisive religious policy.
            - **Decline**:
                - After **Aurangzeb**, weak successors and internal conflicts led to the empire’s decline, culminating in its fall during the **Revolt of 1857**.

            ---
            ### 🛕 **Impact on Hindu Temples and Vedic Culture**
            Below is a table summarizing key instances of temple destruction and suppression of Vedic culture during the Mughal period:

            | **Temple/Spiritual Site**          | **Location**              | **Event**                                                                                     | **Ruler Responsible**      |
            |-----------------------------------|--------------------------|---------------------------------------------------------------------------------------------|----------------------------|
            | **Kashi Vishwanath Temple**       | Varanasi (Uttar Pradesh) | Demolished and replaced with **Gyanvapi Mosque**.                                            | Aurangzeb                  |
            | **Somnath Temple**                | Gujarat                  | Plundered multiple times for its wealth.                                                    | Aurangzeb                  |
            | **Krishna Janmabhoomi Temple**    | Mathura (Uttar Pradesh)  | Demolished and replaced with **Shahi Idgah Mosque**.                                         | Aurangzeb                  |
            | **Martand Sun Temple**            | Kashmir                  | Destroyed to suppress Hindu practices.                                                      | Sikandar Butshikan (precursor to Mughal period) |
            | **Jain and Buddhist Temples**     | Throughout India         | Targeted destruction of non-Islamic shrines and religious centers.                           | Various Mughal rulers      |
            | **Nalanda and Takshashila**       | Bihar and Punjab         | Centers of Vedic education destroyed, impacting ancient Indian knowledge and culture.        | Precursor invasions, later influenced under Mughal rule |
            | **Vijayanagara Temples**          | Karnataka                | Temples in **Hampi** desecrated after Mughal-allied invasions.                               | Mughal alliances           |
            | **Ayodhya Ram Temple**            | Ayodhya (Uttar Pradesh)  | Destroyed and replaced with the **Babri Mosque**.                                            | Babur                      |

            ---
            ### 🌟 **Key Impacts on Vedic Culture**
            - **Destruction of Knowledge Hubs**:
                - Ancient centers of learning like **Nalanda** and **Takshashila** were destroyed, severing links to India’s scholarly heritage.
            - **Suppression of Festivals**:
                - Restrictions were placed on Hindu festivals like **Diwali** and **Holi**.
            - **Imposition of Jizya**:
                - Heavy **jizya tax** was imposed on non-Muslims, discouraging the free practice of Vedic traditions.
            - **Cultural Resilience**:
                - Saints and scholars preserved Vedic teachings through oral traditions, Bhakti poetry, and devotion.

            ---
            ### 🎨 **Cultural Contributions**
            - **Architecture**:
                - 🕌 Iconic monuments blending Persian, Indian, and Islamic styles:
                    - **Taj Mahal** (Agra): A symbol of love built by Shah Jahan.
                    - **Red Fort** (Delhi): A magnificent fort showcasing Mughal grandeur.
                    - **Fatehpur Sikri**: Akbar’s planned city, now a UNESCO World Heritage Site.
                - Grand mosques like the **Jama Masjid** and **Badshahi Mosque**.
            - **Art and Literature**:
                - 🌺 Flourishing of **miniature paintings** and the development of the **Mughal School of Art**.
                - 📖 Patronage of Urdu poetry and Persian literature.
            - **Gardens**:
                - Creation of **charbagh-style gardens**, emphasizing symmetry and harmony.

            ---
            ### 🧱 **Administrative Systems**
            - **Mansabdari System**:
                - Hierarchical ranking system introduced by Akbar to organize the military and civil administration.
            - **Land Revenue (Zabt) System**:
                - Efficient tax collection system ensuring economic stability during Akbar’s reign.
            - **Trade and Economy**:
                - Promotion of trade routes, linking India with Central Asia, Persia, and Europe.
                - Introduction of **silver rupee coins**.

            ---
            ### 🌟 **Spiritual Revival and Resistance**
            - **Bhakti Movement**:
                - Saints like **Tulsidas**, **Meerabai**, and **Kabir** preserved the essence of Hindu spirituality through devotional songs and poetry.
                - Writings like the **Ramcharitmanas** (by Tulsidas) inspired the masses.
            - **Rise of the Sikh Gurus**:
                - The Sikh faith, led by Gurus like **Guru Nanak** and **Guru Gobind Singh**, emphasized equality, justice, and resistance to oppression.
            - **Temple Restoration Efforts**:
                - Rulers like **Chhatrapati Shivaji** rebuilt desecrated temples, ensuring the continuation of spiritual practices.

            ---
            ### 📜 **Legacy of the Mughal Empire**
            - **Contributions**:
                - Iconic architecture, art, and administrative innovations.
            - **Controversies**:
                - Religious intolerance and destruction of spiritual sites left a scar on India's cultural landscape.

            The **Mughal Empire** remains a period of immense creativity and resilience, with Sanatan Dharma emerging stronger through centuries of trials. 🕉️🏰
            """)



        elif era == "🌍 Colonial Period (1757 CE - 1947 CE)":
            st.markdown("""
            ### 🕉️ **Colonial Period (1757 CE - 1947 CE)**  
            The Colonial Period not only saw India under British domination but also witnessed a profound revival of **Sanatan Dharma** and the rise of several spiritual movements that reignited India’s cultural and spiritual identity.

            ---
            ### 🛕 **Spiritual Awakening and Movements**
            The colonial period brought a resurgence in spirituality as sages and reformers worked to preserve and promote the values of Sanatan Dharma amidst foreign domination.

            | **Year**  | **Spiritual Movement/Event**                  | **Key Figures and Details**                                                  |
            |-----------|-----------------------------------------------|-------------------------------------------------------------------------------|
            | 1828      | **Brahmo Samaj**                              | Founded by **Raja Ram Mohan Roy**, focusing on monotheism and social reforms. |
            | 1867      | **Arya Samaj**                                | Established by **Swami Dayananda Saraswati**, promoting Vedic teachings.      |
            | 1863-1902 | **Ramakrishna Movement**                      | Led by **Ramakrishna Paramahamsa** and carried forward by **Swami Vivekananda**.|
            | 1893      | **Swami Vivekananda's Chicago Speech**         | Introduced the world to India’s spiritual heritage at the **Parliament of Religions**.|
            | 1915      | **Mahatma Gandhi’s Spiritual Leadership**     | Introduced the principle of **Ahimsa (nonviolence)** as a spiritual weapon.   |
            | 1920      | **Self-Realization Fellowship**               | Founded by **Paramahansa Yogananda**, spreading Kriya Yoga globally.         |

            ---
            ### 🧘‍♂️ **Key Spiritual Figures and Their Contributions**
            - **Ramakrishna Paramahamsa (1836-1886)**:
                - Emphasized the unity of all religions and realization of God through devotion and meditation.
            - **Swami Vivekananda (1863-1902)**:
                - Advocated Vedanta philosophy and inspired the youth to revive Indian spirituality and culture.
            - **Swami Dayananda Saraswati (1824-1883)**:
                - Founded Arya Samaj to revive Vedic knowledge and oppose superstition.
            - **Paramahansa Yogananda (1893-1952)**:
                - Author of **Autobiography of a Yogi**, instrumental in popularizing yoga and meditation in the West.
            - **Sri Aurobindo (1872-1950)**:
                - Merged spirituality with nationalism; emphasized **Integral Yoga** for self-realization and social progress.
            - **Mahatma Gandhi (1869-1948)**:
                - Used spiritual values like truth, nonviolence, and simplicity as tools for India’s independence.

            ---
            ### ✨ **Revival of Sanatan Dharma**
            - 🕉️ **Bhakti Movement**: Saints like **Ramana Maharshi** and **Sai Baba of Shirdi** inspired millions with their teachings on devotion and universal love.
            - 📖 **Preservation of Scriptures**: Scholars translated and preserved ancient texts like the **Bhagavad Gita**, **Upanishads**, and **Vedas**.
            - 🛕 **Temple Rejuvenation**: Efforts were made to restore and protect key temples from colonial neglect.
            - ✨ **Global Recognition**: Vivekananda’s speech in Chicago and the rise of Indian mysticism attracted global attention to Sanatan Dharma.

            ---
            ### 📜 **Cultural and Spiritual Impact**
            - **Rediscovery of India’s Spiritual Roots**:
                - Encouraged self-confidence and pride in India's spiritual and cultural heritage.
            - **Spiritual Nationalism**:
                - Leaders like **Sri Aurobindo** and **Bal Gangadhar Tilak** merged spirituality with the freedom struggle.
            - **Spread of Yoga and Meditation**:
                - Indian spiritual practices like **yoga** and **kirtan** became popular in the West.
            - **Resistance to Conversion**:
                - Movements like Arya Samaj opposed forced religious conversions and worked to preserve Hinduism.

            ---
            ### 🕊️ **Freedom Through Spirituality**
            Many leaders of the independence struggle drew inspiration from spirituality:
            - **Gandhi’s Satyagraha**: Nonviolence and truth as spiritual principles to fight oppression.
            - **Tilak’s Call for Swaraj**: Declared that **“Swaraj is my birthright”**, connecting it to Dharma.
            - **Aurobindo’s Vision**: A free India as a spiritual leader for the world.

            ---
            ### 🌟 **Catchy Highlights**
            - 🪷 **Unity of Religions**: Ramakrishna and Vivekananda emphasized harmony among all faiths.
            - 📚 **Educational Reforms**: Schools like the **Ramakrishna Mission** combined spiritual teachings with modern education.
            - 🌐 **Global Reach**: Indian spiritual masters like Yogananda and Vivekananda inspired millions worldwide.
            - 🕊️ **Cultural Renaissance**: The period saw a revival of traditional arts, literature, and spiritual practices.

            ---
            The **Colonial Period** was not only a time of political struggle but also a profound spiritual awakening that redefined India’s identity and strengthened its resolve for independence. 🕉️🇮🇳
            """)


        elif era == "🚀 Modern India (1947 CE - Present)":
            st.markdown("""
            ### **Modern India (1947 CE - Present)**  
            **Modern India** began on August 15, 1947, with India's independence from British rule. This era has witnessed remarkable political, economic, technological, and cultural transformations.

            ---
            ### 🏛️ **Key Political Events**
            - 🗓️ **1947:** India gained independence, and Pakistan was formed through Partition.
            - 🗓️ **1950:** Adoption of the **Indian Constitution** on January 26; India became a Republic.
            - 🗓️ **1947-1955:** Integration of 562 princely states by **Sardar Vallabhbhai Patel**.
            - 🗓️ **1975-1977:** **Emergency Period** declared by Indira Gandhi.
            - 🗓️ **1992:** Economic liberalization introduced by **P.V. Narasimha Rao** and **Manmohan Singh**.
            - 🗓️ **2014:** Narendra Modi became Prime Minister, initiating policies like **Digital India**, **Make in India**, and **Startup India**.

            ---
            ### 🌾 **Economic Development**
            - 🌱 **Green Revolution (1960s):** Boosted agricultural productivity and self-sufficiency in food grains.
            - 📈 **1991 Economic Reforms:** Liberalization, Privatization, and Globalization transformed India's economy.
            - 🏗️ **Rise in Infrastructure:** Development of metro systems, smart cities, and highways.
            - 🌐 **IT Revolution (2000s):** Emergence of India as a global leader in software and IT services.
            - 🏦 **GST Implementation (2017):** Unified India's taxation system.

            ---
            ### 🚀 **Technological and Cultural Achievements**
            - 🛰️ **1969:** Establishment of **ISRO** (Indian Space Research Organisation).
                - 🚀 **2014:** Mangalyaan (Mars Orbiter Mission) made India the first country to succeed on its first attempt.
                - 🌕 **2019:** Chandrayaan-2 mission for lunar exploration.
                - 🌑 **2023:** Chandrayaan-3 made a successful soft landing on the moon's south pole.
            - 📡 **Digital India Campaign:** Transforming India into a digitally empowered society.
            - 🏏 **Sports Achievements:** Cricket World Cups (1983, 2011), Olympic medals in various sports.
            - 🎨 **Cultural Renaissance:** Bollywood's global reach and the promotion of Indian classical arts and yoga.

            ---
            ### ✊ **Freedom Movements and Key Events**
            Below is a timeline of key movements that shaped Modern India:

            | **Year** | **Movement/Event**                                             | **Details**                                                                 |
            |----------|---------------------------------------------------------------|-----------------------------------------------------------------------------|
            | 1947     | **Independence and Partition**                                | Freedom from British rule; creation of India and Pakistan.                  |
            | 1948     | **Assassination of Mahatma Gandhi**                           | Father of the Nation assassinated by Nathuram Godse.                        |
            | 1956     | **Reorganization of States**                                  | States reorganized based on linguistic lines.                               |
            | 1965     | **Indo-Pak War**                                              | Conflict over Kashmir.                                                      |
            | 1971     | **Bangladesh Liberation War**                                 | India played a key role in the creation of Bangladesh.                      |
            | 1975     | **Emergency**                                                 | Civil liberties suspended; major political crisis.                          |
            | 1984     | **Operation Blue Star & Anti-Sikh Riots**                     | Military operation in Punjab; followed by riots after Indira Gandhi's death.|
            | 1992     | **Babri Masjid Demolition**                                   | Religious tensions escalated after the demolition in Ayodhya.               |
            | 2020     | **Farmers' Protest**                                          | Protest against farm laws; later repealed.                                  |

            ---
            ### 🔍 **Catchy Highlights**
            - 🏆 **India as a Global Leader:** Recognized for its role in IT, space research, and peacekeeping missions.
            - 🌏 **Environmental Focus:** Initiatives like **National Solar Mission** and international climate commitments.
            - ✨ **Cultural Diplomacy:** Yoga Day (June 21) declared by the UN, showcasing India's soft power.

            ---
            **Modern India** stands as a testament to its resilience, diversity, and progress, constantly evolving as a major player on the global stage. 🇮🇳
            """)


        # Knowledge Base Search
        st.subheader("🔎 Search the Knowledge Base")
        search_query = st.text_input("Type your query here:", placeholder="E.g., Contributions of Aryabhata, Bhakti Movement, etc.")
        if st.button("Search History"):
            if search_query.strip():
                with st.spinner("Fetching information from the knowledge base..."):
                    context = (
                        "You are VedaGPT, an advanced AI specializing in Indian history and culture. "
                        "Provide highly accurate, in-depth, and well-researched information about the user's query. "
                        "Incorporate references to India's ancient texts, spiritual philosophies, historical events, and cultural significance. "
                        "Present your answers in a professional tone, emphasizing clarity, context, and relevance to the query."
                    )
                    response = query_gemini(context, search_query, language_code)
                    if response:
                        st.write("### 📚 **Search Results:**")
                        st.markdown(f"> {response}")
                    else:
                        st.error("No relevant information found. Try refining your query.")

                    # Recommendations Section
                    st.markdown("### 🔍 Additional Insights & Suggestions")
                    recommendations = generate_recommendations_based_on_input(search_query, language_code)
                    if "recommendations" not in st.session_state:
                        st.session_state.recommendations = recommendations
                    
                    with st.expander("📜 Explore Related Topics and Practices"):
                        for rec in st.session_state.recommendations:
                            st.markdown(f"- **{rec}**")
            else:
                st.warning("Please enter a query to search the knowledge base.")




# Footer Section
st.divider()
with st.container():
    st.markdown("""
        <div style="text-align: center; padding: 20px; color: #555;">
            <p style="font-size: 14px; font-weight: bold;">Developed with Passion and Precision</p>
            <p style="font-size: 12px;">Crafted by Aditya Pandey | Building the Future of AI & Spiritual Wisdom 🔱</p>
            <p style="font-size: 10px; color: #777;">Innovating with technology, rooted in tradition.</p>
        </div>
    """, unsafe_allow_html=True)
