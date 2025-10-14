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
st.sidebar.header("🧠 What's your mood now?")
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
    if mood in ["😢 Sad", "😠 Angry", "😕 Upset"]:
        mood_prompt = (
            "The student is feeling {mood}. Respond with empathy, encouragement, "
            "and practical advice to help them feel better."
        ).format(mood=mood)
    else:  # Normal, Calm, Cool
        mood_prompt = (
            "The student is feeling {mood}. Respond positively, celebrate their feelings, "
            "and ask a reflective question to encourage mindfulness or gratitude."
        ).format(mood=mood)

    full_prompt = f"<|system|>\nYou are a compassionate student wellness chatbot. {mood_prompt}\n<|user|>\n{user_message}\n<|assistant|>"

    try:
        response = client.text_generation(
            prompt=full_prompt,
            max_new_tokens=300,
            temperature=0.7,
            return_full_text=False
        ).strip()
    except Exception as e:
        response = f"⚠️ Sorry, I couldn't reach the model right now. ({e})"

    clean_reply = response.replace(user_message, "").replace("<|system|>", "").replace("<|user|>", "").replace("<|assistant|>", "").strip()
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



