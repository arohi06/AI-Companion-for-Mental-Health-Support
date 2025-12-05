import streamlit as st
from src.asr import transcribe_from_microphone
from src.tts import murf_tts_synthesize
from src.agent import SupportAgent
from src.memory import ConversationMemory
from src.config import DEFAULT_LANGUAGE, MURF_VOICE_ID

# Set page config for a website-like experience
st.set_page_config(
    page_title="Voice AI Companion",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed",  # Hide sidebar by default for cleaner look
    menu_items={
        'About': "# Voice AI Companion\nA safe, supportive voice assistant for reflection and support."
    }
)

# Enhanced Custom CSS for a modern, website-like UI
st.markdown("""
    <style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        color: #333;
    }
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem 2rem;
        text-align: center;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }
    .hero-section h1 {
        font-size: 3.5rem;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    .hero-section p {
        font-size: 1.4rem;
        opacity: 0.9;
        max-width: 600px;
        margin: 0 auto;
    }
    .features {
        display: flex;
        justify-content: space-around;
        margin: 2rem 0;
        flex-wrap: wrap;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        text-align: center;
        width: 30%;
        min-width: 250px;
        margin: 1rem;
        transition: transform 0.3s ease;
    }
    .feature-card:hover {
        transform: translateY(-5px);
    }
    .feature-card h3 {
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    .interaction-section {
        background: white;
        padding: 2.5rem;
        border-radius: 15px;
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    .conversation-log {
        background: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        max-height: 400px;
        overflow-y: auto;
        border: 1px solid #dee2e6;
    }
    .footer {
        text-align: center;
        padding: 1.5rem;
        background: #e9ecef;
        border-radius: 10px;
        margin-top: 2rem;
        font-size: 0.9rem;
        color: #6c757d;
    }
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 8px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
    }
    .stAudio {
        margin-top: 1rem;
        border-radius: 8px;
    }
    .sidebar-content {
        padding: 1rem;
        background: white;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    .expander-content {
        background: #f1f3f4;
        padding: 1rem;
        border-radius: 5px;
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "memory" not in st.session_state:
    st.session_state.memory = ConversationMemory(max_turns=20)
if "agent" not in st.session_state:
    st.session_state.agent = SupportAgent(st.session_state.memory)

# Sidebar (minimal, collapsible)
with st.sidebar:
    st.markdown('<div class="sidebar-content">', unsafe_allow_html=True)
    st.header("⚙️ Settings")
    lang = st.selectbox("🎤 Language", options=["en-IN", "en-US", "hi-IN"], index=0, help="Choose your preferred language.")
    with st.expander("🔧 Advanced"):
        voice = st.text_input("Voice ID", value=MURF_VOICE_ID, help="Customize voice if needed.")
    
    # Conversation History in Sidebar
    st.subheader("📜 Conversation History")
    st.markdown('<div class="conversation-log">', unsafe_allow_html=True)
    transcript = st.session_state.memory.transcript_text()
    if transcript:
        st.text_area("", value=transcript, height=300, disabled=True, label_visibility="collapsed")
    else:
        st.info("Your conversation history will appear here.")
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Default voice if not set
if 'voice' not in locals():
    voice = MURF_VOICE_ID

# Hero Section
st.markdown("""
    <div class="hero-section">
        <h1>🎙️ Voice AI Companion</h1>
        <p>Your personal voice assistant for meaningful conversations. Speak naturally, get thoughtful responses, and reflect on life's moments.</p>
    </div>
""", unsafe_allow_html=True)

# Features Section (to make it more website-like)
st.markdown("""
    <div class="features">
        <div class="feature-card">
            <h3>🎤 Real-Time Voice</h3>
            <p>Record and transcribe your thoughts instantly with advanced speech recognition.</p>
        </div>
        <div class="feature-card">
            <h3>🗣️ Natural Responses</h3>
            <p>Receive supportive, voiced replies that feel like a real conversation.</p>
        </div>
        <div class="feature-card">
            <h3>🌍 Multilingual</h3>
            <p>Supports multiple languages for a truly inclusive experience.</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Interaction Section (now full width, no columns)
st.markdown('<div class="interaction-section">', unsafe_allow_html=True)
st.subheader("💬 Start Your Conversation")
if st.button("🎤 Record & Respond", key="record_button"):
    with st.spinner("🎧 Listening... Speak now!"):
        text = transcribe_from_microphone(language_code=lang or DEFAULT_LANGUAGE, timeout_sec=6)
    if not text:
        st.error("❌ No speech detected. Please try again or check your microphone.")
    else:
        st.success("✅ Heard you loud and clear!")
        st.markdown(f"**You:** {text}")
        with st.spinner("🤔 Thinking..."):
            reply = st.session_state.agent.respond(text)
        st.markdown(f"**Companion:** {reply}")
        
        with st.spinner("🔊 Generating voice..."):
            audio_bytes = murf_tts_synthesize(reply, voice_id=voice, audio_format="mp3")
        if audio_bytes:
            st.audio(audio_bytes, format="audio/mp3")
        else:
            st.warning("⚠️ Voice synthesis failed. Please check settings.")
st.markdown('</div>', unsafe_allow_html=True)

# Simplified Footer (removed tech mentions)
st.markdown("""
    <div class="footer">
        <p><strong>Important:</strong> This tool offers general support and reflection. It's not a substitute for professional advice. Seek help from qualified experts when needed.</p>
    </div>
""", unsafe_allow_html=True)
