"""
KOOKIE - Smart AI Assistant
Created by Sebestian - Cyber Security Student
"""

import streamlit as st
import requests
import re
import random
from datetime import datetime

# CONFIG
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = "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"
MODELS = ["meta-llama/llama-3.2-3b-instruct:free", "mistralai/mistral-7b-instruct:free"]

# PAGE SETUP
st.set_page_config(
    page_title="KOOKIE AI",
    page_icon="K",
    layout="wide",
    initial_sidebar_state="expanded"
)

# GROK-STYLE CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    . stApp {
        background-color: #09090b;
        font-family: 'Inter', sans-serif;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #09090b;
        border-right: 1px solid #1f1f23;
        width: 260px ! important;
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 1rem;
    }
    
    /* Logo */
    .logo {
        display: flex;
        align-items: center;
        gap: 10px;
        padding: 12px 16px;
        margin-bottom: 20px;
    }
    
    .logo-icon {
        width: 32px;
        height: 32px;
        background: linear-gradient(135deg, #a855f7, #6366f1);
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
        font-weight: 700;
        color: white;
    }
    
    .logo-text {
        font-size: 20px;
        font-weight: 700;
        color: #ffffff;
    }
    
    /* Sidebar Menu Items */
    .menu-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 16px;
        color: #a1a1aa;
        font-size: 14px;
        font-weight: 500;
        border-radius: 8px;
        margin: 2px 8px;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .menu-item:hover {
        background-color: #1f1f23;
        color: #ffffff;
    }
    
    .menu-item.active {
        background-color: #1f1f23;
        color: #ffffff;
    }
    
    /* Section Label */
    .section-label {
        color: #52525b;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        padding: 16px 16px 8px;
    }
    
    /* History Item */
    .history-item {
        padding: 10px 16px;
        color: #a1a1aa;
        font-size: 13px;
        border-radius: 8px;
        margin: 2px 8px;
        cursor: pointer;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        transition: all 0.2s;
    }
    
    .history-item:hover {
        background-color: #1f1f23;
        color: #ffffff;
    }
    
    /* Main Chat Area */
    .main-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 20px;
    }
    
    /* Chat Messages */
    .stChatMessage {
        background-color: transparent ! important;
        border: none !important;
        padding: 16px 0 !important;
    }
    
    [data-testid="stChatMessageContent"] {
        background-color: transparent !important;
        color: #ffffff !important;
        font-size: 15px;
        line-height: 1.6;
    }
    
    /* User message bubble */
    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) [data-testid="stChatMessageContent"] {
        background-color: #27272a !important;
        border-radius: 18px;
        padding: 12px 18px !important;
        max-width: fit-content;
        margin-left: auto;
    }
    
    /* Chat Input */
    .stChatInput {
        position: fixed;
        bottom: 0;
        left: 260px;
        right: 0;
        padding: 20px;
        background: linear-gradient(transparent, #09090b 20%);
    }
    
    .stChatInput > div {
        max-width: 800px;
        margin: 0 auto;
        background-color: #18181b ! important;
        border: 1px solid #27272a !important;
        border-radius: 24px !important;
        padding: 4px ! important;
    }
    
    .stChatInput input {
        color: #ffffff !important;
        font-size: 15px ! important;
        background: transparent !important;
    }
    
    .stChatInput input::placeholder {
        color: #52525b !important;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #27272a;
        color: #ffffff;
        border: 1px solid #3f3f46;
        border-radius: 8px;
        font-weight: 500;
        font-size: 14px;
        padding: 8px 16px;
        transition: all 0.2s;
    }
    
    .stButton > button:hover {
        background-color: #3f3f46;
        border-color: #52525b;
    }
    
    /* Primary Button */
    .primary-btn > button {
        background: linear-gradient(135deg, #7c3aed, #6366f1);
        border: none;
    }
    
    .primary-btn > button:hover {
        opacity: 0.9;
    }
    
    /* Text Input */
    .stTextInput > div > div > input {
        background-color: #18181b !important;
        color: #ffffff !important;
        border: 1px solid #27272a !important;
        border-radius: 8px !important;
    }
    
    /* Select Box */
    .stSelectbox > div > div {
        background-color: #18181b ! important;
        border: 1px solid #27272a !important;
        border-radius: 8px !important;
    }
    
    . stSelectbox > div > div > div {
        color: #ffffff !important;
    }
    
    /* Welcome Screen */
    .welcome-container {
        text-align: center;
        padding: 60px 20px;
        max-width: 600px;
        margin: 0 auto;
    }
    
    .welcome-title {
        font-size: 32px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 12px;
    }
    
    .welcome-subtitle {
        font-size: 16px;
        color: #71717a;
        margin-bottom: 40px;
    }
    
    /* Suggestion Chips */
    .suggestions {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        justify-content: center;
        margin-top: 30px;
    }
    
    .suggestion-chip {
        background-color: #18181b;
        border: 1px solid #27272a;
        border-radius: 20px;
        padding: 10px 18px;
        color: #a1a1aa;
        font-size: 14px;
        cursor: pointer;
        transition: all 0.2s;
    }
    
    .suggestion-chip:hover {
        background-color: #27272a;
        color: #ffffff;
        border-color: #3f3f46;
    }
    
    /* Mode Badge */
    .mode-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background-color: #18181b;
        border: 1px solid #27272a;
        border-radius: 20px;
        padding: 6px 14px;
        color: #a1a1aa;
        font-size: 13px;
        margin-bottom: 20px;
    }
    
    .mode-badge.active {
        background-color: rgba(124, 58, 237, 0.2);
        border-color: rgba(124, 58, 237, 0.4);
        color: #a855f7;
    }
    
    /* Divider */
    .divider {
        height: 1px;
        background-color: #1f1f23;
        margin: 16px 8px;
    }
    
    /* Footer */
    .sidebar-footer {
        position: absolute;
        bottom: 20px;
        left: 0;
        right: 0;
        padding: 16px;
        text-align: center;
    }
    
    .footer-text {
        color: #52525b;
        font-size: 11px;
    }
    
    . footer-text a {
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
    }
    
    ::-webkit-scrollbar-track {
        background: transparent;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #27272a;
        border-radius: 3px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #3f3f46;
    }
    
    /* Hide default elements */
    .stDeployButton {display: none;}
    div[data-testid="stToolbar"] {display: none;}
    div[data-testid="stDecoration"] {display: none;}
    div[data-testid="stStatusWidget"] {display: none;}
</style>
""", unsafe_allow_html=True)

# SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = []
if "user_name" not in st.session_state:
    st.session_state.user_name = "User"
if "history" not in st.session_state:
    st.session_state.history = []
if "chat_mode" not in st.session_state:
    st.session_state.chat_mode = "General"
if "chat_history_list" not in st.session_state:
    st.session_state.chat_history_list = []

# AI FUNCTIONS
def get_system_prompt():
    user = st.session_state.user_name
    mode = st.session_state.chat_mode
    
    base = f"""You are KOOKIE, a witty and intelligent AI assistant created by Sebestian, a Cyber Security student. 

User: {user}
Mode: {mode}

Personality:
- Friendly, confident, slightly playful
- Smart and knowledgeable
- Give clear, helpful responses
- Use emojis occasionally
- Format code with markdown

Rules:
- Call user by name when appropriate
- Be conversational and natural
- Keep responses concise but complete"""

    mode_prompts = {
        "General": "\n\nHelp with any topic or question.",
        "Code": "\n\nFocus on programming.  Give code examples with explanations.",
        "Creative": "\n\nBe creative and imaginative.  Help with writing and ideas.",
        "Learn": "\n\nExplain concepts simply. Help user understand and learn.",
        "Security": "\n\nFocus on cyber security, ethical hacking, and best practices."
    }
    
    return base + mode_prompts.get(mode, "")

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
                text = re.sub(r'\[.*?\]', '', text)
                st.session_state.history.append({"role": "user", "content": message})
                st.session_state.history. append({"role": "assistant", "content": text})
                return text
        except:
            continue
    
    return f"Having connection issues.  Try again!"

def process_command(text):
    cmd = text.lower().strip()
    user = st.session_state.user_name
    
    if "call me " in cmd:
        name = re.sub(r'[^\w\s]', '', cmd.split("call me ")[-1]). strip(). title()
        if name:
            st.session_state.user_name = name
            return f"Got it! I'll call you {name} from now on."
    
    if any(x in cmd for x in ["what time", "time now", "current time"]):
        return f"It's {datetime.now().strftime('%I:%M %p')} right now."
    
    if any(x in cmd for x in ["what date", "what day", "today"]):
        return f"Today is {datetime.now().strftime('%A, %B %d, %Y')}."
    
    if cmd in ["hi", "hello", "hey", "yo"]:
        responses = [
            f"Hey!  What's up? 😊",
            f"Hello {user}! How can I help? ",
            f"Hey there! Ready when you are.",
            f"Hi!  What would you like to know?"
        ]
        return random. choice(responses)
    
    if cmd in ["help", "commands", "/help"]:
        return """Here's what I can do:

**Modes:** General, Code, Creative, Learn, Security

**Commands:**
- `call me [name]` - Set your name
- `what time` - Current time
- `what date` - Today's date

Just ask me anything! """
    
    return None

# SIDEBAR
with st.sidebar:
    # Logo
    st.markdown("""
    <div class="logo">
        <div class="logo-icon">K</div>
        <span class="logo-text">KOOKIE</span>
    </div>
    """, unsafe_allow_html=True)
    
    # New Chat Button
    if st.button("+ New Chat", use_container_width=True, key="new_chat"):
        if st.session_state.messages:
            first_msg = st.session_state.messages[0]["content"][:30] + "..."
            st. session_state.chat_history_list.insert(0, first_msg)
        st.session_state.messages = []
        st.session_state.history = []
        st.rerun()
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Mode Selection
    st.markdown('<div class="section-label">Mode</div>', unsafe_allow_html=True)
    
    modes = ["General", "Code", "Creative", "Learn", "Security"]
    selected_mode = st.selectbox(
        "Select Mode",
        options=modes,
        index=modes.index(st.session_state.chat_mode),
        label_visibility="collapsed"
    )
    
    if selected_mode != st.session_state.chat_mode:
        st.session_state.chat_mode = selected_mode
        st.rerun()
    
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # History
    st.markdown('<div class="section-label">History</div>', unsafe_allow_html=True)
    
    if st.session_state.chat_history_list:
        for i, item in enumerate(st.session_state.chat_history_list[:5]):
            st.markdown(f'<div class="history-item">{item}</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="history-item" style="color:#3f3f46;">No history yet</div>', unsafe_allow_html=True)
    
    st. markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Profile
    st.markdown('<div class="section-label">Profile</div>', unsafe_allow_html=True)
    
    new_name = st.text_input(
        "Your Name",
        value=st. session_state.user_name,
        label_visibility="collapsed",
        placeholder="Enter your name"
    )
    
    if new_name and new_name != st.session_state.user_name:
        st.session_state.user_name = new_name. strip(). title()
    
    # Footer
    st.markdown("""
    <div style="position:fixed; bottom:20px; width:220px; text-align:center;">
        <p style="color:#52525b; font-size:11px;">
            Made by <a href="https://github.com/sebestian09" style="color:#a855f7; text-decoration:none;">Sebestian</a><br>
            Cyber Security Student
        </p>
    </div>
    """, unsafe_allow_html=True)

# MAIN CONTENT
if not st.session_state.messages:
    # Welcome Screen
    st.markdown(f"""
    <div class="welcome-container">
        <h1 class="welcome-title">What can I help with?</h1>
        <p class="welcome-subtitle">I'm KOOKIE, your AI assistant.  Ask me anything!</p>
        <div class="mode-badge active">
            Mode: {st.session_state. chat_mode}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Suggestion Buttons
    suggestions = [
        "Explain quantum computing",
        "Write Python code",
        "Help me study",
        "Creative story idea",
        "Cyber security tips"
    ]
    
    cols = st.columns(5)
    for i, suggestion in enumerate(suggestions):
        with cols[i]:
            if st. button(suggestion, key=f"sug_{i}", use_container_width=True):
                st.session_state. messages.append({"role": "user", "content": suggestion})
                response = ai_chat(suggestion)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

# Display Messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat Input
if prompt := st.chat_input(f"How can KOOKIE help? "):
    # Add user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Get response
    with st.chat_message("assistant"):
        with st.spinner(""):
            response = process_command(prompt)
            if response is None:
                response = ai_chat(prompt)
            st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
