import streamlit as st
import requests

# -----------------------------
# SESSION STATE INITIALIZATION
# -----------------------------
if "messages" not in st.session_state:

    try:
        response = requests.get("http://127.0.0.1:8000/history")

        if response.status_code == 200:

            history = response.json()["history"]

            st.session_state.messages = [
                {
                    "role": chat["role"],
                    "content": chat["message"]
                }
                for chat in history
            ]

        else:
            st.session_state.messages = []

    except:
        st.session_state.messages = []

if "uploaded_pdfs" not in st.session_state:
    st.session_state.uploaded_pdfs = []

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:

    st.title("🤖 AI Chatbot")

    page = st.radio(
        "Navigation",
        ["Chat", "Upload PDF", "Dashboard"]
    )

    if st.button("🗑 Clear Chat"):

        try:

            response = requests.delete(
                "http://127.0.0.1:8000/clear_history"
            )

            if response.status_code == 200:
                st.success("✅ Chat history cleared successfully!")

        except Exception as e:
            st.error(f"❌ Failed to clear chat: {e}")

        # Clear Streamlit session
        st.session_state.messages = []
        st.session_state.uploaded_pdfs = []

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
    message = st.chat_input("Type a message")

    if message:

        # Store user message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": message
            }
        )

        try:

            # If PDF uploaded → Ask PDF
            if st.session_state.uploaded_pdfs:

                response = requests.post(
                    "http://127.0.0.1:8000/ask_pdf",
                    json={
                        "question": message
                    }
                )

            # Otherwise → Normal Chat
            else:

                response = requests.post(
                    "http://127.0.0.1:8000/chat",
                    json={
                        "message": message
                    }
                )

            data = response.json()

            if "reply" in data:
                bot_response = data["reply"]

            elif "error" in data:
                bot_response = f"❌ {data['error']}"

            else:
                bot_response = "Unexpected response from backend."

        except Exception as e:
            bot_response = f"❌ Backend Error: {e}"

        # Store assistant response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": bot_response
            }
        )

        st.rerun()

# -----------------------------
# PDF UPLOAD PAGE
# -----------------------------
elif page == "Upload PDF":

    st.title("📄 Upload PDF")

    uploaded_file = st.file_uploader(
        "Choose PDF",
        type=["pdf"]
    )

    if uploaded_file:

        files = {
            "file": (
                uploaded_file.name,
                uploaded_file.getvalue(),
                "application/pdf"
            )
        }

        try:

            response = requests.post(
                "http://127.0.0.1:8000/upload_pdf",
                files=files
            )

            data = response.json()

            if response.status_code == 200:

                st.success(data["message"])

                if uploaded_file.name not in st.session_state.uploaded_pdfs:
                    st.session_state.uploaded_pdfs.append(
                        uploaded_file.name
                    )

                st.info(f"📄 File Name: {data['filename']}")
                st.info(f"📝 Characters Extracted: {data['characters_extracted']}")

            else:
                st.error(data)

        except Exception as e:
            st.error(f"❌ Upload failed: {e}")

# -----------------------------
# DASHBOARD PAGE
# -----------------------------
elif page == "Dashboard":

    st.title("📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Total Messages",
            len(st.session_state.messages)
        )

    with col2:
        st.metric(
            "Uploaded PDFs",
            len(st.session_state.uploaded_pdfs)
        )

    with col3:
        st.metric(
            "Conversations",
            len(st.session_state.messages) // 2
        )

    st.divider()

    st.subheader("📂 Uploaded Files")

    if st.session_state.uploaded_pdfs:

        st.table(
            {
                "Uploaded PDFs": st.session_state.uploaded_pdfs
            }
        )

    else:
        st.info("No PDFs uploaded yet.")

    st.divider()

    st.subheader("💬 Chat Export")

    if st.session_state.messages:

        chat_text = "\n".join(
            [
                f"{msg['role']}: {msg['content']}"
                for msg in st.session_state.messages
            ]
        )

        st.download_button(
            label="📥 Download Chat History",
            data=chat_text,
            file_name="chat_history.txt",
            mime="text/plain"
        )

    else:
        st.info("No chat messages available.")