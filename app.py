"""
KOOKIE - Smart AI Assistant (WEB VERSION)
Created by Sebestian - Cyber Security Student
"""

import streamlit as st
import requests
import re
import random
from datetime import datetime

# ============================================================
# CONFIG
# ============================================================

API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = "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"
MODELS = ["meta-llama/llama-3.2-3b-instruct:free", "mistralai/mistral-7b-instruct:free"]

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
# DARK THEME CSS
# ============================================================

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    . stApp {
        background: linear-gradient(180deg, #0a0a0f 0%, #12101a 100%);
        font-family: 'Inter', sans-serif;
    }
    
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0d14 0%, #13111c 100%);
        border-right: 1px solid rgba(168, 85, 247, 0.1);
    }
    
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
    }
    
    .logo-subtitle {
        color: #71717a;
        font-size: 13px;
    }
    
    .main-header {
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
    }
    
    .gradient {
        background: linear-gradient(135deg, #a855f7, #22d3ee);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .main-subtitle {
        color: #71717a;
        font-size: 16px;
    }
    
    .stChatInput > div {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
    }
    
    .stChatInput input {
        color: #ffffff !important;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #7c3aed, #6366f1);
        color: #ffffff;
        border: none;
        border-radius: 12px;
        font-weight: 600;
    }
    
    .stButton > button:hover {
        box-shadow: 0 10px 30px rgba(124, 58, 237, 0.3);
    }
    
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.03) !important;
        color: #ffffff !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }
    
    .stSelectbox > div > div {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
    }
    
    .feature-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 10px;
    }
    
    .feature-title {
        color: #ffffff;
        font-size: 14px;
        font-weight: 600;
    }
    
    .feature-desc {
        color: #71717a;
        font-size: 12px;
    }
    
    .custom-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(168, 85, 247, 0.3), transparent);
        margin: 20px 0;
    }
    
    . section-title {
        color: #a855f7;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 12px;
    }
    
    .footer {
        text-align: center;
        padding: 20px;
        color: #52525b;
        font-size: 12px;
    }
    
    .footer a {
        color: #a855f7;
        text-decoration: none;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
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

# ============================================================
# AI ENGINE
# ============================================================

def get_system_prompt():
    user = st.session_state.user_name
    mode = st. session_state.chat_mode
    
    base = f"""You are KOOKIE, a smart AI assistant created by Sebestian, a Cyber Security student.

User: {user}
Mode: {mode}

Personality:
- Professional and friendly
- Knowledgeable and helpful
- Clear responses
- Use markdown for code

Rules:
- Call user {user}
- Be conversational
- Provide accurate info"""

    modes = {
        "General": "\n\nHelp with any questions.",
        "Code Helper": "\n\nFocus on programming and debugging.  Give code examples.",
        "Creative": "\n\nHelp with creative writing and ideas.",
        "Study Buddy": "\n\nHelp with learning and explaining concepts.",
        "Cyber Security": "\n\nFocus on security topics and ethical hacking."
    }
    
    return base + modes.get(mode, "")

def ai_chat(message):
    user = st.session_state.user_name
    
    msgs = [{"role": "system", "content": get_system_prompt()}]
    for m in st.session_state.history[-10:]:
        msgs.append(m)
    msgs.append({"role": "user", "content": message})
    
    for model in MODELS:
        try:
            r = requests.post(
                API_URL,
                headers={
                    "Authorization": f"Bearer {API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": model,
                    "messages": msgs,
                    "max_tokens": 1000,
                    "temperature": 0.7
                },
                timeout=30
            )
            
            if r.status_code == 200:
                text = r.json()["choices"][0]["message"]["content"]. strip()
                text = re. sub(r'\[.*?\]', '', text)
                st. session_state.history.append({"role": "user", "content": message})
                st.session_state.history. append({"role": "assistant", "content": text})
                return text
        except:
            continue
    
    return f"Connection issue, {user}. Try again!"

def process_command(text):
    cmd = text.lower().strip()
    user = st.session_state.user_name
    
    if "call me " in cmd:
        name = re.sub(r'[^\w\s]', '', cmd.split("call me ")[-1]).strip(). title()
        if name:
            st.session_state.user_name = name
            return f"Got it! I'll call you {name}."
    
    if any(x in cmd for x in ["what time", "time now"]):
        return f"It's {datetime.now().strftime('%I:%M %p')}, {user}."
    
    if any(x in cmd for x in ["what date", "what day"]):
        return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}."
    
    if cmd in ["hi", "hello", "hey"]:
        return random.choice([
            f"Hey {user}! How can I help? ",
            f"Hello {user}! What's up?",
            f"Hi {user}! Ready to assist."
        ])
    
    if cmd in ["help", "commands"]:
        return """**Chat Modes:** General, Code Helper, Creative, Study Buddy, Cyber Security

**Commands:**
- "call me [name]" - Change name
- "what time" - Current time
- "what date" - Today's date
- "clear" - Clear chat"""
    
    if cmd in ["clear", "clear chat"]:
        st.session_state.messages = []
        st.session_state.history = []
        return "Chat cleared!"
    
    return None

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
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
    
    if st.button("New Chat", use_container_width=True):
        st.session_state. messages = []
        st.session_state.history = []
        st.rerun()
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    st.markdown('<p class="section-title">Chat Mode</p>', unsafe_allow_html=True)
    
    mode_list = ["General", "Code Helper", "Creative", "Study Buddy", "Cyber Security"]
    mode_desc = {
        "General": "All-purpose assistant",
        "Code Helper": "Programming help",
        "Creative": "Writing and ideas",
        "Study Buddy": "Learning assistant",
        "Cyber Security": "Security topics"
    }
    
    selected = st.selectbox(
        "Mode",
        options=mode_list,
        index=mode_list.index(st.session_state.chat_mode),
        label_visibility="collapsed"
    )
    
    if selected != st.session_state.chat_mode:
        st.session_state.chat_mode = selected
        st.rerun()
    
    st.caption(mode_desc[selected])
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    st.markdown('<p class="section-title">Profile</p>', unsafe_allow_html=True)
    
    new_name = st.text_input(
        "Name",
        value=st.session_state.user_name,
        label_visibility="collapsed"
    )
    
    if new_name and new_name != st.session_state.user_name:
        st.session_state.user_name = new_name. strip(). title()
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    st.markdown('<p class="section-title">Features</p>', unsafe_allow_html=True)
    
    for title, desc in [("Smart AI", "Advanced AI"), ("5 Modes", "Different modes"), ("Context", "Remembers chat"), ("Fast", "Quick responses"), ("Secure", "Privacy first"), ("Free", "No cost")]:
        st.markdown(f'<div class="feature-card"><div class="feature-title">{title}</div><div class="feature-desc">{desc}</div></div>', unsafe_allow_html=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    st.markdown('<div style="text-align:center;color:#52525b;font-size:12px;">Made by <span style="color:#a855f7;">Sebestian</span><br>Cyber Security Student</div>', unsafe_allow_html=True)

# ============================================================
# MAIN
# ============================================================

st.markdown('<div class="main-header"><h1 class="main-title">KOOKIE <span class="gradient">AI</span></h1><p class="main-subtitle">Your intelligent assistant</p></div>', unsafe_allow_html=True)

if not st.session_state.messages:
    cols = st.columns(5)
    suggestions = ["Explain AI", "Python code", "Study tips", "Story idea", "Security tips"]
    for i, s in enumerate(suggestions):
        with cols[i]:
            if st.button(s, key=f"sug_{i}", use_container_width=True):
                st.session_state. messages.append({"role": "user", "content": s})
                resp = ai_chat(s)
                st.session_state.messages.append({"role": "assistant", "content": resp})
                st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if not st.session_state.messages:
    welcome = f"Hello {st.session_state.user_name}! I'm KOOKIE.  Currently in **{st.session_state.chat_mode}** mode.  How can I help?"
    with st.chat_message("assistant"):
        st.markdown(welcome)
    st.session_state.messages.append({"role": "assistant", "content": welcome})

if prompt := st.chat_input(f"Message KOOKIE ({st.session_state.chat_mode})... "):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state. messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            resp = process_command(prompt)
            if resp is None:
                resp = ai_chat(prompt)
            st.markdown(resp)
    st.session_state.messages.append({"role": "assistant", "content": resp})

st.markdown('<div class="footer"><p>KOOKIE AI by <a href="https://github.com/sebestian09">Sebestian</a> - Cyber Security Student</p></div>', unsafe_allow_html=True)
