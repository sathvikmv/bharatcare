import os
import streamlit as st
import requests

# -----------------------------------------------
# BACKEND URL — priority order:
#   1. Streamlit secrets (Streamlit Cloud)
#   2. Environment variable (Render / Railway)
#   3. Local dev fallback
# -----------------------------------------------
try:
    _backend_url = st.secrets["BACKEND_URL"]
except Exception:
    _backend_url = os.environ.get(
        "BACKEND_URL",
        "https://ai-agent-backend-ev85.onrender.com"
    )

# Render's fromService:host gives only the hostname — try both HTTPS and HTTP when needed
if _backend_url and not _backend_url.startswith("http"):
    _backend_url = _backend_url.strip()

DEFAULT_USERNAME = "default_user"

def normalize_backend_url(raw_url: str) -> str:
    raw_url = raw_url.strip()
    if raw_url.startswith(("http://", "https://")):
        return raw_url.rstrip("/")

    https_url = f"https://{raw_url.rstrip('/')}"
    http_url = f"http://{raw_url.rstrip('/')}"

    for candidate in (https_url, http_url):
        try:
            resp = requests.get(f"{candidate}/", timeout=5)
            if resp.status_code == 200:
                return candidate.rstrip("/")
        except Exception:
            continue

    return https_url.rstrip("/")

BASE_URL = normalize_backend_url(_backend_url)
BACKEND_ERROR = None

# -----------------------------------------------
# PAGE CONFIG
# -----------------------------------------------
st.set_page_config(
    page_title="AI Agent with Tool Orchestration",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------
# BACKEND HEALTH CHECK
# -----------------------------------------------
def backend_online() -> bool:
    global BACKEND_ERROR
    try:
        r = requests.get(f"{BASE_URL}/", timeout=5)
        if r.status_code == 200:
            return True
        BACKEND_ERROR = f"Unexpected status {r.status_code}"
        return False
    except Exception as e:
        BACKEND_ERROR = str(e)
        return False

BACKEND_UP = backend_online()

# -----------------------------------------------
# SESSION STATE INITIALIZATION
# -----------------------------------------------
if "chat_id" not in st.session_state:
    st.session_state.chat_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# Create default chat session on first load
if BACKEND_UP and st.session_state.chat_id is None:
    try:
        r = requests.post(
            f"{BASE_URL}/chat/create",
            json={"username": DEFAULT_USERNAME, "title": "My Chat"},
            timeout=5,
        )
        if r.status_code == 201:
            st.session_state.chat_id = r.json()["id"]
    except Exception:
        pass

# -----------------------------------------------
# SIDEBAR
# -----------------------------------------------
with st.sidebar:
    st.title("🤖 AI Chatbot")
    st.caption("Powered by FastAPI + ChromaDB + RAG")

    if not BACKEND_UP:
        st.warning("⚠️ Backend offline. Running in demo mode.")
        st.caption(f"Backend check URL: `{BASE_URL}`")
        if BACKEND_ERROR:
            st.caption(f"Backend check error: `{BACKEND_ERROR}`")

    st.divider()

    page = st.radio(
        "Navigation",
        ["💬 Chat", "📄 Upload File", "📊 Dashboard"],
    )

    st.divider()

    if st.button("🗑 Clear Chat", use_container_width=True):
        if BACKEND_UP and st.session_state.chat_id:
            try:
                requests.delete(
                    f"{BASE_URL}/chat/{st.session_state.chat_id}",
                    params={"username": DEFAULT_USERNAME},
                    timeout=5,
                )
            except Exception:
                pass
        st.session_state.messages = []
        st.session_state.chat_id = None
        st.session_state.uploaded_files = []
        st.rerun()

    st.divider()
    st.caption(f"🔗 Backend: `{BASE_URL}`")

# -----------------------------------------------
# CHAT PAGE
# -----------------------------------------------
if page == "💬 Chat":
    st.title("🤖 My AI Chatbot")

    if not BACKEND_UP:
        st.info("🔌 Backend is not reachable. Messages are stored locally in this session only.")

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Type a message…")

    if user_input:
        # Ensure chat session exists
        if BACKEND_UP and st.session_state.chat_id is None:
            try:
                r = requests.post(
                    f"{BASE_URL}/chat/create",
                    json={"username": DEFAULT_USERNAME, "title": "My Chat"},
                    timeout=5,
                )
                if r.status_code == 201:
                    st.session_state.chat_id = r.json()["id"]
            except Exception:
                st.error("❌ Could not create chat session.")

        # Save user message to backend
        if BACKEND_UP and st.session_state.chat_id:
            try:
                requests.post(
                    f"{BASE_URL}/chat/{st.session_state.chat_id}/message",
                    params={"username": DEFAULT_USERNAME},
                    json={"role": "user", "content": user_input},
                    timeout=5,
                )
            except Exception:
                pass

        st.session_state.messages.append({"role": "user", "content": user_input})

        # RAG context retrieval if files uploaded
        context_str = ""
        if BACKEND_UP and st.session_state.uploaded_files:
            try:
                rag_resp = requests.post(
                    f"{BASE_URL}/rag/retrieve",
                    json={"query": user_input},
                    timeout=10,
                )
                if rag_resp.status_code == 200:
                    chunks = rag_resp.json().get("context", [])
                    if chunks:
                        context_str = "\n\n".join(chunks[:3])
            except Exception:
                pass

        # Build reply
        if context_str:
            bot_reply = (
                "📄 **Relevant context from your uploaded documents:**\n\n"
                f"{context_str}"
            )
        elif not BACKEND_UP:
            bot_reply = (
                "🤖 **Demo Mode** — Backend is not connected.\n\n"
                "To get real AI responses, deploy the FastAPI backend and set the "
                "`BACKEND_URL` secret in Streamlit Cloud."
            )
        else:
            bot_reply = (
                "🤖 I'm your AI assistant! Your message has been saved. "
                "Upload a document and ask a question to get context-based answers."
            )

        # Save bot reply to backend
        if BACKEND_UP and st.session_state.chat_id:
            try:
                requests.post(
                    f"{BASE_URL}/chat/{st.session_state.chat_id}/message",
                    params={"username": DEFAULT_USERNAME},
                    json={"role": "assistant", "content": bot_reply},
                    timeout=5,
                )
            except Exception:
                pass

        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.rerun()

# -----------------------------------------------
# UPLOAD PAGE
# -----------------------------------------------
elif page == "📄 Upload File":
    st.title("📄 Upload Document")
    st.caption("Supported formats: PDF · TXT · DOCX · CSV")

    if not BACKEND_UP:
        st.warning("⚠️ Backend is offline. File uploads are unavailable in demo mode.")
    else:
        uploaded_file = st.file_uploader(
            "Choose a file",
            type=["pdf", "txt", "docx", "csv"],
        )

        if uploaded_file:
            files = {
                "file": (
                    uploaded_file.name,
                    uploaded_file.getvalue(),
                    uploaded_file.type or "application/octet-stream",
                )
            }

            with st.spinner("⏳ Uploading and processing…"):
                try:
                    response = requests.post(
                        f"{BASE_URL}/upload/",
                        files=files,
                        timeout=60,
                    )
                    data = response.json()

                    if response.status_code == 201:
                        st.success("✅ File uploaded and indexed successfully!")
                        col1, col2 = st.columns(2)
                        col1.info(f"📄 **Filename:** `{data['filename']}`")
                        col2.info(f"📦 **Size:** {data['size']:,} bytes")
                        st.info(f"🕒 **Uploaded At:** {data['uploaded_at']}")

                        if uploaded_file.name not in st.session_state.uploaded_files:
                            st.session_state.uploaded_files.append(uploaded_file.name)
                    else:
                        st.error(f"❌ Upload failed: {data.get('detail', data)}")

                except Exception as e:
                    st.error(f"❌ Upload error: {e}")

# -----------------------------------------------
# DASHBOARD PAGE
# -----------------------------------------------
elif page == "📊 Dashboard":
    st.title("📊 Dashboard")

    if BACKEND_UP:
        try:
            metrics_resp = requests.get(f"{BASE_URL}/dashboard/", timeout=5)
            if metrics_resp.status_code == 200:
                metrics = metrics_resp.json()
                col1, col2, col3, col4 = st.columns(4)
                col1.metric("💬 Total Chats", metrics.get("total_chats", 0))
                col2.metric("📨 Total Messages", metrics.get("total_messages", 0))
                col3.metric("📁 Uploaded Files", metrics.get("total_uploaded_files", 0))
                col4.metric("🧠 Vector Chunks", metrics.get("total_documents_in_vector_db", 0))
            else:
                st.error("❌ Could not fetch metrics from backend.")
        except Exception as e:
            st.error(f"❌ Dashboard error: {e}")
    else:
        st.warning("⚠️ Backend offline — showing session stats only.")
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Messages (session)", len(st.session_state.messages))
        col2.metric("Uploaded Files (session)", len(st.session_state.uploaded_files))
        col3.metric("Conversations (session)", len(st.session_state.messages) // 2)

    st.divider()

    st.subheader("📂 Uploaded Files This Session")
    if st.session_state.uploaded_files:
        st.table({"Uploaded Files": st.session_state.uploaded_files})
    else:
        st.info("No files uploaded yet in this session.")

    st.divider()

    st.subheader("💬 Export Chat History")
    if st.session_state.messages:
        chat_text = "\n".join(
            [f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages]
        )
        st.download_button(
            label="📥 Download Chat History",
            data=chat_text,
            file_name="chat_history.txt",
            mime="text/plain",
            use_container_width=True,
        )
    else:
        st.info("No chat messages to export.")