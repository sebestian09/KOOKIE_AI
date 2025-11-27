"""
KOOKIE - Smart AI Assistant (WEB VERSION)
Created by Sebestian - Cyber Security Student
"""

import streamlit as st
import requests
import re
from datetime import datetime

# ============================================================
# CONFIG
# ============================================================

API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = "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"
MODELS = ["meta-llama/llama-3. 2-3b-instruct:free", "mistralai/mistral-7b-instruct:free"]

# ============================================================
# PAGE SETUP
# ============================================================

st.set_page_config(
    page_title="KOOKIE - AI Assistant",
    page_icon="K",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# PROFESSIONAL DARK THEME CSS
# ============================================================

st. markdown("""
<style>
    /* Import Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    /* Global Styles */
    . stApp {
        background: linear-gradient(180deg, #0a0a0f 0%, #12101a 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0d14 0%, #13111c 100%);
        border-right: 1px solid rgba(168, 85, 247, 0.1);
    }
    
    section[data-testid="stSidebar"] . block-container {
        padding-top: 2rem;
    }
    
    /* Logo */
    .logo-container {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 8px;
    }
    
    .logo-icon {
        width: 42px;
        height: 42px;
        background: linear-gradient(135deg, #a855f7, #6366f1);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        font-weight: 700;
        color: white;
    }
    
    .logo-text {
        font-size: 24px;
        font-weight: 700;
        color: #ffffff;
        letter-spacing: -0.5px;
    }
    
    . logo-subtitle {
        color: #71717a;
        font-size: 13px;
        margin-top: -4px;
    }
    
    /* Main Title */
    . main-header {
        text-align: center;
        padding: 20px 0 30px;
    }
    
    .main-title {
        font-size: 48px;
        font-weight: 800;
        background: linear-gradient(135deg, #ffffff 0%, #a1a1aa 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 8px;
        letter-spacing: -1px;
    }
    
    .main-title . gradient {
        background: linear-gradient(135deg, #a855f7, #22d3ee);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .main-subtitle {
        color: #71717a;
        font-size: 16px;
    }
    
    /* Chat Container */
    .stChatMessage {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 12px;
    }
    
    /* Chat Input */
    .stChatInput > div {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0. 1) !important;
        border-radius: 16px !important;
    }
    
    .stChatInput > div:focus-within {
        border-color: rgba(168, 85, 247, 0.5) !important;
        box-shadow: 0 0 20px rgba(168, 85, 247, 0.1) !important;
    }
    
    .stChatInput input {
        color: #ffffff !important;
        font-size: 15px ! important;
    }
    
    .stChatInput input::placeholder {
        color: #52525b !important;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #7c3aed, #6366f1);
        color: #ffffff;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        font-size: 14px;
        padding: 12px 20px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(124, 58, 237, 0.3);
    }
    
    /* Secondary Button */
    .secondary-btn > button {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    .secondary-btn > button:hover {
        background: rgba(255, 255, 255, 0.1);
        box-shadow: none;
        transform: none;
    }
    
    /* Text Input */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0. 03) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: rgba(168, 85, 247, 0.5) !important;
    }
    
    /* Select Box */
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }
    
    /* Feature Cards */
    .feature-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 12px;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        background: rgba(255, 255, 255, 0.04);
        border-color: rgba(168, 85, 247, 0. 2);
    }
    
    .feature-icon {
        font-size: 24px;
        margin-bottom: 8px;
    }
    
    .feature-title {
        color: #ffffff;
        font-size: 15px;
        font-weight: 600;
        margin-bottom: 4px;
    }
    
    . feature-desc {
        color: #71717a;
        font-size: 13px;
    }
    
    /* Stats */
    .stat-container {
        display: flex;
        justify-content: space-around;
        padding: 20px 0;
        border-top: 1px solid rgba(255, 255, 255, 0.05);
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        margin: 20px 0;
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-number {
        font-size: 28px;
        font-weight: 800;
        background: linear-gradient(135deg, #a855f7, #6366f1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stat-label {
        color: #71717a;
        font-size: 12px;
        margin-top: 4px;
    }
    
    /* Divider */
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(168, 85, 247, 0.3), transparent);
        margin: 24px 0;
    }
    
    /* Section Title */
    .section-title {
        color: #a855f7;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 16px;
    }
    
    /* Mode Selector */
    .mode-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 8px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .mode-card:hover {
        background: rgba(124, 58, 237, 0.1);
        border-color: rgba(124, 58, 237, 0.3);
    }
    
    .mode-card.active {
        background: rgba(124, 58, 237, 0.15);
        border-color: rgba(124, 58, 237, 0.4);
    }
    
    /* Quick Actions */
    .quick-action {
        display: inline-block;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 20px;
        padding: 8px 16px;
        margin: 4px;
        color: #a1a1aa;
        font-size: 13px;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .quick-action:hover {
        background: rgba(124, 58, 237, 0.1);
        border-color: rgba(124, 58, 247, 0.3);
        color: #ffffff;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: #52525b;
        font-size: 12px;
        margin-top: 40px;
    }
    
    . footer a {
        color: #a855f7;
        text-decoration: none;
    }
    
    /* Hide Streamlit Elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: #0a0a0f;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #2a2a2a;
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #3a3a3a;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: rgba(255, 255, 255, 0.02) !important;
        border: 1px solid rgba(255, 255, 255, 0. 05) !important;
        border-radius: 12px !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: transparent;
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        color: #a1a1aa;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: rgba(124, 58, 237, 0.15);
        border-color: rgba(124, 58, 237, 0.3);
        color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_name" not in st.session_state:
    st.session_state.user_name = "Master"
if "history" not in st.session_state:
    st.session_state.history = []
if "chat_mode" not in st.session_state:
    st.session_state.chat_mode = "General"
if "total_messages" not in st.session_state:
    st.session_state.total_messages = 0

# ============================================================
# AI ENGINE
# ============================================================

def get_system_prompt():
    user = st.session_state.user_name
    mode = st.session_state.chat_mode
    
    base_prompt = f"""You are KOOKIE, a smart and professional AI assistant created by Sebestian, a Cyber Security student. 

User's Name: {user}
Current Mode: {mode}

Your Personality:
- Professional yet friendly
- Knowledgeable and helpful
- Clear and concise responses
- Confident with a touch of warmth

Rules:
- Address the user as {user}
- Be conversational and natural
- Provide accurate information
- Keep responses well-formatted
- Use markdown for code blocks"""

    mode_prompts = {
        "General": "\n\nYou are in General mode. Help with any questions or tasks.",
        "Code Helper": "\n\nYou are in Code Helper mode. Focus on programming help, debugging, and code explanations.  Always provide code examples when relevant.",
        "Creative": "\n\nYou are in Creative mode. Help with creative writing, ideas, stories, and artistic content. Be more expressive and imaginative.",
        "Study Buddy": "\n\nYou are in Study Buddy mode. Help with learning, explaining concepts, and educational content. Break down complex topics simply.",
        "Cyber Security": "\n\nYou are in Cyber Security mode. Focus on security topics, ethical hacking concepts, network security, and best practices. Provide security-focused advice."
    }
    
    return base_prompt + mode_prompts.get(mode, "")

def ai_chat(message):
    user = st.session_state.user_name
    
    messages = [{"role": "system", "content": get_system_prompt()}]
    
    for msg in st.session_state.history[-10:]:
        messages.append(msg)
    messages.append({"role": "user", "content": message})
    
    for model in MODELS:
        try:
            response = requests.post(
                API_URL,
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://kookie.streamlit.app"
                },
                json={
                    "model": model,
                    "messages": messages,
                    "max_tokens": 1000,
                    "temperature": 0.7
                },
                timeout=30
            )
            
            if response.status_code == 200:
                text = response.json()["choices"][0]["message"]["content"]. strip()
                text = re.sub(r'\[.*?\]', '', text)
                st.session_state.history.append({"role": "user", "content": message})
                st.session_state.history. append({"role": "assistant", "content": text})
                st.session_state.total_messages += 1
                return text
        except Exception as e:
            continue
    
    return f"I'm having connection issues right now, {user}. Please try again in a moment."

def process_command(text):
    cmd = text.lower().strip()
    user = st.session_state.user_name
    
    # Name change
    if "call me " in cmd:
        name = re.sub(r'[^\w\s]', '', cmd.split("call me ")[-1]). strip(). title()
        if name:
            st.session_state. user_name = name
            return f"Got it! I'll call you {name} from now on."
    
    # Time
    if any(x in cmd for x in ["what time", "time now", "current time"]):
        return f"It's currently {datetime.now().strftime('%I:%M %p')}, {user}."
    
    # Date
    if any(x in cmd for x in ["what date", "what day", "today's date"]):
        return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}."
    
    # Greetings
    if cmd in ["hi", "hello", "hey", "yo"]:
        greetings = [
            f"Hey {user}! How can I help you today?",
            f"Hello {user}! What would you like to know?",
            f"Hi there, {user}! Ready to assist you."
        ]
        import random
        return random.choice(greetings)
    
    # Help
    if cmd in ["help", "/help", "commands"]:
        return """Here's what I can do:

**Chat Modes:**
- General - All-purpose assistance
- Code Helper - Programming help
- Creative - Writing and ideas
- Study Buddy - Learning help
- Cyber Security - Security topics

**Quick Commands:**
- "call me [name]" - Change your name
- "what time" - Current time
- "what date" - Today's date
- "clear" - Clear chat history

**Tips:**
- Change modes in the sidebar
- Ask me anything! """
    
    # Clear
    if cmd in ["clear", "/clear", "clear chat"]:
        st.session_state.messages = []
        st.session_state.history = []
        return "Chat cleared! Fresh start."
    
    return None

# ============================================================
# SIDEBAR
# ============================================================

with st. sidebar:
    # Logo
    st.markdown("""
    <div class="logo-container">
        <div class="logo-icon">K</div>
        <div>
            <div class="logo-text">KOOKIE</div>
            <div class="logo-subtitle">AI Assistant</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # New Chat Button
    if st.button("New Chat", use_container_width=True, key="new_chat"):
        st.session_state.messages = []
        st.session_state.history = []
        st.rerun()
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Chat Mode Selection
    st.markdown('<p class="section-title">Chat Mode</p>', unsafe_allow_html=True)
    
    modes = {
        "General": "All-purpose assistant",
        "Code Helper": "Programming help",
        "Creative": "Writing and ideas",
        "Study Buddy": "Learning assistant",
        "Cyber Security": "Security topics"
    }
    
    selected_mode = st.selectbox(
        "Select Mode",
        options=list(modes.keys()),
        index=list(modes.keys()).index(st.session_state.chat_mode),
        label_visibility="collapsed"
    )
    
    if selected_mode != st.session_state.chat_mode:
        st.session_state.chat_mode = selected_mode
        st.rerun()
    
    st.caption(f"{modes[selected_mode]}")
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Profile Section
    st.markdown('<p class="section-title">Profile</p>', unsafe_allow_html=True)
    
    new_name = st.text_input(
        "Your Name",
        value=st. session_state.user_name,
        label_visibility="collapsed",
        placeholder="Enter your name"
    )
    
    if new_name and new_name != st.session_state.user_name:
        st.session_state.user_name = new_name. strip(). title()
        st.success(f"Name updated to {st.session_state.user_name}")
    
    st. markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Stats
    st.markdown('<p class="section-title">Session Stats</p>', unsafe_allow_html=True)
    
    col1, col2 = st. columns(2)
    with col1:
        st.metric("Messages", len(st.session_state.messages))
    with col2:
        st.metric("Mode", st.session_state.chat_mode[:3])
    
    st. markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Features
    st.markdown('<p class="section-title">Features</p>', unsafe_allow_html=True)
    
    features = [
        ("Smart AI", "Powered by advanced AI"),
        ("5 Modes", "Different chat modes"),
        ("Context", "Remembers conversation"),
        ("Fast", "Quick responses"),
        ("Secure", "Privacy focused"),
        ("Free", "No cost to use")
    ]
    
    for title, desc in features:
        st.markdown(f"""
        <div class="feature-card">
            <div class="feature-title">{title}</div>
            <div class="feature-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("""
    <div style="text-align: center; color: #52525b; font-size: 12px; padding: 10px 0;">
        Made by <span style="color: #a855f7;">Sebestian</span><br>
        Cyber Security Student
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# MAIN CONTENT
# ============================================================

# Header
st.markdown("""
<div class="main-header">
    <h1 class="main-title">KOOKIE <span class="gradient">AI</span></h1>
    <p class="main-subtitle">Your intelligent assistant for everything</p>
</div>
""", unsafe_allow_html=True)

# Quick Actions (only show if no messages)
if not st.session_state.messages:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <p style="color: #71717a; margin-bottom: 16px;">Quick suggestions to get started:</p>
    </div>
    """, unsafe_allow_html=True)
    
    suggestions = [
        "Explain quantum computing",
        "Write a Python function",
        "Help me study for exams",
        "Creative story ideas",
        "Cyber security tips"
    ]
    
    cols = st.columns(len(suggestions))
    for idx, suggestion in enumerate(suggestions):
        with cols[idx]:
            if st.button(suggestion, key=f"suggestion_{idx}", use_container_width=True):
                st.session_state. messages.append({"role": "user", "content": suggestion})
                response = ai_chat(suggestion)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Welcome message
if not st.session_state.messages:
    user = st.session_state.user_name
    mode = st.session_state.chat_mode
    welcome = f"""Hello {user}! I'm KOOKIE, your AI assistant. 

I'm currently in **{mode}** mode.  You can change modes in the sidebar.

How can I help you today?"""
    
    with st.chat_message("assistant"):
        st.markdown(welcome)
    st.session_state.messages.append({"role": "assistant", "content": welcome})

# Chat input
if prompt := st.chat_input(f"Message KOOKIE ({st.session_state.chat_mode} mode)... "):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = process_command(prompt)
            if response is None:
                response = ai_chat(prompt)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})

# Footer
st.markdown("""
<div class="footer">
    <p>KOOKIE AI - Built with care by <a href="https://github.com/sebestian09" target="_blank">Sebestian</a></p>
    <p>Cyber Security Student</p>
</div>
""", unsafe_allow_html=True)
