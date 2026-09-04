import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS
from streamlit_js_eval import streamlit_js_eval
import base64, fitz, uuid, json, re
from datetime import datetime
import streamlit.components.v1 as components
try:
    import docx  # python-docx, optional — Word file reading
    HAS_DOCX = True
except ImportError:
    HAS_DOCX = False

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

def clean_api_key(raw):
    """Strip anything that isn't a valid API-key character.
    Protects against accidental copy-paste of extra text (like a currency
    symbol or label) alongside the actual key, which breaks HTTP requests."""
    if not raw:
        return ""
    cleaned = raw.strip()
    cleaned = "".join(ch for ch in cleaned if 33 <= ord(ch) <= 126)  # printable ASCII only
    return cleaned

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

# ════════════════════════════════════════
#  LONG-TERM MEMORY — separate permanent store
#  (facts Shourya remembers across ALL chats)
# ════════════════════════════════════════
MEMORY_KEY = "shourya_memory_v1"

def save_memory():
    text = st.session_state.get("long_term_memory", "")
    b64 = base64.b64encode(text.encode("utf-8")).decode("utf-8")
    streamlit_js_eval(
        js_expressions=f"localStorage.setItem('{MEMORY_KEY}', atob('{b64}')); 'saved'",
        key=f"savemem_{uuid.uuid4().hex[:6]}"
    )

def load_memory():
    raw = streamlit_js_eval(
        js_expressions=f"localStorage.getItem('{MEMORY_KEY}')",
        key="load_memory_once"
    )
    if raw and raw not in ("null", "undefined"):
        return raw
    return ""

# ════════════════════════════════════
#  SESSION STATE INIT + LOAD
# ════════════════════════════════════
if "initialized" not in st.session_state:
    st.session_state.initialized = False
    st.session_state.storage_load_tries = 0
    st.session_state.chats = {}
    st.session_state.current_id = None
    st.session_state.pending_files = []
    st.session_state.show_uploader = False
    st.session_state.show_mic = False
    st.session_state.saved_api_key = ""
    st.session_state.long_term_memory = ""

# Load from localStorage on first run.
# streamlit_js_eval returns None on its very first mount (the JS call/response
# is a two-step round trip) — so we retry a couple of times before giving up,
# instead of wrongly concluding "nothing was saved" and re-asking for the key.
if not st.session_state.initialized:
    saved = load_from_storage()
    mem = load_memory()
    if saved is None and st.session_state.storage_load_tries < 3:
        st.session_state.storage_load_tries += 1
        st.rerun()
    else:
        st.session_state.long_term_memory = mem or ""
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
        elif f.name.lower().endswith(".docx") and HAS_DOCX:
            try:
                import io
                d = docx.Document(io.BytesIO(raw))
                txt = "\n".join([p.text for p in d.paragraphs])
                texts.append(f"[Word Doc: {f.name}]\n{txt}")
            except:
                texts.append(f"[Word Doc: {f.name}] (could not read)")
            records.append({"name":f.name,"type":"docx"})
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

    st.markdown("<div style='font-size:0.78rem;color:#6b7280;margin-bottom:4px;'>🔑 Groq API Key</div>", unsafe_allow_html=True)
    api_key_input = st.text_input(
        "", type="password",
        placeholder="gsk_... (saved permanently)",
        label_visibility="collapsed",
        value=st.session_state.saved_api_key,
        key="api_key_field"
    )
    if api_key_input and api_key_input != st.session_state.saved_api_key:
        st.session_state.saved_api_key = clean_api_key(api_key_input)
        save_to_storage()
    st.markdown("<div style='font-size:0.72rem;color:#22c55e;'>✅ Key saved permanently in your browser</div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.72rem;color:#9ca3af;'>FREE key → console.groq.com</div>", unsafe_allow_html=True)
    st.divider()

    st.markdown("<div style='font-size:0.78rem;color:#6b7280;margin-bottom:4px;'>🧠 Long-Term Memory</div>", unsafe_allow_html=True)
    mem_input = st.text_area(
        "", value=st.session_state.long_term_memory,
        placeholder="e.g. I prefer Python. I'm building a food delivery app. Call me by name X.",
        label_visibility="collapsed", height=90, key="mem_field"
    )
    if mem_input != st.session_state.long_term_memory:
        st.session_state.long_term_memory = mem_input
        save_memory()
    st.markdown("<div style='font-size:0.7rem;color:#9ca3af;'>Remembered in every chat, permanently.</div>", unsafe_allow_html=True)
    st.divider()

    st.markdown("<div style='font-size:0.78rem;color:#6b7280;margin-bottom:4px;'>🎯 Select Mode</div>", unsafe_allow_html=True)
    mode_list = list(MODES.keys())
    default_mode = get_chat()["mode"] if get_chat() else mode_list[-1]
    def _sync_from_sidebar():
        new_mode = st.session_state.get("sidebar_mode")
        if get_chat() and new_mode:
            st.session_state.chats[st.session_state.current_id]["mode"] = new_mode
            st.session_state["topbar_mode"] = new_mode
    mode = st.selectbox("", mode_list, index=mode_list.index(default_mode), label_visibility="collapsed", key="sidebar_mode", on_change=_sync_from_sidebar)
    st.divider()

    st.markdown("<div class='new-chat-wrap'>", unsafe_allow_html=True)
    if st.button("✏️  New Chat", use_container_width=True):
        create_new_chat(); save_to_storage(); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

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
st.markdown("<div class='main-content'>", unsafe_allow_