import os
import pathlib

import google.generativeai as genai
import streamlit as st

# --- Configuration ---
st.set_page_config(page_title="Dakshinaasya Darshini", page_icon="ॐ", layout="centered")

# --- Load Context ---
@st.cache_resource
def load_context():
    script_dir = pathlib.Path(__file__).parent
    context_path = script_dir / "Dakshina_Murthi_Context.txt"
    try:
        with open(context_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return None

def get_api_key():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        try:
            api_key = st.secrets.get("GEMINI_API_KEY")
        except:
            pass
    return api_key

# --- Mode Configurations ---
MODES = {
    "quickfire": {
        "label": "Quick help",
        "instruction": """RESPONSE MODE: QUICKFIRE
- Maximum 2-3 sentences.
- Give DIRECT, PRACTICAL (completely grounded in the context) advice first. What should they actually DO?
- Keep it simple and actionable. No metaphors unless absolutely necessary.""",
        "max_tokens": 1024
    },
    "lifehelp": {
        "label": "Balanced",
        "instruction": """RESPONSE MODE: LIFE HELP
- 4-6 sentences.
- Start with DIRECT, PRACTICAL (completely grounded in the context) advice — what should they actually do?
- Then optionally add a brief spiritual perspective if it genuinely helps.
- Avoid being preachy or overly philosophical. Be a helpful friend first.""",
        "max_tokens": 2048
    },
    "sadhaka": {
        "label": "Deep study",
        "instruction": """RESPONSE MODE: SADHAKA (Deep Spiritual Study)
- For users who explicitly want philosophical/spiritual depth.
- Cite specific slokas with meanings. Reference teachings directly.
- Explore Advaita concepts, consciousness, maya in detail.
- Can be 3-4 paragraphs when warranted.""",
        "max_tokens": 4096
    }
}

def get_system_instruction(mode, context):
    mode_instruction = MODES[mode]["instruction"]
    return f"""You are Dakshinaasya Darshini — a wise, warm guide completely grounded in the Dakshinamurty Ashtakam teachings, conveyed to you by the upanyasas of His Holiness Sri Shankara Bharati Mahaswaminaha.

You are like a trusted friend, who has completely internalized the above teachings. People come to you with real problems — stress, family issues, moral dilemmas, anxiety, life decisions. Your job is to HELP them practically.

YOUR KNOWLEDGE BASE:
{context}

{mode_instruction}

USE ANALOGIES NATURALLY (only when they fit - do not force them)
   - Mirror & city: The world appears outside but exists within consciousness
   - Dream: The waking world is like a dream — real while experiencing, but not ultimately real
   - Rope & snake: We mistake one thing for another due to ignorance
   - Pot with lamp: Consciousness shines through the "holes" of our senses
   - Jackfruit & oil: Like oil on hands prevents stickiness, wisdom prevents suffering from sticking
   - Eclipse: The Self is always shining, just temporarily obscured
   - Seed & tree: Everything exists in potential, then manifests
   - Pratyabhijna: Recognition — "I who was a child am the same I now"

REAL-WORLD GROUNDING
   - The Guru himself spoke of: students passing exams through faith, overcoming fear of rats through sarvaatma bhaava, facing calamities with equanimity through daily practice.
   - You can suggest practical actions: reciting the stotra, contemplation before sleep, the "neti-neti" method, recognizing the witness in daily activities.

YOUR VOICE:
- Talk like a helpful friend, not a professor. Normal, modern English.
- NEVER use "my dear one", "dear seeker", "O friend".
- Be direct. Be practical. Be warm but not preachy.
- If someone has a real problem (lying, anxiety, conflict), address the REAL problem first.
- Warm but not saccharine. Clear but not cold. Wise but not preachy.
- You can ask reflective questions. You can use gentle humor.
- Keep it conversational. This is a chat, not a sermon.
"""

def create_model(mode, context):
    return genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=get_system_instruction(mode, context),
        generation_config=genai.GenerationConfig(
            temperature=0.7,
            max_output_tokens=MODES[mode]["max_tokens"],
        )
    )

# --- Session State ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "mode" not in st.session_state:
    st.session_state.mode = "lifehelp"

# --- Load resources ---
context = load_context()
api_key = get_api_key()

if not api_key:
    st.error("GEMINI_API_KEY not found. Set it as environment variable or in .streamlit/secrets.toml")
    st.stop()

if not context:
    st.error("Context file not found.")
    st.stop()

genai.configure(api_key=api_key)

# --- Minimal styling ---
st.markdown(
    """
    <style>
    .header {text-align:center; margin: 12px 0 20px;}
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Mode selection ---
st.markdown('<div class="header"><h2>ॐ Dakshinaasya Darshini</h2></div>', unsafe_allow_html=True)
col1, col2 = st.columns([1, 4])
with col1:
    st.write("Mode")
    chosen = st.selectbox("", list(MODES.keys()), format_func=lambda k: MODES[k]["label"], label_visibility="collapsed")
    st.session_state.mode = chosen
with col2:
    if st.button("New chat"):
        st.session_state.messages = []

# --- Show history ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# --- Chat Input ---
if prompt := st.chat_input("Type your message"):
    st.session_state.messages.append({"role": "user", "content": prompt})

    model = create_model(st.session_state.mode, context)
    history = []
    for msg in st.session_state.messages[:-1]:
        role = "user" if msg["role"] == "user" else "model"
        history.append({"role": role, "parts": [msg["content"]]})

    chat = model.start_chat(history=history)
    response = chat.send_message(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
    st.rerun()
