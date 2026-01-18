
import streamlit as st
import google.generativeai as genai
import os
import speech_recognition as sr
import io
from pydub import AudioSegment
from audio_recorder_streamlit import audio_recorder

# --- Configuration ---
st.set_page_config(page_title="Dakshinaasya Darshini", page_icon="🕉️", layout="centered")

# --- Load Context & Initialize Model ---
@st.cache_resource
def setup_model():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        st.error("GEMINI_API_KEY not found. Please set it before running.")
        return None, None

    genai.configure(api_key=api_key)

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

# --- CSS Styling ---
st.markdown("""
<style>
/* Background */
.stApp {
    background: linear-gradient(rgba(255,255,255,0.88), rgba(255,255,255,0.88)), 
                url('https://www.starsai.com/wp-content/uploads/sri-dakshinamurthy.jpg');
    background-size: cover;
    background-position: center top;
    background-attachment: fixed;
}

/* Hide Streamlit defaults */
#MainMenu, footer, header {display: none !important;}
[data-testid="stSidebar"], [data-testid="stSidebarCollapsedControl"] {display: none !important;}

/* Main container */
.main .block-container {
    padding-top: 70px !important;
    padding-bottom: 100px !important;
    max-width: 800px !important;
}

/* Header */
.header {
    position: fixed;
    top: 0; left: 0; right: 0;
    background: #B8860B;
    padding: 12px 20px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 999;
}
.header-title { color: white; font-size: 1.4rem; font-weight: 600; margin: 0; }
.header-icon { color: white; font-size: 1.3rem; }

/* Welcome content */
.om { text-align: center; font-size: 4rem; color: #B8860B; margin: 20px 0; }
.welcome-title { text-align: center; font-size: 2.2rem; font-weight: 700; color: #1a1a1a; margin: 10px 0; }
.welcome-sub { text-align: center; color: #666; font-size: 1rem; margin-bottom: 30px; }
.try-label { text-align: center; color: #999; font-size: 0.9rem; margin-bottom: 15px; }
.mic-hint { text-align: center; color: #B8860B; font-size: 0.9rem; margin: 25px 0 15px 0; }

/* Suggestion buttons */
.stButton > button {
    background: transparent !important;
    border: 1.5px solid #B8860B !important;
    color: #444 !important;
    border-radius: 25px !important;
    padding: 10px 20px !important;
    font-size: 0.9rem !important;
}
.stButton > button:hover {
    background: rgba(184,134,11,0.1) !important;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background: rgba(255,255,255,0.95) !important;
    border-radius: 12px;
    padding: 12px;
    margin: 8px 0;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

/* Bottom input bar - LIGHT CREAM */
[data-testid="stBottom"] {
    background: #FAF8F3 !important;
    border-top: 1px solid #E8E4DC !important;
}

[data-testid="stChatInput"] {
    background: transparent !important;
}

[data-testid="stChatInput"] > div {
    background: transparent !important;
}

/* The actual input container */
div[data-baseweb="textarea"] {
    background: white !important;
    border: 1px solid #ccc !important;
    border-radius: 25px !important;
}

div[data-baseweb="textarea"]:focus-within {
    border-color: #B8860B !important;
    box-shadow: none !important;
}

/* Textarea itself */
[data-testid="stChatInput"] textarea {
    background: white !important;
    color: #333 !important;
}

/* Send button */
[data-testid="stChatInput"] button {
    background: #B8860B !important;
    border-radius: 50% !important;
}

[data-testid="stChatInput"] button svg {
    fill: white !important;
}

/* Audio recorder styling */
.audio-recorder-container {
    display: flex;
    justify-content: center;
    margin: 10px 0;
}
</style>

<div class="header">
    <span class="header-title">Dakshinaasya Darshini</span>
    <span class="header-icon">⚙️</span>
</div>
""", unsafe_allow_html=True)

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.chat = model.start_chat(history=[]) if model else None
if "audio_processed" not in st.session_state:
    st.session_state.audio_processed = None

# --- Helper Functions ---
def process_message(text):
    """Send message and get response"""
    if text and text.strip():
        st.session_state.messages.append({"role": "user", "content": text})
        if st.session_state.chat:
            try:
                response = st.session_state.chat.send_message(text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.session_state.messages.append({"role": "assistant", "content": f"Error: {e}"})

def transcribe_audio(audio_bytes):
    """Convert audio to text"""
    try:
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
        wav_buffer = io.BytesIO()
        audio.export(wav_buffer, format="wav")
        wav_buffer.seek(0)
        
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_buffer) as source:
            audio_data = recognizer.record(source)
            return recognizer.recognize_google(audio_data)
    except:
        return None

# --- Welcome Screen ---
if len(st.session_state.messages) == 0:
    st.markdown('<div class="om">ॐ</div>', unsafe_allow_html=True)
    st.markdown('<h1 class="welcome-title">Namaste!</h1>', unsafe_allow_html=True)
    st.markdown('<p class="welcome-sub">I am Dakshinaasya Darshini, your spiritual guide.<br>Ask me anything.</p>', unsafe_allow_html=True)
    st.markdown('<p class="try-label">Try asking:</p>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Explain Sloka 1", use_container_width=True):
            process_message("Explain Sloka 1")
            st.rerun()
    with c2:
        if st.button("What is Tat Tvam Asi?", use_container_width=True):
            process_message("What is Tat Tvam Asi?")
            st.rerun()
    
    c3, c4 = st.columns(2)
    with c3:
        if st.button("I feel anxious", use_container_width=True):
            process_message("I feel anxious")
            st.rerun()
    with c4:
        if st.button("Mirror analogy", use_container_width=True):
            process_message("Mirror analogy")
            st.rerun()
    
    st.markdown('<p class="mic-hint">🎤 Tap mic to speak or type below</p>', unsafe_allow_html=True)
    
    # Audio recorder
    audio_bytes = audio_recorder(
        text="",
        recording_color="#B8860B",
        neutral_color="#B8860B",
        icon_size="2x",
        pause_threshold=2.0
    )
    
    if audio_bytes and audio_bytes != st.session_state.audio_processed:
        st.session_state.audio_processed = audio_bytes
        text = transcribe_audio(audio_bytes)
        if text:
            process_message(f"🎤 {text}")
            st.rerun()
        else:
            st.toast("Could not understand audio", icon="⚠️")

else:
    # Show chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

# --- Chat Input ---
if prompt := st.chat_input("Type your message..."):
    process_message(prompt)
    st.rerun()

