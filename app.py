
import streamlit as st
import google.generativeai as genai
import os
import speech_recognition as sr
from audiorecorder import audiorecorder
import io
from pydub import AudioSegment

# --- Configuration ---
st.set_page_config(page_title="Dakshinaasya Darshini", page_icon="🕉️", layout="centered")

# --- Custom Styling: Light Mode, Background Image, Footer Logo ---
st.markdown("""
<style>
    /* Force light mode background */
    .stApp {
        background: linear-gradient(
            rgba(255, 255, 255, 0.92), 
            rgba(255, 255, 255, 0.92)
        ), url('https://www.starsai.com/wp-content/uploads/sri-dakshinamurthy.jpg');
        background-size: cover;
        background-position: center top;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }
    
    /* Force light theme on main content */
    .main .block-container {
        background-color: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        padding: 2rem;
        margin-top: 1rem;
    }
    
    /* Light mode text colors - force everywhere */
    .stMarkdown, .stMarkdown p, .stMarkdown span, 
    h1, h2, h3, p, span, label,
    [data-testid="stChatMessage"] p,
    .stChatMessage, div, .element-container {
        color: #1a1a1a !important;
    }
    
    /* Title styling */
    h1 {
        color: #4a0080 !important;
    }
    
    /* Chat message styling */
    [data-testid="stChatMessage"] {
        background-color: rgba(255, 255, 255, 0.95) !important;
        border-radius: 12px;
        padding: 12px;
        margin: 8px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        border: 1px solid rgba(0,0,0,0.05);
    }
    
    /* Chat input styling */
    [data-testid="stChatInput"] {
        background-color: white !important;
    }
    
    [data-testid="stChatInput"] textarea {
        background-color: white !important;
        color: #1a1a1a !important;
        border: 1px solid #ddd !important;
    }
    
    /* HIDE SIDEBAR COMPLETELY */
    [data-testid="stSidebar"] {
        display: none !important;
    }
    
    [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
    }
    
    /* Also hide the sidebar button/toggle */
    button[kind="header"] {
        display: none !important;
    }
    
    .css-1rs6os, .css-17ziqus {
        display: none !important;
    }
    
    /* Footer logo */
    .footer-logo {
        position: fixed;
        bottom: 15px;
        right: 15px;
        z-index: 9999;
    }
    
    .footer-logo img {
        height: 50px;
        opacity: 0.85;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: white !important;
        color: #1a1a1a !important;
        border-radius: 8px;
    }
    
    details {
        background-color: white !important;
        border-radius: 8px;
        border: 1px solid #eee !important;
    }
    
    /* Hide hamburger menu and default footer */
    #MainMenu {display: none !important;}
    footer {display: none !important;}
    header {visibility: hidden !important;}
    
    /* Style the caption */
    .stCaption, small {
        color: #666 !important;
    }
    
    /* New conversation button - add at top */
    .new-convo-btn {
        position: fixed;
        top: 10px;
        right: 15px;
        z-index: 9999;
    }
</style>

<!-- Footer Logo -->
<div class="footer-logo">
    <img src="https://vedantabharati.org/wp-content/uploads/2021/01/footer-logo.jpg" alt="Vedanta Bharati">
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
# New Conversation button at top
col1, col2 = st.columns([5, 1])
with col1:
    st.title("🕉️ Dakshinaasya Darshini")
with col2:
    if st.button("🔄 New"):
        st.session_state.messages = []
        st.session_state.last_audio_len = 0
        st.session_state.voice_input = ""
        st.session_state.chat = model.start_chat(history=[]) if model else None
        st.rerun()

st.caption("Your guide in the spirit of Dakshinamurty — ask anything")

# Initialize chat
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat = model.start_chat(history=[]) if model else None
if "voice_input" not in st.session_state:
    st.session_state.voice_input = ""

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Welcome message
if not st.session_state.messages:
    with st.chat_message("assistant"):
        welcome = "🙏 Hari Om. I am here — what is on your mind?"
        st.write(welcome)
        st.session_state.messages.append({"role": "assistant", "content": welcome})

# Voice input section - auto-transcribes when recording stops
if "last_audio_len" not in st.session_state:
    st.session_state.last_audio_len = 0

with st.expander("🎤 Voice Input", expanded=False):
    st.caption("Click to record, click again to stop — transcription is automatic")
    audio = audiorecorder("🎙️ Start Recording", "⏹️ Stop Recording")

    if len(audio) > 0:
        audio_bytes = audio.export().read()
        current_len = len(audio_bytes)
        
        # Auto-transcribe when new audio is detected
        if current_len != st.session_state.last_audio_len:
            st.session_state.last_audio_len = current_len
            st.audio(audio_bytes, format="audio/wav")
            
            with st.spinner("Transcribing..."):
                transcribed_text = transcribe_audio(audio_bytes)
                if transcribed_text:
                    st.session_state.voice_input = transcribed_text
                    st.success(f"Transcribed: {transcribed_text}")
                    st.rerun()
                else:
                    st.warning("Could not understand audio. Please try again.")

# Process voice input if available
if st.session_state.voice_input:
    prompt = st.session_state.voice_input
    st.session_state.voice_input = ""  # Clear it

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

# Chat input (text)
if prompt := st.chat_input("Ask anything..."):
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
