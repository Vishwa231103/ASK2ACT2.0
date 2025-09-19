import streamlit as st
import fitz  # PyMuPDF
import openai

# Set Together.ai as OpenAI-compatible
client = openai.OpenAI(
    api_key=st.secrets["together"]["api_key"],
    base_url="https://api.together.xyz/v1"
)

# Page configuration
st.set_page_config(page_title="AI Multi-Tool", layout="wide")
st.markdown("<h1 style='text-align:center;'>🤖ASK2ACT</h1>", unsafe_allow_html=True)
st.markdown("---")

# Sidebar navigation
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712109.png", width=80)
    st.title("🧰 Tools")
    tool = st.radio("Choose a tool:", [
        "Chat Assistant", "📂 File Summarizer"
    ])
    st.markdown("---")
    st.markdown("Made with ❤️ by **Neurocoders**")

# Initialize history
if "history" not in st.session_state:
    st.session_state.history = {
        "chat": [], "code": [], "summary": [], "files": []
    }

# Chat Assistant
def chat_assistant():
    st.subheader("💬 Chat Assistant")
    user_input = st.text_input("Enter your message:")
    if st.button("Process", key="chat"):
        if user_input.strip():
            with st.spinner("Thinking..."):
                try:
                    response = client.chat.completions.create(
                        model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                        messages=[
                            {"role": "system", "content": "You are a helpful assistant."},
                            {"role": "user", "content": user_input}
                        ]
                    )
                    reply = response.choices[0].message.content
                    st.success("✅ Response generated!")
                    st.write(f"🧠 {reply}")
                    st.session_state.history["chat"].append(user_input)
                except Exception as e:
                    st.error(f"❌ Error: {e}")
        else:
            st.warning("⚠️ Please enter a message.")

# File Summarizer
def file_summarizer():
    st.subheader("📂 File Summarizer")
    uploaded_file = st.file_uploader("Upload a file:", type=["pdf", "txt"])
    if uploaded_file:
        file_text = ""
        if uploaded_file.name.endswith(".pdf"):
            try:
                doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
                for page in doc:
                    file_text += page.get_text()
            except Exception as e:
                st.error(f"Error reading PDF: {e}")
        elif uploaded_file.name.endswith(".txt"):
            file_text = uploaded_file.read().decode("utf-8")

        if file_text:
            if st.button("Process File"):
                with st.spinner("Summarizing file..."):
                    try:
                        prompt = f"Summarize the following file content:\n\n{file_text[:5000]}"
                        response = client.chat.completions.create(
                            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
                            messages=[
                                {"role": "system", "content": "You are a summarization expert."},
                                {"role": "user", "content": prompt}
                            ]
                        )
                        summary = response.choices[0].message.content
                        st.success("✅ File Summary:")
                        st.write(summary)
                        st.session_state.history["files"].append(uploaded_file.name)
                    except Exception as e:
                        st.error(f"❌ Error: {e}")

# Tool routing
if tool == "Chat Assistant":
    chat_assistant()
elif tool == "📂 File Summarizer":
    file_summarizer()
else:
    print("Unknown tool selected.")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray;'>"
    "🔧 Built with Streamlit || Made by <b>Neurocoders</b>"
    "</div>",
    unsafe_allow_html=True
)
