import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"
DEFAULT_USERNAME = "default_user"

# -----------------------------
# SESSION STATE INITIALIZATION
# -----------------------------
if "chat_id" not in st.session_state:
    st.session_state.chat_id = None

if "messages" not in st.session_state:
    st.session_state.messages = []

if "uploaded_files" not in st.session_state:
    st.session_state.uploaded_files = []

# Create a default chat session on first load
if st.session_state.chat_id is None:
    try:
        r = requests.post(
            f"{BASE_URL}/chat/create",
            json={"username": DEFAULT_USERNAME, "title": "My Chat"}
        )
        if r.status_code == 201:
            st.session_state.chat_id = r.json()["id"]
    except Exception:
        pass

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.title("🤖 AI Chatbot")

    page = st.radio(
        "Navigation",
        ["Chat", "Upload File", "Dashboard"]
    )

    if st.button("🗑 Clear Chat"):
        if st.session_state.chat_id:
            try:
                requests.delete(
                    f"{BASE_URL}/chat/{st.session_state.chat_id}",
                    params={"username": DEFAULT_USERNAME}
                )
            except Exception:
                pass
        st.session_state.messages = []
        st.session_state.chat_id = None
        st.session_state.uploaded_files = []
        st.rerun()

# -----------------------------
# CHAT PAGE
# -----------------------------
if page == "Chat":

    st.title("🤖 My AI Chatbot")

    # Display chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # Chat input
    user_input = st.chat_input("Type a message")

    if user_input:
        # Ensure chat session exists
        if st.session_state.chat_id is None:
            try:
                r = requests.post(
                    f"{BASE_URL}/chat/create",
                    json={"username": DEFAULT_USERNAME, "title": "My Chat"}
                )
                if r.status_code == 201:
                    st.session_state.chat_id = r.json()["id"]
            except Exception:
                st.error("❌ Could not create chat session.")
                st.stop()

        # Save user message to backend
        try:
            requests.post(
                f"{BASE_URL}/chat/{st.session_state.chat_id}/message",
                params={"username": DEFAULT_USERNAME},
                json={"role": "user", "content": user_input}
            )
        except Exception:
            pass

        st.session_state.messages.append({"role": "user", "content": user_input})

        # Retrieve context from RAG if files uploaded
        context_str = ""
        if st.session_state.uploaded_files:
            try:
                rag_resp = requests.post(
                    f"{BASE_URL}/rag/retrieve",
                    json={"query": user_input}
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
                f"📄 **Relevant context from your uploaded documents:**\n\n{context_str}"
            )
        else:
            bot_reply = (
                "🤖 I'm your AI assistant! I don't have an LLM connected yet, but "
                "your message has been saved. Upload a document and ask a question to "
                "get context-based answers."
            )

        # Save bot reply to backend
        try:
            requests.post(
                f"{BASE_URL}/chat/{st.session_state.chat_id}/message",
                params={"username": DEFAULT_USERNAME},
                json={"role": "assistant", "content": bot_reply}
            )
        except Exception:
            pass

        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        st.rerun()

# -----------------------------
# FILE UPLOAD PAGE
# -----------------------------
elif page == "Upload File":

    st.title("📄 Upload Document")
    st.caption("Supported formats: PDF, TXT, DOCX, CSV")

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "txt", "docx", "csv"]
    )

    if uploaded_file:
        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                uploaded_file.type or "application/octet-stream"
            )
        }

        with st.spinner("Uploading and processing..."):
            try:
                response = requests.post(
                    f"{BASE_URL}/upload/",
                    files=files
                )
                data = response.json()

                if response.status_code == 201:
                    st.success(f"✅ File uploaded successfully!")
                    st.info(f"📄 **Filename:** {data['filename']}")
                    st.info(f"📦 **Size:** {data['size']} bytes")
                    st.info(f"🕒 **Uploaded At:** {data['uploaded_at']}")

                    if uploaded_file.name not in st.session_state.uploaded_files:
                        st.session_state.uploaded_files.append(uploaded_file.name)
                else:
                    st.error(f"❌ Upload failed: {data.get('detail', data)}")

            except Exception as e:
                st.error(f"❌ Upload error: {e}")

# -----------------------------
# DASHBOARD PAGE
# -----------------------------
elif page == "Dashboard":

    st.title("📊 Dashboard")

    # Fetch live metrics from backend
    try:
        metrics_resp = requests.get(f"{BASE_URL}/dashboard/", timeout=5)
        if metrics_resp.status_code == 200:
            metrics = metrics_resp.json()
        else:
            metrics = None
    except Exception:
        metrics = None

    if metrics:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("💬 Total Chats", metrics.get("total_chats", 0))
        col2.metric("📨 Total Messages", metrics.get("total_messages", 0))
        col3.metric("📁 Uploaded Files", metrics.get("total_uploaded_files", 0))
        col4.metric("🧠 Vector Chunks", metrics.get("total_documents_in_vector_db", 0))
    else:
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Messages", len(st.session_state.messages))
        col2.metric("Uploaded Files", len(st.session_state.uploaded_files))
        col3.metric("Conversations", len(st.session_state.messages) // 2)

    st.divider()

    st.subheader("📂 Uploaded Files This Session")
    if st.session_state.uploaded_files:
        st.table({"Uploaded Files": st.session_state.uploaded_files})
    else:
        st.info("No files uploaded yet.")

    st.divider()

    st.subheader("💬 Chat Export")
    if st.session_state.messages:
        chat_text = "\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages]
        )
        st.download_button(
            label="📥 Download Chat History",
            data=chat_text,
            file_name="chat_history.txt",
            mime="text/plain"
        )
    else:
        st.info("No chat messages available.")