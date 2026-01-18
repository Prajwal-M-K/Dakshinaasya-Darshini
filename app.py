
import streamlit as st
import google.generativeai as genai
import os
import speech_recognition as sr
from audiorecorder import audiorecorder
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
        padding-bottom: 100px !important;
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
    
    /* Content area */
    .content-area {
        padding-top: 80px;
        text-align: center;
    }
    
    /* Om symbol */
    .om-symbol {
        font-size: 5rem;
        color: #B8860B;
        margin: 30px 0 20px 0;
        line-height: 1;
    }
    
    /* Namaste heading */
    .namaste-heading {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a1a !important;
        margin: 20px 0 15px 0;
    }
    
    /* Subtitle */
    .subtitle {
        font-size: 1.1rem;
        color: #666 !important;
        margin-bottom: 40px;
        line-height: 1.6;
    }
    
    /* Try asking label */
    .try-asking {
        color: #999 !important;
        font-size: 0.95rem;
        margin-bottom: 20px;
    }
    
    /* Suggestion buttons container */
    .suggestion-buttons {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 15px;
        margin-bottom: 40px;
    }
    
    /* Individual suggestion button */
    .suggestion-btn {
        background-color: transparent !important;
        border: 1.5px solid #B8860B !important;
        color: #4a4a4a !important;
        padding: 12px 24px !important;
        border-radius: 25px !important;
        font-size: 0.95rem !important;
        cursor: pointer;
        transition: all 0.2s ease;
        font-weight: 400 !important;
    }
    
    .suggestion-btn:hover {
        background-color: rgba(184, 134, 11, 0.1) !important;
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
    }
    
    .mic-icon-hint {
        font-size: 1.1rem;
    }
    
    /* Bottom input container */
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #f5f5f5;
        padding: 15px 20px;
        display: flex;
        align-items: center;
        gap: 15px;
        z-index: 1000;
    }
    
    /* Text input styling */
    .stTextInput > div > div > input {
        border-radius: 25px !important;
        border: 1px solid #ddd !important;
        padding: 15px 20px !important;
        font-size: 1rem !important;
        background-color: white !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #B8860B !important;
        box-shadow: none !important;
    }
    
    /* Mic button */
    .mic-button {
        background-color: #B8860B !important;
        color: white !important;
        border: none !important;
        border-radius: 50% !important;
        width: 55px !important;
        height: 55px !important;
        font-size: 1.5rem !important;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    
    /* Chat message styling */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 15px;
        padding: 15px;
        margin: 10px 0;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
    }
    
    /* Bottom input area - LIGHT THEME */
    [data-testid="stBottom"] {
        background-color: rgba(245, 243, 238, 0.98) !important;
        background: linear-gradient(
            rgba(245, 243, 238, 0.98), 
            rgba(245, 243, 238, 0.98)
        ), url('https://www.starsai.com/wp-content/uploads/sri-dakshinamurthy.jpg') !important;
        background-size: cover !important;
        background-position: center bottom !important;
        padding: 15px 20px !important;
        border-top: 1px solid #e0d9c8 !important;
    }
    
    /* Chat input container wrapper */
    [data-testid="stChatInputContainer"] {
        background-color: transparent !important;
    }
    
    /* The outer chat input wrapper */
    [data-testid="stChatInput"] {
        background-color: transparent !important;
    }
    
    /* Chat input textarea */
    [data-testid="stChatInput"] textarea {
        border-radius: 30px !important;
        border: 1.5px solid #ccc !important;
        padding: 15px 60px 15px 20px !important;
        background-color: white !important;
        color: #333 !important;
        font-size: 1rem !important;
    }
    
    [data-testid="stChatInput"] textarea::placeholder {
        color: #999 !important;
    }
    
    [data-testid="stChatInput"] textarea:focus {
        border-color: #B8860B !important;
        box-shadow: 0 0 0 1px #B8860B !important;
    }
    
    /* Style the send button in chat input */
    [data-testid="stChatInput"] button {
        background-color: #B8860B !important;
        color: white !important;
        border-radius: 50% !important;
        border: none !important;
    }
    
    /* Audio recorder styling - positioned to look like it's in the input */
    .mic-wrapper {
        position: fixed;
        bottom: 25px;
        right: 80px;
        z-index: 1001;
    }
    
    div[data-testid="stAudioRecorder"] button,
    .stAudioRecorder > button {
        background-color: #B8860B !important;
        color: white !important;
        border-radius: 50% !important;
        width: 45px !important;
        height: 45px !important;
        min-width: 45px !important;
        font-size: 1.2rem !important;
        border: none !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.15) !important;
    }
    
    /* Toast notifications */
    [data-testid="stToast"] {
        color: #1a1a1a !important;
    }
    
    /* Welcome screen specific - center align everything */
    .welcome-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        min-height: 70vh;
        text-align: center;
    }
    
    /* Force all dark mode overrides to light */
    .stApp, .main, [data-testid="stAppViewContainer"] {
        color-scheme: light !important;
    }
    
    /* Override any remaining dark backgrounds */
    div[data-baseweb="base-input"] {
        background-color: white !important;
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

# --- Voice Input Function ---
def transcribe_audio(audio_bytes):
    """Convert audio bytes to text using Google Speech Recognition"""
    try:
        # Convert audio to WAV format for speech recognition
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
        wav_buffer = io.BytesIO()
        audio.export(wav_buffer, format="wav")
        wav_buffer.seek(0)

        # Use speech recognition
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_buffer) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data)
            return text
    except sr.UnknownValueError:
        return None
    except sr.RequestError as e:
        st.error(f"Speech recognition service error: {e}")
        return None
    except Exception as e:
        st.error(f"Audio processing error: {e}")
        return None

# --- UI ---

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat = model.start_chat(history=[]) if model else None
if "voice_input" not in st.session_state:
    st.session_state.voice_input = ""
if "last_audio_len" not in st.session_state:
    st.session_state.last_audio_len = 0
if "show_welcome" not in st.session_state:
    st.session_state.show_welcome = True

# Add top padding for fixed header
st.markdown('<div style="padding-top: 60px;"></div>', unsafe_allow_html=True)

# Function to handle suggestion click
def handle_suggestion(suggestion):
    st.session_state.pending_prompt = suggestion
    st.session_state.show_welcome = False

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
        <span class="mic-icon-hint">🎤</span>
        Tap mic to speak or type below
    </p>
    ''', unsafe_allow_html=True)

else:
    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# Process pending prompt from suggestion buttons
if "pending_prompt" in st.session_state and st.session_state.pending_prompt:
    prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None
    
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    if st.session_state.chat:
        with st.chat_message("assistant"):
            with st.spinner(""):
                try:
                    response = st.session_state.chat.send_message(prompt)
                    st.write(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Error: {e}")
    st.rerun()

# Voice input section - mic button positioned via CSS
# Audio recorder (will be positioned by CSS to appear in input bar)
audio = audiorecorder("🎤", "🔴", key="audio_recorder")

if len(audio) > 0:
    audio_bytes = audio.export().read()
    current_len = len(audio_bytes)
    
    # Auto-transcribe when new audio is detected
    if current_len != st.session_state.last_audio_len:
        st.session_state.last_audio_len = current_len
        
        with st.spinner("🎤 Transcribing..."):
            transcribed_text = transcribe_audio(audio_bytes)
            if transcribed_text:
                st.session_state.voice_input = transcribed_text
                st.session_state.show_welcome = False
                st.rerun()
            else:
                st.toast("Could not understand audio. Please try again.", icon="⚠️")

# Process voice input if available
if st.session_state.voice_input:
    prompt = st.session_state.voice_input
    st.session_state.voice_input = ""

    with st.chat_message("user"):
        st.write(f"🎤 {prompt}")
    st.session_state.messages.append({"role": "user", "content": f"🎤 {prompt}"})

    if st.session_state.chat:
        with st.chat_message("assistant"):
            with st.spinner(""):
                try:
                    response = st.session_state.chat.send_message(prompt)
                    st.write(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Error: {e}")

# Chat input (text) - main input at bottom
if prompt := st.chat_input("Type your message..."):
    st.session_state.show_welcome = False
    
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    if st.session_state.chat:
        with st.chat_message("assistant"):
            with st.spinner(""):
                try:
                    response = st.session_state.chat.send_message(prompt)
                    st.write(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Error: {e}")
