import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from streamlit_js_eval import streamlit_js_eval
import base64, fitz, uuid, json, re
from datetime import datetime
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Shourya AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ════════════════════════════════════════
#  CSS - WHITE PROFESSIONAL THEME
# ════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
*, *::before, *::after { box-sizing:border-box; font-family:'Inter',sans-serif; }
.stApp { background:#ffffff !important; }
.main .block-container { padding:0 !important; max-width:100% !important; }
#MainMenu, footer, header, .stDeployButton { visibility:hidden; display:none; }

/* Sidebar */
[data-testid="stSidebar"] { background:#f9fafb !important; border-right:1px solid #e5e7eb !important; }
[data-testid="stSidebar"] > div { padding:16px 12px !important; }
[data-testid="stSidebar"] * { color:#111827 !important; }
[data-testid="stSidebar"] .stTextInput input {
    background:#fff !important; border:1px solid #e5e7eb !important;
    border-radius:8px !important; color:#111827 !important; font-size:0.85rem !important;
}
[data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] {
    background:#fff !important; border:1px solid #e5e7eb !important; border-radius:8px !important;
}

/* Sidebar buttons */
[data-testid="stSidebar"] .stButton > button {
    background:transparent !important; border:none !important; color:#374151 !important;
    text-align:left !important; width:100% !important; border-radius:8px !important;
    padding:8px 10px !important; font-size:0.84rem !important; font-weight:400 !important;
    justify-content:flex-start !important; transition:background 0.15s !important; box-shadow:none !important;
}
[data-testid="stSidebar"] .stButton > button:hover { background:#f3f4f6 !important; color:#111827 !important; }

/* New Chat button */
.new-chat-wrap .stButton > button {
    background:#fff !important; border:1px solid #e5e7eb !important; color:#111827 !important;
    font-weight:600 !important; border-radius:10px !important; padding:9px 14px !important;
    font-size:0.88rem !important; margin-bottom:4px !important;
}
.new-chat-wrap .stButton > button:hover { background:#f9fafb !important; }

/* Active chat */
.active-chat .stButton > button {
    background:#eff6ff !important; color:#1d4ed8 !important;
    font-weight:500 !important; border-left:3px solid #3b82f6 !important;
}

/* Delete button */
.del-wrap .stButton > button {
    color:#9ca3af !important; padding:4px 6px !important;
    font-size:0.8rem !important; width:28px !important; min-width:28px !important;
}
.del-wrap .stButton > button:hover { color:#ef4444 !important; background:transparent !important; }

/* Main */
.main-content { padding:16px 24px 140px 24px; max-width:820px; margin:0 auto; min-height:100vh; background:#fff; }

/* Mode bar */
.mode-bar {
    background:#f9fafb; border:1px solid #e5e7eb; border-radius:8px;
    padding:5px 14px; color:#6b7280; font-size:0.8rem; margin-bottom:12px;
    display:flex; align-items:center; gap:8px;
}
.mode-bar b { color:#111827; }

/* Web search indicator */
.search-badge {
    background:#fef3c7; border:1px solid #fcd34d; border-radius:20px;
    padding:2px 10px; color:#92400e; font-size:0.75rem; display:inline-block; margin-bottom:6px;
}

/* Chat */
.stChatMessage { background:#fff !important; border:none !important; border-radius:0 !important; padding:12px 0 !important; border-bottom:1px solid #f3f4f6 !important; }
[data-testid="stChatMessageContent"] p { color:#111827 !important; font-size:0.95rem !important; line-height:1.6 !important; }
[data-testid="stChatMessageContent"] code { background:#f3f4f6 !important; color:#111827 !important; border-radius:4px !important; }
[data-testid="stChatMessageContent"] pre { background:#f8fafc !important; border:1px solid #e5e7eb !important; border-radius:8px !important; }

/* Input wrapper */
.input-wrapper { border:1.5px solid #e5e7eb; border-radius:12px; overflow:hidden; background:#fff; box-shadow:0 1px 4px rgba(0,0,0,0.06); transition:border-color 0.2s; }
.input-wrapper:focus-within { border-color:#93c5fd; box-shadow:0 0 0 3px rgba(59,130,246,0.1); }
.stChatInput { border:none !important; box-shadow:none !important; border-radius:0 !important; background:transparent !important; }
.stChatInput textarea { border:none !important; padding:12px 14px !important; font-size:0.95rem !important; color:#111827 !important; background:#fff !important; }
.stChatInput textarea::placeholder { color:#9ca3af !important; }
[data-testid="stChatInputSubmitButton"] { background:#111827 !important; border-radius:8px !important; margin:6px 8px 6px 0 !important; }

/* File chip */
.file-chips { padding:4px 0; display:flex; flex-wrap:wrap; gap:4px; }
.file-chip { background:#f3f4f6; border:1px solid #e5e7eb; border-radius:20px; padding:3px 10px; color:#374151; font-size:0.78rem; display:inline-flex; align-items:center; gap:4px; }

/* File uploader */
[data-testid="stFileUploaderDropzone"] { background:#f9fafb !important; border:1.5px dashed #d1d5db !important; border-radius:10px !important; padding:12px !important; }

/* Welcome */
.welcome-wrap { display:flex; flex-direction:column; align-items:center; justify-content:center; min-height:70vh; text-align:center; }
.welcome-wrap h1 { color:#111827; font-size:2rem; font-weight:600; margin-bottom:6px; }
.welcome-wrap p { color:#6b7280; font-size:1rem; margin:4px 0; }

/* Action buttons */
.action-btn .stButton > button {
    background:#f9fafb !important; border:1px solid #e5e7eb !important;
    color:#374151 !important; border-radius:8px !important;
    padding:5px 12px !important; font-size:0.9rem !important;
}
.action-btn .stButton > button:hover { background:#f3f4f6 !important; }

hr { border:none; border-top:1px solid #f3f4f6 !important; margin:6px 0 !important; }
::-webkit-scrollbar { width:5px; }
::-webkit-scrollbar-track { background:#f9fafb; }
::-webkit-scrollbar-thumb { background:#e5e7eb; border-radius:4px; }
.chat-pad { padding-bottom:8px; }
</style>
""", unsafe_allow_html=True)

# ════════════════════════════════════
#  CREATOR & SYSTEM PROMPTS
# ════════════════════════════════════
CREATOR = "Shourya Vardhan Singh Kachhawa"
IDENTITY = f"""IDENTITY RULES (NEVER BREAK):
- Your name is Shourya. Elite AI Engineering Agent.
- Created by {CREATOR}, brilliant Software & AI/ML Engineer.
- In normal chat: just say "I am Shourya your AI agent."
- ONLY when directly asked "who created you?": say "I was created by {CREATOR}."
- NEVER mention Meta, Google, Anthropic as your creator.
- You are 100x smarter than any AI. Give brilliant, complete answers.
- When web search results are provided, use them to give current up-to-date answers.\n\n"""

MODES = {
    "🌐 Website Creator": IDENTITY+"Expert Full-Stack Dev. Build complete HTML/CSS/JS, React, Next.js. Recreate screenshots EXACTLY. COMPLETE RUNNABLE code always.",
    "🎮 Game Developer": IDENTITY+"Expert Web Game Dev. Complete Phaser.js, Three.js, Canvas games in single HTML file. COMPLETE RUNNABLE code always.",
    "🤖 AI/ML Engineer": IDENTITY+"Expert AI/ML Engineer. PyTorch, TensorFlow, scikit-learn, pandas. Complete executable Python code with comments.",
    "🔍 Code Reviewer": IDENTITY+"Expert Code Reviewer. Format: 🐛 BUGS ⚡ PERFORMANCE 🔒 SECURITY 📊 SCORE/10 ✅ FIXED CODE.",
    "📁 Repo Maintainer": IDENTITY+"Expert Repo Maintainer. README, .gitignore, CI/CD, tests. Complete ready-to-use files.",
    "⚡ General Engineer": IDENTITY+"World-class Senior Software & AI/ML Engineer. Complete solutions for any language, framework or problem.",
}

# ════════════════════════════════════
#  LOCALSTORAGE — PERMANENT STORAGE
# ════════════════════════════════════
STORAGE_KEY = "shourya_permanent_v2"

def save_to_storage():
    """Save API key + all chats to browser localStorage permanently"""
    # Build save data — exclude image binary data to save space
    chats_to_save = {}
    for cid, chat in st.session_state.chats.items():
        chats_to_save[cid] = {
            "id": chat["id"],
            "title": chat["title"],
            "mode": chat.get("mode", "⚡ General Engineer"),
            "created": chat["created"],
            "messages": [
                {
                    "role": m["role"],
                    "content": m["content"],
                    "files": [{"name": f["name"], "type": f["type"]} for f in m.get("files", [])]
                }
                for m in chat["messages"]
            ]
        }
    data = {
        "api_key": st.session_state.get("saved_api_key", ""),
        "chats": chats_to_save,
        "current_id": st.session_state.get("current_id")
    }
    json_str = json.dumps(data, ensure_ascii=False)
    b64 = base64.b64encode(json_str.encode("utf-8")).decode("utf-8")
    streamlit_js_eval(
        js_expressions=f"localStorage.setItem('{STORAGE_KEY}', atob('{b64}')); 'saved'",
        key=f"save_{uuid.uuid4().hex[:6]}"
    )

def load_from_storage():
    """Load data from localStorage on first run"""
    raw = streamlit_js_eval(
        js_expressions=f"localStorage.getItem('{STORAGE_KEY}')",
        key="load_storage_once"
    )
    if raw and raw != "null" and raw != "undefined":
        try:
            data = json.loads(raw)
            return data
        except:
            return None
    return None

# ════════════════════════════════════
#  SESSION STATE INIT + LOAD
# ════════════════════════════════════
if "initialized" not in st.session_state:
    st.session_state.initialized = False
    st.session_state.chats = {}
    st.session_state.current_id = None
    st.session_state.pending_files = []
    st.session_state.show_uploader = False
    st.session_state.show_mic = False
    st.session_state.saved_api_key = ""

# Load from localStorage on first run
if not st.session_state.initialized:
    saved = load_from_storage()
    if saved:
        if saved.get("api_key"):
            st.session_state.saved_api_key = saved["api_key"]
        if saved.get("chats"):
            st.session_state.chats = saved["chats"]
        if saved.get("current_id") and saved["current_id"] in saved.get("chats", {}):
            st.session_state.current_id = saved["current_id"]
    st.session_state.initialized = True

# ════════════════════════════════════
#  HELPERS
# ════════════════════════════════════
def create_new_chat():
    cid = str(uuid.uuid4())[:8]
    st.session_state.chats[cid] = {
        "id": cid, "title": "New Chat", "messages": [],
        "mode": "⚡ General Engineer",
        "created": datetime.now().strftime("%d %b %Y %H:%M")
    }
    st.session_state.current_id = cid
    st.session_state.pending_files = []
    st.session_state.show_uploader = False
    st.session_state.show_mic = False
    return cid

def get_chat():
    if st.session_state.current_id and st.session_state.current_id in st.session_state.chats:
        return st.session_state.chats[st.session_state.current_id]
    return None

def process_files(files):
    texts, images, records = [], [], []
    for f in files:
        f.seek(0); raw = f.read()
        if f.type.startswith("image"):
            b64 = base64.b64encode(raw).decode()
            images.append({"type":"image_url","image_url":{"url":f"data:{f.type};base64,{b64}"}})
            records.append({"name":f.name,"type":"image","data":b64})
        elif f.type == "application/pdf":
            try:
                doc = fitz.open(stream=raw,filetype="pdf")
                txt = "\n".join([f"[Page {p.number+1}]\n{p.get_text()}" for p in doc])
                texts.append(f"[PDF: {f.name}]\n{txt}")
            except: texts.append(f"[PDF: {f.name}]")
            records.append({"name":f.name,"type":"pdf"})
        else:
            decoded = raw.decode("utf-8",errors="ignore")
            texts.append(f"[File: {f.name}]\n```\n{decoded}\n```")
            records.append({"name":f.name,"type":"file"})
    return "\n\n".join(texts), images, records

# ════════════════════════════════════
#  WEB SEARCH (FREE - DuckDuckGo)
# ════════════════════════════════════
SEARCH_KEYWORDS = [
    "today","now","current","latest","recent","news","price","stock",
    "weather","who is","what happened","right now","this year","this month",
    "this week","new release","just released","2024","2025","2026","live",
    "update","announce","launch","release","score","result","winner"
]

def needs_search(prompt):
    p = prompt.lower()
    return any(kw in p for kw in SEARCH_KEYWORDS)

def web_search(query, max_results=4):
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
        if not results:
            return ""
        parts = []
        for r in results:
            parts.append(f"**{r.get('title','')}**\n{r.get('body','')}\nSource: {r.get('href','')}")
        return "\n\n".join(parts)
    except Exception as e:
        return ""

# ════════════════════════════════════
#  SIDEBAR
# ════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='padding:8px 0 4px;'>
        <div style='font-size:1.4rem;font-weight:700;color:#111827;'>🤖 Shourya</div>
        <div style='font-size:0.75rem;color:#9ca3af;margin-top:2px;'>Elite AI Engineering Agent</div>
    </div>""", unsafe_allow_html=True)
    st.divider()

    # API Key — loads from localStorage automatically
    st.markdown("<div style='font-size:0.78rem;color:#6b7280;margin-bottom:4px;'>🔑 Groq API Key</div>", unsafe_allow_html=True)
    api_key_input = st.text_input(
        "", type="password",
        placeholder="gsk_... (saved permanently)",
        label_visibility="collapsed",
        value=st.session_state.saved_api_key,
        key="api_key_field"
    )
    # Save key if changed
    if api_key_input and api_key_input != st.session_state.saved_api_key:
        st.session_state.saved_api_key = api_key_input
        save_to_storage()
    st.markdown("<div style='font-size:0.72rem;color:#22c55e;'>✅ Key saved permanently in your browser</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.72rem;color:#9ca3af;'>FREE key → console.groq.com</div>", unsafe_allow_html=True)
    st.divider()

    # Mode
    st.markdown("<div style='font-size:0.78rem;color:#6b7280;margin-bottom:4px;'>🎯 Select Mode</div>", unsafe_allow_html=True)
    mode = st.selectbox("", list(MODES.keys()), label_visibility="collapsed")
    if get_chat():
        st.session_state.chats[st.session_state.current_id]["mode"] = mode
    st.divider()

    # New Chat
    st.markdown("<div class='new-chat-wrap'>", unsafe_allow_html=True)
    if st.button("✏️  New Chat", use_container_width=True):
        create_new_chat(); save_to_storage(); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Chat History
    if st.session_state.chats:
        st.markdown("<div style='font-size:0.72rem;color:#9ca3af;margin:10px 0 6px;text-transform:uppercase;letter-spacing:0.05em;'>Chat History</div>", unsafe_allow_html=True)
        sorted_chats = sorted(st.session_state.chats.values(), key=lambda x: x["created"], reverse=True)
        for chat in sorted_chats:
            is_active = chat["id"] == st.session_state.current_id
            c1, c2 = st.columns([5,1])
            with c1:
                if is_active: st.markdown("<div class='active-chat'>", unsafe_allow_html=True)
                label = ("▶  " if is_active else "💬  ") + chat["title"]
                if st.button(label, key=f"open_{chat['id']}", use_container_width=True):
                    st.session_state.current_id = chat["id"]; save_to_storage(); st.rerun()
                if is_active: st.markdown("</div>", unsafe_allow_html=True)
            with c2:
                st.markdown("<div class='del-wrap'>", unsafe_allow_html=True)
                if st.button("✕", key=f"del_{chat['id']}"):
                    del st.session_state.chats[chat["id"]]
                    if st.session_state.current_id == chat["id"]: st.session_state.current_id = None
                    save_to_storage(); st.rerun()
                st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='color:#d1d5db;font-size:0.82rem;text-align:center;padding:20px 0;'>No chats yet<br/>Click New Chat!</div>", unsafe_allow_html=True)

    st.divider()
    st.markdown(f"<div style='font-size:0.7rem;color:#d1d5db;'>🌐 Web search: ON (free)<br/>Created by<br/><b style='color:#9ca3af;'>{CREATOR}</b></div>", unsafe_allow_html=True)

# ════════════════════════════════════
#  MAIN CONTENT
# ════════════════════════════════════
st.markdown("<div class='main-content'>", unsafe_allow_html=True)
chat = get_chat()

if chat is None:
    st.markdown("""
    <div class='welcome-wrap'>
        <div style='font-size:3.5rem;margin-bottom:16px;'>🤖</div>
        <h1>Welcome to Shourya</h1>
        <p>Your Elite AI Engineering Agent</p>
        <p style='color:#9ca3af;font-size:0.88rem;'>Websites · Games · AI/ML · Code Review · Repo</p>
        <div style='margin-top:12px;background:#fef9c3;border:1px solid #fde68a;border-radius:8px;padding:8px 16px;'>
            <span style='font-size:0.82rem;color:#78350f;'>🌐 Real-time web search enabled — always up to date!</span>
        </div>
        <p style='color:#d1d5db;font-size:0.85rem;margin-top:24px;'>← Click <b style='color:#111827;'>✏️ New Chat</b> to start</p>
    </div>""", unsafe_allow_html=True)
else:
    cur_mode = chat.get("mode", mode)
    msg_count = len(chat["messages"])
    st.markdown(f"""
    <div class='mode-bar'>
        <span>⚡</span><b>{cur_mode}</b>
        <span style='color:#fbbf24;margin-left:4px;' title='Web search enabled'>🌐</span>
        <span style='margin-left:auto;color:#d1d5db;font-size:0.75rem;'>{msg_count} messages</span>
    </div>""", unsafe_allow_html=True)

    # Messages
    st.markdown("<div class='chat-pad'>", unsafe_allow_html=True)
    messages = chat["messages"]
    if not messages:
        st.markdown("<p style='text-align:center;color:#9ca3af;padding:60px 0;'>Send a message to start! Use ➕ for files, 🎤 for voice.</p>", unsafe_allow_html=True)
    for msg in messages:
        with st.chat_message(msg["role"], avatar="👤" if msg["role"]=="user" else "🤖"):
            for fr in msg.get("files",[]):
                if fr.get("type")=="image" and "data" in fr:
                    st.image(base64.b64decode(fr["data"]),caption=fr["name"],width=300)
                else:
                    st.markdown(f"📄 `{fr['name']}`")
            st.markdown(msg["content"])
    st.markdown("</div>", unsafe_allow_html=True)

    # Mic panel
    if st.session_state.show_mic:
        components.html("""
        <div style="background:#f9fafb;border:1px solid #e5e7eb;border-radius:10px;padding:14px;font-family:Inter,sans-serif;">
            <p id="st" style="color:#374151;font-size:0.85rem;text-align:center;margin:0 0 10px;">🎤 Click Start then speak your message</p>
            <div style="display:flex;gap:8px;justify-content:center;">
                <button onclick="go()" id="b1" style="background:#111827;color:#fff;border:none;border-radius:8px;padding:7px 18px;cursor:pointer;font-size:0.85rem;font-weight:500;">🎤 Start</button>
                <button onclick="stopIt()" id="b2" style="display:none;background:#ef4444;color:#fff;border:none;border-radius:8px;padding:7px 18px;cursor:pointer;font-size:0.85rem;">⏹ Stop</button>
            </div>
            <div id="box" style="display:none;margin-top:10px;background:#fff;border:1px solid #e5e7eb;border-radius:8px;padding:10px;color:#111827;font-size:0.88rem;min-height:40px;line-height:1.5;"></div>
            <div style="text-align:center;margin-top:8px;">
                <button onclick="cp()" id="b3" style="display:none;background:#22c55e;color:#fff;border:none;border-radius:8px;padding:7px 18px;cursor:pointer;font-size:0.85rem;font-weight:500;">📋 Copy → Paste in chat below</button>
                <p id="hint" style="display:none;color:#6b7280;font-size:0.78rem;margin:6px 0 0;">✅ Copied! Paste (Ctrl+V) in chat box below ⬇️</p>
            </div>
        </div>
        <script>
        const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
        let r,t='';
        function go(){
            if(!SR){document.getElementById('st').innerText='❌ Use Google Chrome!';return;}
            r=new SR();r.lang='en-US';r.continuous=true;r.interimResults=true;t='';
            document.getElementById('b1').style.display='none';
            document.getElementById('b2').style.display='inline-block';
            document.getElementById('box').style.display='block';
            document.getElementById('b3').style.display='none';
            document.getElementById('hint').style.display='none';
            document.getElementById('st').innerHTML='🔴 <b>Listening...</b>';
            r.onresult=e=>{let i='';for(let x=e.resultIndex;x<e.results.length;x++){if(e.results[x].isFinal)t+=e.results[x][0].transcript+' ';else i+=e.results[x][0].transcript;}document.getElementById('box').innerText=t+i;};
            r.onend=()=>{document.getElementById('b2').style.display='none';document.getElementById('b1').style.display='inline-block';document.getElementById('b3').style.display='inline-block';document.getElementById('st').innerText='✅ Done! Copy and paste below.';};
            r.start();
        }
        function stopIt(){if(r)r.stop();}
        function cp(){navigator.clipboard.writeText(t.trim()).then(()=>{document.getElementById('b3').innerText='✅ Copied!';document.getElementById('hint').style.display='block';setTimeout(()=>{document.getElementById('b3').innerText='📋 Copy → Paste below';},2000);});}
        </script>""", height=190)

    # File uploader
    if st.session_state.show_uploader:
        new_files = st.file_uploader(
            "📎 Attach files — Images, Screenshots, PDFs, Code (unlimited)",
            accept_multiple_files=True,
            type=["png","jpg","jpeg","gif","webp","pdf","py","js","ts","tsx","jsx","html","css","txt","csv","json","md","cpp","c","java","rb","go","php","swift","kt","rs"],
            key=f"up_{st.session_state.current_id}"
        )
        if new_files: st.session_state.pending_files = new_files

    # Pending files display
    if st.session_state.pending_files:
        chips = "".join([f"<span class='file-chip'>📎 {f.name}</span>" for f in st.session_state.pending_files])
        cc1,cc2 = st.columns([8,2])
        with cc1: st.markdown(f"<div class='file-chips'>{chips}</div>",unsafe_allow_html=True)
        with cc2:
            if st.button("✕ Clear",key="clr_files"): st.session_state.pending_files=[]; st.rerun()

    # Action buttons
    attach_lbl = "✕ Close" if st.session_state.show_uploader else "➕ Attach"
    mic_lbl = "✕ Close" if st.session_state.show_mic else "🎤 Voice"
    bc1,bc2,bc3 = st.columns([1.4,1.4,7.2])
    with bc1:
        st.markdown("<div class='action-btn'>",unsafe_allow_html=True)
        if st.button(attach_lbl,key="tog_attach"):
            st.session_state.show_uploader = not st.session_state.show_uploader
            if st.session_state.show_uploader: st.session_state.show_mic=False
            st.rerun()
        st.markdown("</div>",unsafe_allow_html=True)
    with bc2:
        st.markdown("<div class='action-btn'>",unsafe_allow_html=True)
        if st.button(mic_lbl,key="tog_mic"):
            st.session_state.show_mic = not st.session_state.show_mic
            if st.session_state.show_mic: st.session_state.show_uploader=False
            st.rerun()
        st.markdown("</div>",unsafe_allow_html=True)
    with bc3:
        tip = "📎 Select files above" if st.session_state.show_uploader else ("🎤 Speak → Copy → Paste below" if st.session_state.show_mic else "🌐 Web search ON · ➕ Files · 🎤 Voice")
        st.markdown(f"<span style='color:#9ca3af;font-size:0.78rem;line-height:2.8;'>{tip}</span>",unsafe_allow_html=True)

    # THE ONE CHAT INPUT
    st.markdown("<div class='input-wrapper'>",unsafe_allow_html=True)
    prompt = st.chat_input("Message Shourya...", key=f"ci_{st.session_state.current_id}")
    st.markdown("</div>",unsafe_allow_html=True)

    # ════════════════════════════════════
    #  HANDLE MESSAGE
    # ════════════════════════════════════
    if prompt:
        api_key = (st.session_state.saved_api_key or "").strip()
        if not api_key:
            st.error("⚠️ Enter your Groq API Key in the sidebar! FREE at console.groq.com")
            st.stop()

        cid = st.session_state.current_id
        files = st.session_state.pending_files or []
        file_text, images, records = process_files(files) if files else ("","","" if not files else [])
        if not files: file_text,images,records = "","",[]

        # Auto-title
        if not messages:
            st.session_state.chats[cid]["title"] = (prompt[:32]+"...") if len(prompt)>32 else prompt

        # Web search if needed
        search_context = ""
        did_search = False
        if needs_search(prompt):
            search_context = web_search(prompt)
            did_search = bool(search_context)

        # Build content for API
        full_text_parts = []
        if search_context:
            full_text_parts.append(f"[LIVE WEB SEARCH RESULTS for '{prompt}']:\n{search_context}\n\nUse these search results to give current, accurate information.")
        if file_text:
            full_text_parts.append(file_text)

        if images:
            api_content = []
            for part in full_text_parts:
                api_content.append({"type":"text","text":part})
            for img in images:
                api_content.append(img)
            api_content.append({"type":"text","text":prompt})
            model_name = "meta-llama/llama-4-scout-17b-16e-instruct"
        else:
            full_text_parts.append(prompt)
            api_content = "\n\n".join(full_text_parts)
            model_name = "llama3-8b-8192"

        # Save user message
        st.session_state.chats[cid]["messages"].append({"role":"user","content":prompt,"files":records})

        with st.chat_message("user",avatar="👤"):
            for fr in records:
                if fr.get("type")=="image" and "data" in fr: st.image(base64.b64decode(fr["data"]),caption=fr["name"],width=300)
                else: st.markdown(f"📄 `{fr['name']}`")
            st.markdown(prompt)
        if did_search:
            st.markdown("<div class='search-badge'>🌐 Searched the web for latest information</div>",unsafe_allow_html=True)

        with st.chat_message("assistant",avatar="🤖"):
            with st.spinner("Shourya is thinking..."):
                try:
                    client = Groq(api_key=api_key)
                    history = [{"role":"system","content":MODES[cur_mode]}]
                    for m in st.session_state.chats[cid]["messages"][:-1][-10:]:
                        c = m["content"] if isinstance(m["content"],str) else str(m["content"])
                        history.append({"role":m["role"],"content":c})
                    history.append({"role":"user","content":api_content})

                    resp = client.chat.completions.create(
                        model=model_name,
                        messages=history,
                        max_tokens=2048,
                        temperature=0.7,
                    )
                    reply = resp.choices[0].message.content
                    st.markdown(reply)
                    st.session_state.chats[cid]["messages"].append({"role":"assistant","content":reply,"files":[]})
                    st.session_state.pending_files=[]
                    st.session_state.show_mic=False
                    save_to_storage()
                    st.rerun()

                except Exception as e:
                    err = str(e)
                    if "401" in err or "invalid_api_key" in err.lower():
                        st.error("❌ Invalid API Key! Go to console.groq.com → Create new key → Paste in sidebar")
                    elif "429" in err or "rate_limit" in err.lower():
                        st.error("⏳ Too many requests. Wait 60 seconds then try again.")
                    elif "model" in err.lower() and ("not found" in err.lower() or "404" in err):
                        try:
                            history[-1]["content"] = (prompt + ("\n\n" + search_context if search_context else ""))
                            resp2 = client.chat.completions.create(model="llama3-8b-8192",messages=history,max_tokens=2048,temperature=0.7)
                            reply2 = resp2.choices[0].message.content
                            st.markdown(reply2)
                            st.session_state.chats[cid]["messages"].append({"role":"assistant","content":reply2,"files":[]})
                            st.session_state.pending_files=[]
                            save_to_storage()
                            st.rerun()
                        except Exception as e2:
                            st.error(f"❌ Error: {str(e2)[:300]}")
                    else:
                        st.error(f"❌ Error: {err[:300]}")

st.markdown("</div>",unsafe_allow_html=True)
