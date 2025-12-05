import streamlit as st
from src.asr import transcribe_from_microphone
from src.tts import murf_tts_synthesize
from src.agent import SupportAgent
from src.memory import ConversationMemory
from src.config import DEFAULT_LANGUAGE, MURF_VOICE_ID

# Set page config
st.set_page_config(
    page_title="Voice AI Companion",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "# Voice AI Companion\nA safe, supportive voice assistant for reflection and support."
    }
)

# Custom CSS: Added subtle aesthetic background (light gradient), kept ChatGPT-like white theme
st.markdown("""
    <style>
    /* Added aesthetic background: subtle light gradient for depth */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stVerticalBlock"] {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%) !important;  /* Light gray gradient */
        color: #000000 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    .main .block-container {
        background: transparent !important;
        padding: 0 !important;
        max-width: none !important;
    }
    .title {
        text-align: center !important;
        font-size: 2.5rem !important;
        font-weight: 700 !important;
        color: #000000 !important;
        margin: 20px 0 !important;
        text-shadow: none !important;
    }
    .message {
        margin: 10px 0 !important;
        padding: 15px 20px !important;
        border-radius: 18px !important;
        max-width: 70% !important;
        word-wrap: break-word !important;
        position: relative !important;
        animation: slideIn 0.5s ease-out !important;
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-20px); }
        to { opacity: 1; transform: translateX(0); }
    }
    .message.user {
        background: #e3f2fd !important;  /* Light blue for user */
        color: #000000 !important;
        margin-left: auto !important;
        text-align: right !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }
    .message.assistant {
        background: #f5f5f5 !important;  /* Light gray for assistant */
        color: #000000 !important;
        margin-right: auto !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }
    .message.user::after {
        content: '' !important;
        position: absolute !important;
        bottom: -2px !important;
        right: -8px !important;
        width: 0 !important;
        height: 0 !important;
        border: 8px solid transparent !important;
        border-left-color: #e3f2fd !important;
        border-bottom: none !important;
        border-right: none !important;
    }
    .message.assistant::after {
        content: '' !important;
        position: absolute !important;
        bottom: -2px !important;
        left: -8px !important;
        width: 0 !important;
        height: 0 !important;
        border: 8px solid transparent !important;
        border-right-color: #f5f5f5 !important;
        border-bottom: none !important;
        border-left: none !important;
    }
    .input-bar {
        position: fixed !important;
        bottom: 0 !important;
        left: 0 !important;
        right: 0 !important;
        background: #ffffff !important;
        border-top: 1px solid #e0e0e0 !important;
        padding: 10px 20px !important;
        display: flex !important;
        align-items: center !important;
        gap: 10px !important;
        z-index: 1000 !important;
    }
    .input-bar .stTextInput {
        flex: 1 !important;
        margin: 0 !important;
    }
    .input-bar .stTextInput input {
        border: 1px solid #ccc !important;
        border-radius: 20px !important;
        padding: 10px 15px !important;
        font-size: 16px !important;
        width: 100% !important;
    }
    .input-bar .stButton {
        margin: 0 !important;
    }
    .input-bar .stButton>button {
        background: #10a37f !important;  /* ChatGPT green */
        color: #ffffff !important;
        border: none !important;
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        font-size: 18px !important;
        cursor: pointer !important;
        transition: all 0.3s ease !important;
    }
    .input-bar .stButton>button:hover {
        background: #0e8f6b !important;
    }
    .stAudio {
        margin: 10px 0 !important;
        border-radius: 10px !important;
    }
    .sidebar-content {
        background: #f9f9f9 !important;
        color: #000000 !important;
        padding: 20px !important;
        border-radius: 10px !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1) !important;
    }
    .conversation-log {
        background: #ffffff !important;
        padding: 15px !important;
        border-radius: 10px !important;
        max-height: 400px !important;
        overflow-y: auto !important;
        border: 1px solid #e0e0e0 !important;
        color: #000000 !important;
    }
    .footer {
        text-align: center !important;
        padding: 15px !important;
        background: #f9f9f9 !important;
        border-radius: 10px !important;
        margin: 20px auto !important;
        max-width: 900px !important;
        font-size: 0.9rem !important;
        color: #666 !important;
        margin-bottom: 80px !important;  /* Space for fixed input bar */
    }
    .stTextInput, .stSelectbox {
        background: #ffffff !important;
        border: 1px solid #ccc !important;
        border-radius: 5px !important;
        color: #000000 !important;
    }
    .stTextInput input, .stSelectbox select {
        background: transparent !important;
        color: #000000 !important;
    }
    .stExpander {
        background: #f9f9f9 !important;
        border-radius: 5px !important;
    }
    /* Ensure messages don't overlap with fixed bar */
    .message-container {
        padding-bottom: 100px !important;  /* Space for input bar */
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "memory" not in st.session_state:
    st.session_state.memory = ConversationMemory(max_turns=20)
if "agent" not in st.session_state:
    st.session_state.agent = SupportAgent(st.session_state.memory)
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.header("⚙️ Settings")
    lang = st.selectbox("🎤 Language", options=["en-IN", "en-US", "hi-IN"], index=0)
    with st.expander("🔧 Advanced"):
        voice = st.text_input("Voice ID", value=MURF_VOICE_ID) 
    st.subheader("📜 Conversation History")
    st.markdown('<div class="conversation-log">', unsafe_allow_html=True)
    transcript = st.session_state.memory.transcript_text()
    if transcript:
        st.text_area("", value=transcript, height=300, disabled=True, label_visibility="collapsed")
    else:
        st.info("Your conversation history will appear here.")
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Default voice
if 'voice' not in locals():
    voice = MURF_VOICE_ID

# Title
st.markdown('<div class="title">🎙️ Voice AI Companion</div>', unsafe_allow_html=True)

# Messages container with padding for fixed bar
st.markdown('<div class="message-container">', unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="message user">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="message assistant">{msg["content"]}</div>', unsafe_allow_html=True)
        if msg["audio"]:
            st.audio(msg["audio"], format="audio/mp3")
st.markdown('</div>', unsafe_allow_html=True)

# Fixed input bar at bottom using st.form
with st.form(key="input_form", clear_on_submit=True):
    st.markdown('<div class="input-bar">', unsafe_allow_html=True)
    col1, col2 = st.columns([10, 1])
    with col1:
        user_input = st.text_input("", placeholder="Type your message or use voice...", label_visibility="collapsed")
    with col2:
        voice_button = st.form_submit_button("🎤")
    submit_button = st.form_submit_button("Send")
    st.markdown('</div>', unsafe_allow_html=True)

# Handle form submission
if submit_button or voice_button:
    if voice_button:
        with st.spinner("🎧 Listening... Speak now!"):
            text = transcribe_from_microphone(language_code=lang or DEFAULT_LANGUAGE, timeout_sec=6)
        if text:
            user_input = text
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input, "audio": None})
        with st.spinner("🤔 Thinking..."):
            reply = st.session_state.agent.respond(user_input)
        with st.spinner("🔊 Generating voice..."):
            audio_bytes = murf_tts_synthesize(reply, voice_id=voice, audio_format="mp3")
        st.session_state.messages.append({"role": "assistant", "content": reply, "audio": audio_bytes if audio_bytes else None})
        st.rerun()

# Footer
st.markdown("""
    <div class="footer">
        <p><strong>Important:</strong> This tool offers general support and reflection. It's not a substitute for professional advice. Seek help from qualified experts when needed.</p>
    </div>
""", unsafe_allow_html=True)
