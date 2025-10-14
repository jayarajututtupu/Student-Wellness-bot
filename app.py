import streamlit as st
from huggingface_hub import InferenceClient

# --- Load Hugging Face token from Streamlit secrets ---
HF_TOKEN = st.secrets["HF_TOKEN"]

# --- Initialize Hugging Face client ---
client = InferenceClient("meta-llama/Meta-Llama-3-8B", token=HF_TOKEN)

# --- Streamlit App UI ---
st.set_page_config(page_title="Student Wellness Chatbot", page_icon="🧠", layout="centered")
st.title("🧠 Student Wellness Chatbot")
st.caption("A friendly AI assistant for students' mental health and well-being.")

# --- Initialize chat history ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Display chat history ---
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- User input ---
prompt = st.chat_input("How are you feeling today?")

if prompt:
    # Display user message
    st.chat_message("user").markdown(prompt)
    st.session_state.chat_history.append({"role": "user", "content": prompt})

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = client.text_generation(
                prompt,
                max_new_tokens=200,
                temperature=0.7,
                top_p=0.9
            )
            st.markdown(response)

    # Save assistant reply
    st.session_state.chat_history.append({"role": "assistant", "content": response})