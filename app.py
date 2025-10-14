import os
import streamlit as st
from huggingface_hub import InferenceClient

# Hugging Face token (securely stored in Streamlit secrets)
HF_TOKEN = st.secrets["HF_TOKEN"]
client = InferenceClient("meta-llama/Meta-Llama-3-8B", token=HF_TOKEN)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "mood" not in st.session_state:
    st.session_state.mood = "🙂 Normal"

# Sidebar: Emoji Mood Tracker
st.sidebar.header("🧠 What's your Present Mood?")
mood = st.sidebar.radio(
    "How are you feeling today?",
    ["🙂 Normal", "😢 Sad", "😠 Angry", "😌 Calm", "😕 Upset", "😎 Cool"]
)
st.session_state.mood = mood
st.sidebar.write(f"Selected mood: {mood}")

# Chatbot UI
st.title("😊 Student Wellness Chatbot")
st.markdown("Type how you're feeling. I'm here to support you with empathy and encouragement.")

user_input = st.text_area("🧑 What's on your mind?", placeholder="e.g., 'I feel anxious about exams'")

# LLaMA response function
def get_wellness_response(user_message, mood):
    system_prompt = (
        f"You are a compassionate mental wellness chatbot for students. "
        f"The student is currently feeling {mood}. "
        "Respond with empathy, motivation, and relaxation tips. "
        "After your response, ask a gentle follow-up question to encourage reflection."
    )
    full_prompt = f"<|system|>\n{system_prompt}\n<|user|>\n{user_message}\n<|assistant|>"
    
    response = client.text_generation(full_prompt, max_new_tokens=300, temperature=0.7)
    reply = response.strip()

    # Remove system and user tags if present
    clean_reply = (
        reply.replace("<|system|>", "")
             .replace("<|user|>", "")
             .replace("<|assistant|>", "")
             .strip()
    )

    return clean_reply

# Send button
if st.button("Send", key="chat_send"):
    if user_input:
        with st.spinner("Thinking with empathy..."):
            bot_response = get_wellness_response(user_input, st.session_state.mood)
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Bot", bot_response))

# Display chat history
for sender, message in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {message}")
