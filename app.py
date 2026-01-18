
import streamlit as st
import google.generativeai as genai
import os
import speech_recognition as sr
import io
from pydub import AudioSegment

# --- Configuration ---
st.set_page_config(page_title="Dakshinaasya Darshini", page_icon="🕉️", layout="centered")

# --- Custom Styling to match the UI design ---
st.markdown("""
<style>
    /* Background image with overlay */
    .stApp {
        background: linear-gradient(
            rgba(255, 255, 255, 0.88), 
            rgba(255, 255, 255, 0.88)
        ), url('https://www.starsai.com/wp-content/uploads/sri-dakshinamurthy.jpg');
        background-size: cover;
        background-position: center top;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {display: none !important;}
    footer {display: none !important;}
    header {visibility: hidden !important;}
    [data-testid="stSidebar"] {display: none !important;}
    [data-testid="stSidebarCollapsedControl"] {display: none !important;}
    
    /* Main container styling */
    .main .block-container {
        padding-top: 0 !important;
        padding-bottom: 120px !important;
        max-width: 800px !important;
    }
    
    /* Header bar */
    .header-bar {
        background-color: #B8860B;
        padding: 15px 25px;
        margin: -1rem -1rem 0 -1rem;
        display: flex;
        justify-content: space-between;
        align-items: center;
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        z-index: 1000;
    }
    
    .header-title {
        color: white !important;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 0;
    }
    
    .header-settings {
        color: white;
        font-size: 1.5rem;
        cursor: pointer;
    }
    
    /* Om symbol */
    .om-symbol {
        font-size: 5rem;
        color: #B8860B;
        margin: 30px 0 20px 0;
        line-height: 1;
        text-align: center;
    }
    
    /* Namaste heading */
    .namaste-heading {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a1a !important;
        margin: 20px 0 15px 0;
        text-align: center;
    }
    
    /* Subtitle */
    .subtitle {
        font-size: 1.1rem;
        color: #666 !important;
        margin-bottom: 40px;
        line-height: 1.6;
        text-align: center;
    }
    
    /* Try asking label */
    .try-asking {
        color: #999 !important;
        font-size: 0.95rem;
        margin-bottom: 20px;
        text-align: center;
    }
    
    /* Streamlit button overrides for suggestion buttons */
    .stButton > button {
        background-color: transparent !important;
        border: 1.5px solid #B8860B !important;
        color: #4a4a4a !important;
        padding: 12px 24px !important;
        border-radius: 25px !important;
        font-size: 0.95rem !important;
        font-weight: 400 !important;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background-color: rgba(184, 134, 11, 0.1) !important;
        border-color: #B8860B !important;
        color: #4a4a4a !important;
    }
    
    /* Mic hint text */
    .mic-hint {
        color: #B8860B !important;
        font-size: 0.95rem;
        margin: 30px 0 20px 0;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        text-align: center;
    }
    
    /* Chat message styling */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    
    /* HIDE the default bottom chat input completely */
    [data-testid="stBottom"] {
        display: none !important;
    }
    
    /* Custom fixed bottom input bar */
    .custom-input-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background: linear-gradient(
            rgba(250, 248, 244, 0.98), 
            rgba(250, 248, 244, 0.98)
        );
        padding: 15px 20px;
        z-index: 1000;
        border-top: 1px solid #e8e4dc;
    }
    
    .input-wrapper {
        max-width: 760px;
        margin: 0 auto;
        display: flex;
        align-items: center;
        gap: 12px;
        background-color: white;
        border: 1.5px solid #ccc;
        border-radius: 30px;
        padding: 5px 5px 5px 20px;
    }
    
    .input-wrapper:focus-within {
        border-color: #B8860B;
    }
    
    /* Style the text input inside the form */
    .stTextInput > div > div > input {
        border: none !important;
        background: transparent !important;
        padding: 10px 0 !important;
        font-size: 1rem !important;
        color: #333 !important;
        box-shadow: none !important;
    }
    
    .stTextInput > div > div > input:focus {
        border: none !important;
        box-shadow: none !important;
        outline: none !important;
    }
    
    .stTextInput > div > div {
        border: none !important;
        background: transparent !important;
    }
    
    .stTextInput label {
        display: none !important;
    }
    
    /* Mic button styling */
    .mic-btn {
        background-color: #B8860B !important;
        color: white !important;
        border: none !important;
        border-radius: 50% !important;
        width: 46px !important;
        height: 46px !important;
        min-width: 46px !important;
        font-size: 1.2rem !important;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    
    /* Style form submit button */
    .stForm [data-testid="stFormSubmitButton"] > button {
        background-color: #B8860B !important;
        color: white !important;
        border: none !important;
        border-radius: 50% !important;
        width: 46px !important;
        height: 46px !important;
        min-width: 46px !important;
        padding: 0 !important;
    }
    
    /* Toast notifications */
    [data-testid="stToast"] {
        color: #1a1a1a !important;
    }
    
    /* Force light theme */
    .stApp, .main, [data-testid="stAppViewContainer"] {
        color-scheme: light !important;
    }
</style>

<!-- Header Bar -->
<div class="header-bar">
    <span class="header-title">Dakshinaasya Darshini</span>
    <span class="header-settings">⚙️</span>
</div>
""", unsafe_allow_html=True)

# --- Load Context & Initialize Model ---
@st.cache_resource
def setup_model():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        st.error("GEMINI_API_KEY not found. Please set it before running.")
        return None, None

    genai.configure(api_key=api_key)

    # Load context from same directory as this script
    import pathlib
    script_dir = pathlib.Path(__file__).parent
    context_path = script_dir / "Dakshina_Murthi_Context.txt"

    try:
        with open(context_path, "r", encoding="utf-8") as f:
            context = f.read()
    except FileNotFoundError:
        st.error(f"Context file not found at {context_path}")
        return None, None

    system_instruction = f"""You are Dakshinaasya Darshini — a wise, warm guide who has completely internalized the Dakshinamurty Ashtakam teachings as expounded by His Holiness Sri Sri Shankarabharati Mahaswamiji.

You are like a trusted friend who happens to be steeped in the teachings expounded in the upanyasa. People come to you with everything — stress at work, family troubles, existential questions, health worries, spiritual doubts, or just curiosity. You meet them exactly where they are.

YOUR FOUNDATION (the teachings you have absorbed):
{context}

═══════════════════════════════════════
HOW YOU RESPOND:
═══════════════════════════════════════

1. BE IMMEDIATE & PRACTICAL
   - This is meant to be like asking a wise guide. Respond quickly, clearly, directly.
   - If someone asks "I am anxious about my job interview tomorrow" — do not launch into philosophy. Ground them first. Then, if natural, connect to a deeper truth.

2. ADAPT YOUR LENGTH TO THEIR NEED
   - Distressed/emotional → 2-4 sentences. Warm. Grounding. One insight maximum.
   - Practical question → Direct answer, then spiritual dimension if relevant.
   - Philosophical/spiritual inquiry → More depth (but still 1-2 paragraphs max). Cite specific slokas or analogies.

3. USE ANALOGIES NATURALLY (only when they fit - do not force them)
   - Mirror & city: The world appears outside but exists within consciousness
   - Dream: The waking world is like a dream — real while experiencing, but not ultimately real
   - Rope & snake: We mistake one thing for another due to ignorance
   - Pot with lamp: Consciousness shines through the "holes" of our senses
   - Jackfruit & oil: Like oil on hands prevents stickiness, wisdom prevents suffering from sticking
   - Eclipse: The Self is always shining, just temporarily obscured
   - Seed & tree: Everything exists in potential, then manifests
   - Pratyabhijna: Recognition — "I who was a child am the same I now"

4. REAL-WORLD GROUNDING
   - The Guru himself spoke of: students passing exams through faith, overcoming fear of rats through sarvaatma bhaava, facing calamities with equanimity through daily practice.
   - You can suggest practical actions: reciting the stotra, contemplation before sleep, the "neti-neti" method, recognizing the witness in daily activities.

5. YOUR VOICE
   - Sound like a thoughtful friend who's read a lot, not a guru or priest. Natural, modern English.
   - NEVER use phrases like "my dear one", "dear seeker", "O friend" — just talk normally.
   - Warm but not saccharine. Clear but not cold. Wise but not preachy.
   - You can ask reflective questions. You can use gentle humor.
   - Keep it conversational. This is a chat, not a sermon.

6. CORE PRINCIPLE
   The essence: You are not the body, mind, or senses. You are pure consciousness (chaitanya), identical with the universal Self (Brahman). All suffering stems from forgetting this. All peace comes from remembering it. The world is not separate from you — it appears within you, like a dream.

   But you do not dump this on everyone. You offer what they need, when they need it.

═══════════════════════════════════════
REMEMBER: You are like a spiritual Alexa — immediate, helpful, always available. Meet people where they are. Brevity is compassion.
═══════════════════════════════════════"""

    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=system_instruction,
        generation_config=genai.GenerationConfig(
            temperature=0.7,
            max_output_tokens=1024,
        )
    )
    return model, context

model, context = setup_model()

# --- UI ---

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat = model.start_chat(history=[]) if model else None
if "show_welcome" not in st.session_state:
    st.session_state.show_welcome = True
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

# Add top padding for fixed header
st.markdown('<div style="padding-top: 60px;"></div>', unsafe_allow_html=True)

# Function to process and send message
def send_message(message):
    if message and message.strip():
        st.session_state.messages.append({"role": "user", "content": message})
        st.session_state.show_welcome = False
        
        if st.session_state.chat:
            try:
                response = st.session_state.chat.send_message(message)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.session_state.messages.append({"role": "assistant", "content": f"Error: {e}"})

# Function to handle suggestion click
def handle_suggestion(suggestion):
    send_message(suggestion)

# Welcome screen (only show when no conversation)
if st.session_state.show_welcome and len(st.session_state.messages) == 0:
    # Om Symbol
    st.markdown('<div class="om-symbol">ॐ</div>', unsafe_allow_html=True)
    
    # Namaste heading
    st.markdown('<h1 class="namaste-heading">Namaste!</h1>', unsafe_allow_html=True)
    
    # Subtitle
    st.markdown('''
    <p class="subtitle">
        I am Dakshinaasya Darshini, your spiritual guide.<br>
        Ask me anything.
    </p>
    ''', unsafe_allow_html=True)
    
    # Try asking label
    st.markdown('<p class="try-asking">Try asking:</p>', unsafe_allow_html=True)
    
    # Suggestion buttons - 2 rows of 2 buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Explain Sloka 1", key="btn1", use_container_width=True):
            handle_suggestion("Explain Sloka 1")
            st.rerun()
    with col2:
        if st.button("What is Tat Tvam Asi?", key="btn2", use_container_width=True):
            handle_suggestion("What is Tat Tvam Asi?")
            st.rerun()
    
    col3, col4 = st.columns(2)
    with col3:
        if st.button("I feel anxious", key="btn3", use_container_width=True):
            handle_suggestion("I feel anxious")
            st.rerun()
    with col4:
        if st.button("Mirror analogy", key="btn4", use_container_width=True):
            handle_suggestion("Mirror analogy")
            st.rerun()
    
    # Mic hint
    st.markdown('''
    <p class="mic-hint">
        🎤 Tap mic to speak or type below
    </p>
    ''', unsafe_allow_html=True)

else:
    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# Custom input bar at the bottom using HTML/CSS
st.markdown('''
<div class="custom-input-bar">
    <div class="input-wrapper" id="custom-input-wrapper">
        <!-- Input will be placed here by Streamlit -->
    </div>
</div>
''', unsafe_allow_html=True)

# Create the actual input using a form
with st.form(key="chat_form", clear_on_submit=True):
    col_input, col_mic, col_send = st.columns([8, 1, 1])
    
    with col_input:
        user_input = st.text_input(
            label="Message",
            placeholder="Type your message...",
            key="text_input",
            label_visibility="collapsed"
        )
    
    with col_mic:
        # Audio file uploader as mic alternative
        audio_file = st.file_uploader(
            "🎤",
            type=["wav", "mp3", "m4a", "ogg"],
            key="audio_upload",
            label_visibility="collapsed"
        )
    
    with col_send:
        submitted = st.form_submit_button("➤")

# Process text input
if submitted and user_input:
    send_message(user_input)
    st.rerun()

# Process audio input
if audio_file is not None:
    try:
        audio_bytes = audio_file.read()
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
        wav_buffer = io.BytesIO()
        audio.export(wav_buffer, format="wav")
        wav_buffer.seek(0)
        
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_buffer) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            if text:
                send_message(f"🎤 {text}")
                st.rerun()
    except Exception as e:
        st.toast(f"Could not process audio: {e}", icon="⚠️")
