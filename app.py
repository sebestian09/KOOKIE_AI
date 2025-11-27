"""
✦ KOOKIE - Smart AI Assistant (WEB VERSION)
Fixed avatar issue
"""

import streamlit as st
import requests
import re
from datetime import datetime

# ══════════════════════════════════════════════════════════════════════════════
# CONFIG
# ══════════════════════════════════════════════════════════════════════════════

API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = "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"
MODELS = ["meta-llama/llama-3. 2-3b-instruct:free", "mistralai/mistral-7b-instruct:free"]

# ══════════════════════════════════════════════════════════════════════════════
# PAGE SETUP
# ══════════════════════════════════════════════════════════════════════════════

st.set_page_config(
    page_title="KOOKIE - AI Assistant",
    page_icon="✦",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════════════════════
# DARK THEME CSS
# ══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<style>
    .stApp { background-color: #0a0a0a; }
    
    section[data-testid="stSidebar"] {
        background-color: #111111;
        border-right: 1px solid #2a2a2a;
    }
    
    .main-title {
        color: #00FFFF;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        text-shadow: 0 0 20px rgba(0,255,255,0.3);
    }
    
    .subtitle {
        color: #888888;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .sidebar-title {
        color: #00FFFF ! important;
        font-size: 1.5rem;
        font-weight: bold;
    }
    
    .stChatInput > div {
        background-color: #0a0a0a ! important;
        border: 1px solid #2a2a2a !important;
        border-radius: 24px !important;
    }
    
    .stChatInput input { color: #ffffff !important; }
    
    .stButton > button {
        background: linear-gradient(135deg, #00FFFF, #00b8b8);
        color: #000000;
        border: none;
        border-radius: 20px;
        font-weight: bold;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #00b8b8, #008888);
        box-shadow: 0 0 15px rgba(0,255,255,0.4);
    }
    
    .stTextInput > div > div > input {
        background-color: #1a1a1a !important;
        color: #ffffff !important;
        border: 1px solid #2a2a2a !important;
        border-radius: 10px !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ══════════════════════════════════════════════════════════════════════════════

if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_name" not in st.session_state:
    st.session_state.user_name = "Master"
if "history" not in st.session_state:
    st.session_state.history = []

# ══════════════════════════════════════════════════════════════════════════════
# AI ENGINE
# ══════════════════════════════════════════════════════════════════════════════

def get_prompt():
    user = st.session_state.user_name
    return f"""You are KOOKIE, a smart, witty female AI assistant with a confident personality. 

User: {user}

Personality:
- Confident and slightly playful like Grok
- Smart and knowledgeable
- Helpful and friendly
- Witty with occasional sass

Rules:
- Address user as {user}
- Be conversational
- No [brackets] in responses"""

def ai_chat(message):
    user = st.session_state.user_name
    
    messages = [{"role": "system", "content": get_prompt()}]
    for msg in st.session_state. history[-10:]:
        messages.append(msg)
    messages.append({"role": "user", "content": message})
    
    for model in MODELS:
        try:
            r = requests.post(API_URL, headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://kookie.streamlit.app"
            }, json={
                "model": model,
                "messages": messages,
                "max_tokens": 500,
                "temperature": 0.7
            }, timeout=20)
            
            if r. status_code == 200:
                text = r.json()["choices"][0]["message"]["content"]. strip()
                text = re.sub(r'\[.*?\]', '', text)
                st.session_state.history.append({"role": "user", "content": message})
                st.session_state.history. append({"role": "assistant", "content": text})
                return text
        except:
            continue
    
    return f"Connection issue, {user}. Try again!"

def process_command(text):
    c = text.lower(). strip()
    user = st.session_state.user_name
    
    if "call me " in c:
        name = re.sub(r'[^\w\s]', '', c. split("call me ")[-1]). strip(). title()
        if name:
            st.session_state.user_name = name
            return f"Got it! I'll call you {name}.  😊"
    
    if any(x in c for x in ["what time", "time now"]):
        return f"It's {datetime.now().strftime('%I:%M %p')}, {user}.  ⏰"
    
    if any(x in c for x in ["what date", "what day"]):
        return f"Today is {datetime.now().strftime('%A, %B %d')}. 📅"
    
    if c in ["hi", "hello", "hey"]:
        return f"Hey {user}! What's up? 👋"
    
    return None

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown('<p class="sidebar-title">✦ KOOKIE</p>', unsafe_allow_html=True)
    st.caption("Smart AI Assistant - Web")
    
    st.divider()
    
    if st.button("🔄 New Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.history = []
        st.rerun()
    
    st.divider()
    
    st.subheader("👤 Profile")
    new_name = st.text_input("Your Name", value=st.session_state.user_name)
    if new_name and new_name != st.session_state.user_name:
        st.session_state.user_name = new_name. strip(). title()
        st.success(f"I'll call you {st.session_state.user_name}!")
    
    st.divider()
    
    st. subheader("✨ Features")
    st.caption("💬 Smart AI Chat")
    st.caption("🧠 Remembers Context")
    st.caption("⚡ Fast Responses")
    
    st.divider()
    st.caption("Made with ❤️")

# ══════════════════════════════════════════════════════════════════════════════
# MAIN CHAT
# ══════════════════════════════════════════════════════════════════════════════

st.markdown('<h1 class="main-title">✦ KOOKIE</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Smart AI Assistant - Web Version</p>', unsafe_allow_html=True)

# Display messages (FIXED: removed custom avatar)
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Welcome message
if not st.session_state.messages:
    user = st.session_state.user_name
    welcome = f"Hey {user}! 👋 I'm KOOKIE Web.  Ask me anything!"
    with st.chat_message("assistant"):
        st.markdown(welcome)
    st.session_state. messages.append({"role": "assistant", "content": welcome})

# Chat input
if prompt := st.chat_input("Message KOOKIE... "):
    # Display user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get and display AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = process_command(prompt)
            if response is None:
                response = ai_chat(prompt)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})