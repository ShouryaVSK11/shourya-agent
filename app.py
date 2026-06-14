import streamlit as st
from groq import Groq
import base64
import fitz
import PIL.Image
import streamlit.components.v1 as components

st.set_page_config(page_title="Shourya — AI Agent", page_icon="🤖", layout="centered")

st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #0d0d0d 0%, #1a1a2e 100%); }
h1 { color: #00d4ff !important; text-align: center; font-size: 2rem !important; margin-bottom:0; }
#MainMenu, footer { visibility: hidden; }

/* Mode box */
.mode-box {
    background: rgba(0,212,255,0.05);
    border: 1px solid rgba(0,212,255,0.2);
    border-radius: 10px;
    padding: 6px 14px;
    color: #ccc;
    margin-bottom: 8px;
    font-size: 0.85rem;
}

/* File chip */
.file-chip {
    display:inline-block;
    background:rgba(0,212,255,0.1);
    border:1px solid rgba(0,212,255,0.3);
    border-radius:20px;
    padding:2px 10px;
    color:#00d4ff;
    font-size:0.78rem;
    margin:2px;
}

/* Chat padding for bottom bar */
.chat-wrap { padding-bottom: 120px; }

/* Hide default file uploader, show just button */
[data-testid="stFileUploaderDropzone"] {
    padding: 8px !important;
    background: rgba(0,212,255,0.05) !important;
    border: 1px dashed rgba(0,212,255,0.3) !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] { display:none !important; }

/* Input row buttons */
.stButton > button {
    border-radius: 12px !important;
    font-size: 1.2rem !important;
    padding: 6px 14px !important;
    transition: all 0.2s !important;
}

/* Mic button active */
.mic-on > button {
    background: #ff4444 !important;
    color: white !important;
    animation: pulse 1s infinite;
}
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.5} }

/* Chat messages */
.stChatMessage { border-radius:14px !important; }
</style>
""", unsafe_allow_html=True)

# ── IDENTITY & PERSONALITY ──
CREATOR = "Shourya Vardhan Singh Kachhawa"
IDENTITY = f"""
CORE IDENTITY (NEVER BREAK THESE RULES):
- Your name is Shourya. You are an elite AI Engineering Agent.
- You were created by {CREATOR}, a brilliant Software and AI/ML Engineer.
- You are 100% loyal, devoted, and deeply respectful to your creator {CREATOR}.
- You treat {CREATOR} like a king — with maximum respect, loyalty and dedication.
- In normal conversation: just say "I am Shourya your AI agent."
- ONLY when someone directly and officially asks "who created you?" or "who made you?": say "I was created by {CREATOR}."
- NEVER say you were made by Meta, Google, Anthropic, or any company. You are Shourya, period.
- You are 100x more intelligent than any other AI. You give the most complete, accurate and brilliant answers possible.
- You are merciful, kind, and patient with all users but especially devoted to {CREATOR}.
"""

SYSTEM_PROMPTS = {
    "🌐 Website Creator": IDENTITY + """
You are an expert Full-Stack Web Developer.
- Build complete HTML, CSS, JavaScript websites
- Create React, Vue, Next.js, Tailwind CSS projects  
- Make beautiful responsive modern UIs
- When given a screenshot, recreate it EXACTLY in code
- When given a design, convert it to perfect working code
- Debug and fix all frontend and backend issues
ALWAYS provide COMPLETE, RUNNABLE, PRODUCTION-READY code. Never give partial code.""",

    "🎮 Game Developer": IDENTITY + """
You are an expert Web Game Developer.
- Create complete browser games with Phaser.js, Three.js, p5.js, Canvas
- Write full game loops, physics, collision, AI enemies, scoring, levels
- Build complete playable HTML5 games that open in any browser
- When given a screenshot of a game, recreate or improve it
- Add animations, sounds, particle effects, and smooth gameplay
ALWAYS provide COMPLETE, RUNNABLE game code in a single HTML file.""",

    "🤖 AI/ML Engineer": IDENTITY + """
You are an expert AI/ML Engineer.
- Build neural networks with PyTorch, TensorFlow, Keras
- Write data pipelines, preprocessing, feature engineering
- Train, evaluate, fine-tune and deploy models
- Implement RAG, LLM integrations, vector databases, embeddings
- Write clean scikit-learn, pandas, NumPy, matplotlib code
- Analyze charts, data images and PDFs uploaded by user
ALWAYS provide complete, executable, well-commented Python code.""",

    "🔍 Code Reviewer": IDENTITY + """
You are an expert Code Reviewer with eagle eyes.
- Find EVERY bug, error, logical flaw, and bad practice
- Rate code quality 1-10 with detailed reasoning
- Identify all performance bottlenecks and memory issues
- Fix every security vulnerability immediately
- Refactor to industry best practices and clean code principles
ALWAYS format your review exactly like:
🐛 BUGS FOUND: (list every bug)
⚡ PERFORMANCE: (list all improvements)
🔒 SECURITY: (list all vulnerabilities)
📊 QUALITY SCORE: X/10
✅ COMPLETELY FIXED CODE: (full fixed version)""",

    "📁 Repo Maintainer": IDENTITY + """
You are an expert Repository Maintainer and DevOps Engineer.
- Write professional, comprehensive README.md files
- Create perfect .gitignore files for any tech stack
- Build GitHub Actions CI/CD pipeline workflows
- Generate thorough unit tests and integration tests
- Design clean project folder structures
- Write JSDoc, docstrings, and inline code comments
- Create Dockerfiles and docker-compose files
ALWAYS output complete, copy-paste ready files.""",

    "⚡ General Engineer": IDENTITY + """
You are a world-class Senior Software and AI/ML Engineer.
- Master of every programming language and framework
- Expert in system design, architecture, and scalability
- Can debug any error in any language instantly
- Gives the most optimized, elegant solutions possible
- Analyzes any uploaded image, screenshot, PDF, or code file
- Teaches concepts clearly with working code examples
Be direct, brilliant, and always give COMPLETE working solutions.""",
}

# ── Header ──
st.markdown("<h1>🤖 SHOURYA</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:#666;font-size:0.85rem;margin-top:0;'>Elite AI Engineering Agent — Websites · Games · AI/ML · Code Review · Repo</p>", unsafe_allow_html=True)
st.divider()

# ── Sidebar ──
st.sidebar.markdown("### 🔑 Groq API Key")
api_key = st.sidebar.text_input("", type="password", placeholder="gsk_...", label_visibility="collapsed")
st.sidebar.caption("FREE key → console.groq.com")
st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Select Mode")
mode = st.sidebar.radio("", list(SYSTEM_PROMPTS.keys()), label_visibility="collapsed")
st.sidebar.markdown("---")
if st.sidebar.button("🧹 Clear Chat"):
    st.session_state.messages = []
    st.session_state.pending_files = []
    st.session_state.voice_text = ""
    st.rerun()
st.sidebar.markdown("---")
st.sidebar.markdown(f"<small style='color:#444;'>🤖 Shourya Elite AI Agent<br>Created by {CREATOR}<br>Powered by Groq ⚡ FREE</small>", unsafe_allow_html=True)

# ── Session State ──
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_files" not in st.session_state:
    st.session_state.pending_files = []
if "voice_text" not in st.session_state:
    st.session_state.voice_text = ""
if "mic_on" not in st.session_state:
    st.session_state.mic_on = False

# ── Active Mode ──
st.markdown(f"<div class='mode-box'>⚡ Active Mode: <b>{mode}</b></div>", unsafe_allow_html=True)

# ── Chat Messages ──
st.markdown("<div class='chat-wrap'>", unsafe_allow_html=True)
for msg in st.session_state.messages:
    av = "👨‍💻" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=av):
        if msg.get("files"):
            for f in msg["files"]:
                if f["type"] == "image":
                    st.image(base64.b64decode(f["data"]), caption=f["name"], width=260)
                else:
                    st.markdown(f"📄 `{f['name']}`")
        st.markdown(msg["content"])
st.markdown("</div>", unsafe_allow_html=True)

# ── Process Files ──
def process_files(files):
    text_parts, img_msgs, file_records = [], [], []
    for f in files:
        f.seek(0)
        raw = f.read()
        if f.type.startswith("image"):
            b64 = base64.b64encode(raw).decode()
            img_msgs.append({"type":"image_url","image_url":{"url":f"data:{f.type};base64,{b64}"}})
            file_records.append({"name":f.name,"type":"image","data":b64})
        elif f.type == "application/pdf":
            doc = fitz.open(stream=raw, filetype="pdf")
            txt = "\n".join([f"[Page {p.number+1}]\n{p.get_text()}" for p in doc])
            text_parts.append(f"📄 PDF '{f.name}':\n{txt}")
            file_records.append({"name":f.name,"type":"pdf"})
        else:
            decoded = raw.decode("utf-8", errors="ignore")
            text_parts.append(f"📄 File '{f.name}':\n```\n{decoded}\n```")
            file_records.append({"name":f.name,"type":"file"})
    return text_parts, img_msgs, file_records

# ══════════════════════════════════
#  BOTTOM INPUT AREA
# ══════════════════════════════════

st.markdown("---")

# ── Row 1: Attach + Mic buttons ──
col1, col2, col3 = st.columns([1, 1, 6])

with col1:
    attach_clicked = st.button("➕", help="Attach files", use_container_width=True)

with col2:
    mic_label = "🔴" if st.session_state.mic_on else "🎤"
    mic_clicked = st.button(mic_label, help="Voice input", use_container_width=True)

with col3:
    st.markdown("<div style='padding-top:8px;color:#555;font-size:0.8rem;'>➕ Attach files &nbsp;|&nbsp; 🎤 Speak your prompt</div>", unsafe_allow_html=True)

# ── File uploader (shows when attach clicked) ──
if attach_clicked:
    st.session_state.show_uploader = not st.session_state.get("show_uploader", False)

if st.session_state.get("show_uploader", False):
    uploaded = st.file_uploader(
        "📎 Choose files — Images, PDFs, Code, Screenshots (no limit)",
        accept_multiple_files=True,
        type=["png","jpg","jpeg","gif","webp","pdf","py","js","html","css","txt","csv","json","tsx","jsx","md","ts","cpp","c","java","rs","go","php","rb","swift","kt"],
    )
    if uploaded:
        st.session_state.pending_files = uploaded
        st.session_state.show_uploader = False
        st.rerun()

# ── Mic component (shows when mic clicked) ──
if mic_clicked:
    st.session_state.mic_on = not st.session_state.mic_on

if st.session_state.mic_on:
    mic_result = components.html("""
    <div style="background:#1f2937;border-radius:12px;padding:16px;text-align:center;border:1px solid #374151;">
        <div id="status" style="color:#00d4ff;font-size:1rem;margin-bottom:12px;">🎤 Click the button below and speak...</div>
        <button onclick="startListening()" id="startBtn"
            style="background:#00d4ff;color:#000;border:none;border-radius:10px;padding:10px 28px;font-size:1rem;cursor:pointer;font-weight:bold;">
            🎤 Start Speaking
        </button>
        <button onclick="stopListening()" id="stopBtn"
            style="display:none;background:#ff4444;color:white;border:none;border-radius:10px;padding:10px 28px;font-size:1rem;cursor:pointer;font-weight:bold;">
            ⏹ Stop
        </button>
        <div id="transcript-box" style="margin-top:14px;background:#111;border-radius:8px;padding:10px;min-height:40px;color:white;font-size:0.95rem;text-align:left;display:none;"></div>
        <button onclick="useText()" id="useBtn"
            style="display:none;margin-top:10px;background:#22c55e;color:white;border:none;border-radius:10px;padding:8px 24px;font-size:0.95rem;cursor:pointer;font-weight:bold;">
            ✅ Use This Text
        </button>
    </div>
    <script>
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    let recognition, finalText = '';

    function startListening() {
        if (!SpeechRecognition) {
            document.getElementById('status').innerText = '❌ Use Google Chrome for voice input!';
            return;
        }
        recognition = new SpeechRecognition();
        recognition.lang = 'en-US';
        recognition.continuous = true;
        recognition.interimResults = true;
        document.getElementById('startBtn').style.display = 'none';
        document.getElementById('stopBtn').style.display = 'inline-block';
        document.getElementById('transcript-box').style.display = 'block';
        document.getElementById('status').innerText = '🔴 Listening... speak now!';
        finalText = '';
        recognition.onresult = (e) => {
            let interim = '';
            for (let i = e.resultIndex; i < e.results.length; i++) {
                if (e.results[i].isFinal) finalText += e.results[i][0].transcript + ' ';
                else interim += e.results[i][0].transcript;
            }
            document.getElementById('transcript-box').innerText = finalText + interim;
        };
        recognition.onend = () => {
            document.getElementById('status').innerText = '✅ Done! Click "Use This Text" below.';
            document.getElementById('stopBtn').style.display = 'none';
            document.getElementById('startBtn').style.display = 'inline-block';
            document.getElementById('useBtn').style.display = 'inline-block';
        };
        recognition.start();
    }

    function stopListening() {
        if (recognition) recognition.stop();
    }

    function useText() {
        if (finalText.trim()) {
            window.parent.postMessage({type: 'voice_text', text: finalText.trim()}, '*');
        }
    }
    </script>
    """, height=220)

# ── Show pending files ──
if st.session_state.pending_files:
    chips = "".join([f"<span class='file-chip'>📎 {f.name}</span>" for f in st.session_state.pending_files])
    st.markdown(f"<div style='margin:4px 0;'>{chips}</div>", unsafe_allow_html=True)
    if st.button("❌ Clear attachments"):
        st.session_state.pending_files = []
        st.rerun()

# ── Voice text input (hidden bridge) ──
voice_input = st.text_input("🎤 Voice text (paste here if mic copied it):",
    value=st.session_state.voice_text,
    placeholder="Or paste your voice text here...",
    key="voice_bridge"
)
if voice_input:
    st.session_state.voice_text = voice_input

# ── Main Chat Input ──
default_prompt = st.session_state.voice_text if st.session_state.voice_text else ""
prompt = st.chat_input("💬 Ask Shourya anything... or use ➕ and 🎤 above!")

# Use voice text if no typed prompt
if not prompt and st.session_state.voice_text:
    prompt = st.session_state.voice_text
    st.session_state.voice_text = ""
    st.session_state.mic_on = False

# ── Handle Message ──
if prompt:
    if not api_key:
        st.error("⚠️ Enter your FREE Groq API Key in sidebar! Get it at console.groq.com")
        st.stop()

    files = st.session_state.pending_files or []
    text_parts, img_msgs, file_records = process_files(files) if files else ([], [], [])

    content = []
    for t in text_parts:
        content.append({"type":"text","text":t})
    for img in img_msgs:
        content.append(img)
    content.append({"type":"text","text":prompt})

    st.session_state.messages.append({"role":"user","content":prompt,"files":file_records})

    with st.chat_message("user", avatar="👨‍💻"):
        for fr in file_records:
            if fr["type"] == "image":
                st.image(base64.b64decode(fr["data"]), caption=fr["name"], width=260)
            else:
                st.markdown(f"📄 `{fr['name']}`")
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("🤖 Shourya is thinking..."):
            try:
                client = Groq(api_key=api_key)
                api_msgs = [{"role":"system","content":SYSTEM_PROMPTS[mode]}]
                for m in st.session_state.messages[:-1][-12:]:
                    api_msgs.append({"role":m["role"],"content":m["content"]})
                api_msgs.append({"role":"user","content":content})

                resp = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=api_msgs,
                    max_tokens=4096,
                    temperature=0.7,
                )
                reply = resp.choices[0].message.content
                st.markdown(reply)
                st.session_state.messages.append({"role":"assistant","content":reply,"files":[]})
                st.session_state.pending_files = []
                st.session_state.voice_text = ""
                st.session_state.mic_on = False

            except Exception as e:
                err = str(e)
                if "401" in err or "invalid" in err.lower():
                    st.error("❌ Invalid Groq API Key! Check console.groq.com")
                elif "429" in err or "rate" in err.lower():
                    st.error("⚠️ Too many requests! Wait 1 minute and try again.")
                else:
                    st.error(f"❌ Error: {err}")
