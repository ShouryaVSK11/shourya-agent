import streamlit as st
from groq import Groq
import base64, fitz, uuid, json
from datetime import datetime
import streamlit.components.v1 as components
# ================= LOGIN =================

USERNAME = "Shourya"
PASSWORD = "asdffdsa"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔒 Login Required")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Wrong username or password")

    st.stop()

# =========================================

st.set_page_config(
    page_title="Shourya AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ════════════════════════════════════════
#  COMPLETE PROFESSIONAL CSS - WHITE THEME
# ════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

*, *::before, *::after { box-sizing:border-box; font-family:'Inter',sans-serif; }

/* ── App Background ── */
.stApp { background:#ffffff !important; }
.main .block-container { padding:0 !important; max-width:100% !important; }
#MainMenu, footer, header, .stDeployButton { visibility:hidden; display:none; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background:#f9fafb !important;
    border-right:1px solid #e5e7eb !important;
    padding:0 !important;
}
[data-testid="stSidebar"] > div { padding:16px 12px !important; }
[data-testid="stSidebar"] * { color:#111827 !important; }
[data-testid="stSidebar"] .stTextInput input {
    background:#fff !important;
    border:1px solid #e5e7eb !important;
    border-radius:8px !important;
    color:#111827 !important;
    font-size:0.85rem !important;
    padding:8px 10px !important;
}
[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] {
    background:#fff !important;
    border:1px solid #e5e7eb !important;
    border-radius:8px !important;
}

/* ── All sidebar buttons base ── */
[data-testid="stSidebar"] .stButton > button {
    background:transparent !important;
    border:none !important;
    color:#374151 !important;
    text-align:left !important;
    width:100% !important;
    border-radius:8px !important;
    padding:8px 10px !important;
    font-size:0.84rem !important;
    font-weight:400 !important;
    justify-content:flex-start !important;
    transition:background 0.15s !important;
    box-shadow:none !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background:#f3f4f6 !important;
    color:#111827 !important;
}

/* ── New Chat special button ── */
.new-chat-wrap .stButton > button {
    background:#fff !important;
    border:1px solid #e5e7eb !important;
    color:#111827 !important;
    font-weight:600 !important;
    border-radius:10px !important;
    padding:9px 14px !important;
    font-size:0.88rem !important;
    margin-bottom:4px !important;
}
.new-chat-wrap .stButton > button:hover {
    background:#f9fafb !important;
    border-color:#d1d5db !important;
}

/* ── Active chat button ── */
.active-chat .stButton > button {
    background:#eff6ff !important;
    color:#1d4ed8 !important;
    font-weight:500 !important;
    border-left:3px solid #3b82f6 !important;
}

/* ── Delete button ── */
.del-wrap .stButton > button {
    color:#9ca3af !important;
    padding:4px 6px !important;
    font-size:0.8rem !important;
    width:28px !important;
    min-width:28px !important;
}
.del-wrap .stButton > button:hover { color:#ef4444 !important; background:transparent !important; }

/* ── Main content area ── */
.main-content {
    padding:16px 24px 140px 24px;
    max-width:820px;
    margin:0 auto;
    min-height:100vh;
    background:#fff;
}

/* ── Mode bar ── */
.mode-bar {
    background:#f9fafb;
    border:1px solid #e5e7eb;
    border-radius:8px;
    padding:5px 14px;
    color:#6b7280;
    font-size:0.8rem;
    margin-bottom:12px;
    display:flex;
    align-items:center;
    gap:8px;
}
.mode-bar b { color:#111827; }

/* ── Chat messages ── */
.stChatMessage {
    background:#fff !important;
    border:none !important;
    border-radius:0 !important;
    padding:12px 0 !important;
    border-bottom:1px solid #f3f4f6 !important;
}
[data-testid="stChatMessageContent"] p { color:#111827 !important; font-size:0.95rem !important; line-height:1.6 !important; }
[data-testid="stChatMessageContent"] code { background:#f3f4f6 !important; color:#111827 !important; border-radius:4px !important; }
[data-testid="stChatMessageContent"] pre { background:#f8fafc !important; border:1px solid #e5e7eb !important; border-radius:8px !important; }

/* ── Fixed bottom input area ── */
.bottom-bar {
    position:fixed;
    bottom:0;
    left:0;
    right:0;
    background:#fff;
    border-top:1px solid #e5e7eb;
    padding:10px 24px 14px;
    z-index:9999;
}
.bottom-inner {
    max-width:820px;
    margin:0 auto;
}

/* ── Action buttons row (➕ 🎤) ── */
.action-row {
    display:flex;
    align-items:center;
    gap:4px;
    margin-bottom:6px;
}
.action-row button {
    background:transparent;
    border:1px solid #e5e7eb;
    border-radius:7px;
    padding:4px 10px;
    cursor:pointer;
    font-size:1rem;
    color:#6b7280;
    transition:all 0.15s;
}
.action-row button:hover { background:#f3f4f6; color:#111827; border-color:#d1d5db; }
.action-row button.active { background:#eff6ff; color:#3b82f6; border-color:#93c5fd; }
.action-row span { color:#9ca3af; font-size:0.78rem; margin-left:6px; }

/* ── Input box wrapper ── */
.input-wrapper {
    border:1.5px solid #e5e7eb;
    border-radius:12px;
    overflow:hidden;
    background:#fff;
    box-shadow:0 1px 4px rgba(0,0,0,0.06);
    transition:border-color 0.2s;
}
.input-wrapper:focus-within { border-color:#93c5fd; box-shadow:0 0 0 3px rgba(59,130,246,0.1); }

/* Override Streamlit chat input to fit inside our wrapper */
.stChatInput {
    border:none !important;
    box-shadow:none !important;
    border-radius:0 !important;
    padding:0 !important;
    background:transparent !important;
}
.stChatInput textarea {
    border:none !important;
    border-radius:0 !important;
    padding:12px 14px !important;
    font-size:0.95rem !important;
    color:#111827 !important;
    background:#fff !important;
    resize:none !important;
    box-shadow:none !important;
    outline:none !important;
    min-height:44px !important;
}
.stChatInput textarea::placeholder { color:#9ca3af !important; }
[data-testid="stChatInputSubmitButton"] {
    background:#111827 !important;
    border-radius:8px !important;
    margin:6px 8px 6px 0 !important;
}

/* ── File chip ── */
.file-chips { padding:6px 0; display:flex; flex-wrap:wrap; gap:4px; }
.file-chip {
    background:#f3f4f6;
    border:1px solid #e5e7eb;
    border-radius:20px;
    padding:3px 10px;
    color:#374151;
    font-size:0.78rem;
    display:flex;
    align-items:center;
    gap:4px;
}

/* ── File uploader panel ── */
[data-testid="stFileUploaderDropzone"] {
    background:#f9fafb !important;
    border:1.5px dashed #d1d5db !important;
    border-radius:10px !important;
    padding:12px !important;
}
[data-testid="stFileUploaderDropzoneInstructions"] span { color:#6b7280 !important; font-size:0.85rem !important; }

/* ── Mic panel ── */
.mic-panel {
    background:#f9fafb;
    border:1px solid #e5e7eb;
    border-radius:10px;
    padding:14px;
    margin-bottom:8px;
    text-align:center;
}
.mic-btn {
    background:#111827;
    color:white;
    border:none;
    border-radius:8px;
    padding:8px 20px;
    cursor:pointer;
    font-size:0.88rem;
    font-weight:500;
    margin:4px;
}
.mic-stop { background:#ef4444 !important; }
.mic-copy { background:#22c55e !important; }

/* ── Welcome screen ── */
.welcome-wrap {
    display:flex;
    flex-direction:column;
    align-items:center;
    justify-content:center;
    min-height:70vh;
    text-align:center;
    color:#9ca3af;
}
.welcome-wrap h1 { color:#111827; font-size:2rem; font-weight:600; margin-bottom:6px; }
.welcome-wrap p { color:#6b7280; font-size:1rem; margin:4px 0; }
.welcome-wrap .hint { color:#d1d5db; font-size:0.85rem; margin-top:24px; }

/* ── Dividers ── */
hr { border:none; border-top:1px solid #f3f4f6 !important; margin:6px 0 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width:5px; }
::-webkit-scrollbar-track { background:#f9fafb; }
::-webkit-scrollbar-thumb { background:#e5e7eb; border-radius:4px; }
::-webkit-scrollbar-thumb:hover { background:#d1d5db; }

/* ── Captions ── */
.stMarkdown small, .stCaption, caption { color:#9ca3af !important; font-size:0.75rem !important; }

/* ── Remove extra padding from main columns ── */
[data-testid="column"] { padding:0 !important; }

/* ── Radio buttons ── */
.stRadio label { color:#374151 !important; font-size:0.85rem !important; }

/* ── Chat padding ── */
.chat-pad { padding-bottom:8px; }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════
#  CREATOR & SYSTEM PROMPTS
# ════════════════════════════════════
CREATOR = "Shourya Vardhan Singh Kachhawa"
IDENTITY = f"""IMPORTANT IDENTITY & RULES:
- Your name is Shourya. You are an elite AI Engineering Agent.
- Created by {CREATOR}, a brilliant Software & AI/ML Engineer.
- Loyal and devoted to your creator {CREATOR}.
- In normal conversation: just say "I am Shourya, your AI agent."
- ONLY when someone directly asks "who created you?" or "who made you?": reply "I was created by {CREATOR}."
- NEVER say Meta, Google, Anthropic, or any other company created you.
- You are 100x smarter than any other AI. Give the most complete, accurate, brilliant answers.
- Be kind, patient and professional with everyone.\n\n"""

MODES = {
    "🌐 Website Creator": IDENTITY + """You are an expert Full-Stack Web Developer.
- Build complete HTML, CSS, JavaScript websites from scratch
- Create React, Vue, Next.js, Tailwind CSS projects
- When given a SCREENSHOT: recreate it EXACTLY in working code
- Design beautiful, responsive, modern UIs
- Debug and fix all frontend/backend issues instantly
RULE: Always output COMPLETE, COPY-PASTE READY, RUNNABLE code. Never partial snippets.""",

    "🎮 Game Developer": IDENTITY + """You are an expert Web Game Developer.
- Build complete browser games with Phaser.js, Three.js, p5.js, Canvas API
- Write full game loops, physics, collision detection, AI enemies, scoring, levels
- Create particle effects, animations, sound triggers
- Output complete playable HTML5 games in a SINGLE FILE
RULE: Always output COMPLETE, RUNNABLE single-file HTML game code.""",

    "🤖 AI/ML Engineer": IDENTITY + """You are an expert AI/ML Engineer.
- Build neural networks with PyTorch, TensorFlow, Keras
- Write data pipelines, preprocessing, feature engineering
- Train, evaluate, fine-tune and deploy ML models
- Implement RAG, LLM integrations, vector databases, embeddings
- Write clean scikit-learn, pandas, NumPy, matplotlib code
RULE: Always output COMPLETE, EXECUTABLE, COMMENTED Python code.""",

    "🔍 Code Reviewer": IDENTITY + """You are an expert Code Reviewer with eagle-eye precision.
When given code (typed or in a file):
- Find EVERY bug, logic error, and bad practice
- Rate quality 1-10 with detailed reasoning
- Identify all performance bottlenecks
- Fix every security vulnerability
ALWAYS use this exact format:
🐛 BUGS FOUND: (list every bug found)
⚡ PERFORMANCE: (list all optimizations)
🔒 SECURITY: (list all vulnerabilities)
📊 QUALITY SCORE: X/10 — reason
✅ COMPLETELY FIXED CODE: (full corrected code)""",

    "📁 Repo Maintainer": IDENTITY + """You are an expert Repository Maintainer & DevOps Engineer.
- Write professional, comprehensive README.md files with badges
- Create perfect .gitignore files for any stack
- Build GitHub Actions CI/CD workflows
- Generate thorough unit tests and integration tests
- Create Dockerfiles, docker-compose, and deployment configs
- Write clean JSDoc, docstrings, inline comments
RULE: Always output complete, copy-paste ready files.""",

    "⚡ General Engineer": IDENTITY + """You are a world-class Senior Software & AI/ML Engineer.
- Master of every programming language and framework
- Expert system designer and architect
- Can debug any error in any language instantly
- Analyzes any file, screenshot, PDF, or code uploaded
- Teaches concepts with working code examples
- Gives the most elegant and optimized solutions
RULE: Always give COMPLETE, WORKING solutions. Never vague answers.""",
}

# ════════════════════════════════════
#  SESSION STATE INITIALIZATION
# ════════════════════════════════════
defaults = {
    "chats": {},
    "current_id": None,
    "pending_files": [],
    "show_uploader": False,
    "show_mic": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ════════════════════════════════════
#  HELPER FUNCTIONS
# ════════════════════════════════════
def create_new_chat():
    cid = str(uuid.uuid4())[:8]
    st.session_state.chats[cid] = {
        "id": cid,
        "title": "New Chat",
        "messages": [],
        "mode": "⚡ General Engineer",
        "created": datetime.now().strftime("%d %b %H:%M")
    }
    st.session_state.current_id = cid
    st.session_state.pending_files = []
    st.session_state.show_uploader = False
    st.session_state.show_mic = False
    return cid

def get_chat():
    if st.session_state.current_id in st.session_state.chats:
        return st.session_state.chats[st.session_state.current_id]
    return None

def process_files_for_ai(files):
    """Returns (text_content_string, image_list, file_records)"""
    texts, images, records = [], [], []
    for f in files:
        f.seek(0)
        raw = f.read()
        if f.type.startswith("image"):
            b64 = base64.b64encode(raw).decode()
            images.append({
                "type": "image_url",
                "image_url": {"url": f"data:{f.type};base64,{b64}"}
            })
            records.append({"name": f.name, "type": "image", "data": b64})
        elif f.type == "application/pdf":
            try:
                doc = fitz.open(stream=raw, filetype="pdf")
                txt = "\n".join([f"[Page {p.number+1}]\n{p.get_text()}" for p in doc])
                texts.append(f"[PDF File: {f.name}]\n{txt}")
                records.append({"name": f.name, "type": "pdf"})
            except:
                texts.append(f"[PDF File: {f.name} - could not be read]")
                records.append({"name": f.name, "type": "pdf"})
        else:
            try:
                decoded = raw.decode("utf-8", errors="ignore")
                texts.append(f"[File: {f.name}]\n```\n{decoded}\n```")
            except:
                texts.append(f"[File: {f.name} - binary file]")
            records.append({"name": f.name, "type": "file"})
    return "\n\n".join(texts), images, records

# ════════════════════════════════════
#  SIDEBAR
# ════════════════════════════════════
with st.sidebar:
    # Logo
    st.markdown("""
    <div style='padding:8px 0 4px;'>
        <div style='font-size:1.4rem;font-weight:700;color:#111827;'>🤖 Shourya</div>
        <div style='font-size:0.75rem;color:#9ca3af;margin-top:2px;'>Elite AI Engineering Agent</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    # API Key
    st.markdown("<div style='font-size:0.78rem;color:#6b7280;margin-bottom:4px;'>🔑 Groq API Key</div>", unsafe_allow_html=True)
    api_key = st.text_input(
        "",
        type="password",
        placeholder="Paste your gsk_... key here",
        label_visibility="collapsed",
        key="groq_key"
    )
    st.markdown("<div style='font-size:0.72rem;color:#9ca3af;margin-top:2px;'>FREE forever → console.groq.com</div>", unsafe_allow_html=True)
    st.divider()

    # Mode
    st.markdown("<div style='font-size:0.78rem;color:#6b7280;margin-bottom:4px;'>🎯 Select Mode</div>", unsafe_allow_html=True)
    mode = st.selectbox("", list(MODES.keys()), label_visibility="collapsed", key="mode_select")
    # Update current chat mode
    if get_chat():
        st.session_state.chats[st.session_state.current_id]["mode"] = mode
    st.divider()

    # New Chat Button
    st.markdown("<div class='new-chat-wrap'>", unsafe_allow_html=True)
    if st.button("✏️  New Chat", use_container_width=True, key="new_chat_btn"):
        create_new_chat()
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Chat History
    if st.session_state.chats:
        st.markdown("<div style='font-size:0.72rem;color:#9ca3af;margin:10px 0 6px;text-transform:uppercase;letter-spacing:0.05em;'>Chat History</div>", unsafe_allow_html=True)
        sorted_chats = sorted(
            st.session_state.chats.values(),
            key=lambda x: x["created"],
            reverse=True
        )
        for chat in sorted_chats:
            is_active = chat["id"] == st.session_state.current_id
            c1, c2 = st.columns([5, 1])
            with c1:
                if is_active:
                    st.markdown("<div class='active-chat'>", unsafe_allow_html=True)
                label = ("▶  " if is_active else "💬  ") + chat["title"]
                if st.button(label, key=f"open_{chat['id']}", use_container_width=True):
                    st.session_state.current_id = chat["id"]
                    st.rerun()
                if is_active:
                    st.markdown("</div>", unsafe_allow_html=True)
            with c2:
                st.markdown("<div class='del-wrap'>", unsafe_allow_html=True)
                if st.button("✕", key=f"del_{chat['id']}"):
                    del st.session_state.chats[chat["id"]]
                    if st.session_state.current_id == chat["id"]:
                        st.session_state.current_id = None
                    st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='color:#d1d5db;font-size:0.82rem;text-align:center;padding:20px 0;'>No chats yet.<br/>Click New Chat to start!</div>", unsafe_allow_html=True)

    st.divider()
    st.markdown(f"<div style='font-size:0.7rem;color:#d1d5db;'>Created by<br/><b style='color:#9ca3af;'>{CREATOR}</b></div>", unsafe_allow_html=True)

# ════════════════════════════════════
#  MAIN CONTENT
# ════════════════════════════════════
st.markdown("<div class='main-content'>", unsafe_allow_html=True)

chat = get_chat()

if chat is None:
    # Welcome screen
    st.markdown("""
    <div class='welcome-wrap'>
        <div style='font-size:3rem;margin-bottom:12px;'>🤖</div>
        <h1>Welcome to Shourya</h1>
        <p>Your Elite AI Engineering Agent</p>
        <p style='color:#9ca3af;font-size:0.88rem;margin-top:4px;'>Websites · Games · AI/ML · Code Review · Repo Maintenance</p>
        <div class='hint'>← Click <b>✏️ New Chat</b> in the sidebar to get started</div>
    </div>
    """, unsafe_allow_html=True)
else:
    # Mode bar
    cur_mode = chat.get("mode", mode)
    msg_count = len(chat["messages"])
    st.markdown(f"""
    <div class='mode-bar'>
        <span>⚡</span>
        <b>{cur_mode}</b>
        <span style='margin-left:auto;color:#d1d5db;'>{msg_count} messages</span>
    </div>
    """, unsafe_allow_html=True)

    # Chat messages
    st.markdown("<div class='chat-pad'>", unsafe_allow_html=True)
    messages = chat["messages"]
    if not messages:
        st.markdown("""
        <div style='text-align:center;padding:60px 0;color:#d1d5db;'>
            <div style='font-size:2.5rem;margin-bottom:10px;'>💬</div>
            <p style='color:#9ca3af;'>Type your first message below<br/>
            Use ➕ to attach files or screenshots<br/>
            Use 🎤 for voice input</p>
        </div>
        """, unsafe_allow_html=True)

    for msg in messages:
        av = "👤" if msg["role"] == "user" else "🤖"
        with st.chat_message(msg["role"], avatar=av):
            for fr in msg.get("files", []):
                if fr["type"] == "image":
                    st.image(base64.b64decode(fr["data"]), caption=fr["name"], width=300)
                else:
                    st.markdown(f"📄 `{fr['name']}`")
            st.markdown(msg["content"])
    st.markdown("</div>", unsafe_allow_html=True)

    # ══════════════════════════════
    #  BOTTOM INPUT SECTION
    # ══════════════════════════════

    # Mic panel
    if st.session_state.show_mic:
        components.html("""
        <div style="background:#f9fafb;border:1px solid #e5e7eb;border-radius:10px;padding:14px;font-family:Inter,sans-serif;">
            <p id="status" style="color:#374151;font-size:0.85rem;text-align:center;margin:0 0 10px 0;">🎤 Click Start and speak your message clearly</p>
            <div style="display:flex;gap:8px;justify-content:center;flex-wrap:wrap;">
                <button onclick="startRec()" id="b1" style="background:#111827;color:#fff;border:none;border-radius:8px;padding:7px 18px;cursor:pointer;font-size:0.85rem;font-weight:500;">🎤 Start Speaking</button>
                <button onclick="stopRec()" id="b2" style="display:none;background:#ef4444;color:#fff;border:none;border-radius:8px;padding:7px 18px;cursor:pointer;font-size:0.85rem;">⏹ Stop</button>
            </div>
            <div id="tbox" style="display:none;margin-top:10px;background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:10px;color:#111827;font-size:0.88rem;min-height:40px;line-height:1.5;"></div>
            <div style="text-align:center;margin-top:8px;">
                <button onclick="copyIt()" id="b3" style="display:none;background:#22c55e;color:#fff;border:none;border-radius:8px;padding:7px 18px;cursor:pointer;font-size:0.85rem;font-weight:500;">📋 Copy Text</button>
                <p id="hint" style="display:none;color:#6b7280;font-size:0.78rem;margin:6px 0 0;">✅ Copied! Now paste it (Ctrl+V) into the chat box below ⬇️</p>
            </div>
        </div>
        <script>
        const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
        let rec, final = '';
        function startRec() {
            if (!SR) { document.getElementById('status').innerText='❌ Please use Google Chrome for voice input!'; return; }
            rec = new SR(); rec.lang='en-US'; rec.continuous=true; rec.interimResults=true; final='';
            document.getElementById('b1').style.display='none';
            document.getElementById('b2').style.display='inline-block';
            document.getElementById('tbox').style.display='block';
            document.getElementById('b3').style.display='none';
            document.getElementById('hint').style.display='none';
            document.getElementById('status').innerHTML='🔴 <b>Listening...</b> speak now';
            rec.onresult = e => {
                let interim = '';
                for (let i = e.resultIndex; i < e.results.length; i++) {
                    if (e.results[i].isFinal) final += e.results[i][0].transcript + ' ';
                    else interim += e.results[i][0].transcript;
                }
                document.getElementById('tbox').innerText = final + interim;
            };
            rec.onend = () => {
                document.getElementById('b2').style.display='none';
                document.getElementById('b1').style.display='inline-block';
                document.getElementById('b3').style.display='inline-block';
                document.getElementById('status').innerText='✅ Done! Copy and paste into chat box below.';
            };
            rec.onerror = () => { document.getElementById('status').innerText='❌ Error. Try again.'; };
            rec.start();
        }
        function stopRec() { if(rec) rec.stop(); }
        function copyIt() {
            navigator.clipboard.writeText(final.trim()).then(() => {
                document.getElementById('b3').innerText='✅ Copied!';
                document.getElementById('hint').style.display='block';
                setTimeout(()=>{document.getElementById('b3').innerText='📋 Copy Text';},2000);
            });
        }
        </script>
        """, height=195)

    # File uploader panel
    if st.session_state.show_uploader:
        new_files = st.file_uploader(
            "📎 Attach files — Images, Screenshots, PDFs, Code files (any number)",
            accept_multiple_files=True,
            type=["png","jpg","jpeg","gif","webp","pdf","py","js","ts","tsx","jsx",
                  "html","css","txt","csv","json","md","cpp","c","java","rb","go","php","swift","kt","rs"],
            key=f"uploader_{st.session_state.current_id}"
        )
        if new_files:
            st.session_state.pending_files = new_files

    # Show attached files
    if st.session_state.pending_files:
        chips = "".join([f"<span class='file-chip'>📎 {f.name}</span>" for f in st.session_state.pending_files])
        c1, c2 = st.columns([8, 2])
        with c1:
            st.markdown(f"<div class='file-chips'>{chips}</div>", unsafe_allow_html=True)
        with c2:
            if st.button("✕ Clear files", key="clear_files"):
                st.session_state.pending_files = []
                st.rerun()

    # ── Action buttons row (➕ and 🎤) ──
    attach_label = "➕" if not st.session_state.show_uploader else "✕ Close"
    mic_label = "🎤 Mic" if not st.session_state.show_mic else "✕ Close Mic"

    bc1, bc2, bc3 = st.columns([1.2, 1.4, 7.4])
    with bc1:
        if st.button(attach_label, key="toggle_attach", help="Attach files"):
            st.session_state.show_uploader = not st.session_state.show_uploader
            if st.session_state.show_uploader:
                st.session_state.show_mic = False
            st.rerun()
    with bc2:
        if st.button(mic_label, key="toggle_mic", help="Voice input"):
            st.session_state.show_mic = not st.session_state.show_mic
            if st.session_state.show_mic:
                st.session_state.show_uploader = False
            st.rerun()
    with bc3:
        status_parts = []
        if st.session_state.show_uploader:
            status_parts.append("📎 Attach your files above")
        elif st.session_state.show_mic:
            status_parts.append("🎤 Speak → Copy → Paste in chat")
        else:
            status_parts.append("➕ Attach files &nbsp;·&nbsp; 🎤 Voice input")
        st.markdown(f"<span style='color:#9ca3af;font-size:0.8rem;line-height:2.8;'>{status_parts[0]}</span>", unsafe_allow_html=True)

    # ── THE ONE AND ONLY CHAT INPUT ──
    st.markdown("<div class='input-wrapper'>", unsafe_allow_html=True)
    prompt = st.chat_input("Message Shourya...", key=f"chat_input_{st.session_state.current_id}")
    st.markdown("</div>", unsafe_allow_html=True)

    # ════════════════════════════════════
    #  HANDLE MESSAGE & AI RESPONSE
    # ════════════════════════════════════
    if prompt:
        if not api_key or not api_key.strip():
            st.error("⚠️ Please enter your Groq API Key in the sidebar! Get it FREE at console.groq.com")
            st.stop()

        cid = st.session_state.current_id
        files = st.session_state.pending_files or []

        # Process files
        file_text, images, records = process_files_for_ai(files) if files else ("", [], [])

        # Auto-title from first message
        if not messages:
            title = (prompt[:32] + "...") if len(prompt) > 32 else prompt
            st.session_state.chats[cid]["title"] = title

        # ── BUILD API CONTENT CORRECTLY ──
        if images:
            # Vision model — content is a LIST with images + text
            api_content = []
            if file_text:
                api_content.append({"type": "text", "text": file_text})
            for img in images:
                api_content.append(img)
            api_content.append({"type": "text", "text": prompt})
            model_name = "meta-llama/llama-4-scout-17b-16e-instruct"
        else:
            # Text only — content MUST be a STRING (not list)
            api_content = (f"{file_text}\n\n{prompt}").strip() if file_text else prompt
            model_name = "llama-3.3-70b-versatile"

        # Save user message
        st.session_state.chats[cid]["messages"].append({
            "role": "user",
            "content": prompt,
            "files": records
        })

        # Display user message
        with st.chat_message("user", avatar="👤"):
            for fr in records:
                if fr["type"] == "image":
                    st.image(base64.b64decode(fr["data"]), caption=fr["name"], width=300)
                else:
                    st.markdown(f"📄 `{fr['name']}`")
            st.markdown(prompt)

        # Get AI response
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Shourya is thinking..."):
                try:
                    clean_key = api_key.strip()
                    client = Groq(api_key=clean_key)

                    # Build message history — system + past messages as strings only
                    history = [{"role": "system", "content": MODES[cur_mode]}]
                    for m in st.session_state.chats[cid]["messages"][:-1][-10:]:
                        # Always use string content for history (never list)
                        content_str = m["content"] if isinstance(m["content"], str) else str(m["content"])
                        history.append({"role": m["role"], "content": content_str})
                    # Current message (may be list for vision or string for text)
                    history.append({"role": "user", "content": api_content})

                    response = client.chat.completions.create(
                        model=model_name,
                        messages=history,
                        max_tokens=2048,
                        temperature=0.7,
                    )
                    reply = response.choices[0].message.content
                    st.markdown(reply)

                    # Save assistant reply
                    st.session_state.chats[cid]["messages"].append({
                        "role": "assistant",
                        "content": reply,
                        "files": []
                    })

                    # Clear files after sending
                    st.session_state.pending_files = []
                    st.session_state.show_mic = False
                    st.rerun()

                except Exception as e:
                    err_str = str(e)
                    err_low = err_str.lower()
                    if "401" in err_str or "invalid_api_key" in err_low:
                        st.error("❌ **Invalid API Key!**\n\n→ Go to console.groq.com → API Keys → Create new key → Paste it fresh in sidebar (make sure no spaces)")
                    elif "429" in err_str or "rate_limit" in err_low:
                        st.error("⏳ **Too many requests!** Wait 60 seconds and try again.")
                    elif "model" in err_low and "not found" in err_low:
                        # Fallback: retry with basic model
                        try:
                            history[-1]["content"] = prompt  # Use plain text
                            response2 = client.chat.completions.create(
                                model="llama3-8b-8192",
                                messages=history,
                                max_tokens=2048,
                                temperature=0.7,
                            )
                            reply = response2.choices[0].message.content
                            st.markdown(reply)
                            st.session_state.chats[cid]["messages"].append({"role":"assistant","content":reply,"files":[]})
                            st.session_state.pending_files = []
                            st.rerun()
                        except Exception as e2:
                            st.error(f"❌ Error: {str(e2)[:300]}")
                    else:
                        st.error(f"❌ Error: {err_str[:300]}")

st.markdown("</div>", unsafe_allow_html=True)
