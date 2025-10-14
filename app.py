import streamlit as st
from huggingface_hub import InferenceClient

# Hugging Face token (stored in Streamlit secrets)
HF_TOKEN = st.secrets["HF_TOKEN"]
client = InferenceClient("meta-llama/Meta-Llama-3-8B", token=HF_TOKEN)

# Initialize session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "mood" not in st.session_state:
    st.session_state.mood = "🙂 Normal"
if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = (
        "You are a compassionate mental wellness chatbot for students. "
        "Respond empathetically and supportively. Ask gentle follow-up questions to encourage reflection."
    )

# Sidebar: Mood Tracker
st.sidebar.header("🧠 Mood Tracker")
mood = st.sidebar.radio(
    "How are you feeling today?",
    ["🙂 Normal", "😢 Sad", "😠 Angry", "😌 Calm", "😕 Upset", "😎 Cool"]
)
st.session_state.mood = mood
st.sidebar.write(f"Selected mood: {mood}")

# Chatbot UI
st.title("🌱 Student Wellness Chatbot")
st.markdown("Type how you're feeling. I'm here to support you with empathy and encouragement.")

# Input box (maintain session state to avoid rerun issues)
if "user_input" not in st.session_state:
    st.session_state.user_input = ""

st.session_state.user_input = st.text_area(
    "🧑 What's on your mind?", value=st.session_state.user_input, placeholder="e.g., 'I feel anxious about exams'"
)

# Function to generate mood-aware response
def get_wellness_response(user_message, mood):
    # Tailor prompt based on mood
    if mood in ["😢 Sad", "😠 Angry", "😕 Upset", "😥 Worried"]:
        mood_prompt = f"The student is feeling {mood}. Respond empathetically and supportively. Ask a gentle follow-up question."
    else:  # Normal, Calm, Cool, Surprised
        mood_prompt = f"The student is feeling {mood}. Respond positively and ask a reflective question or prompt gratitude."

    full_prompt = f"<|system|>\nYou are a compassionate student wellness chatbot. {mood_prompt}\n<|user|>\n{user_message}\n<|assistant|>"

    try:
        response = client.text_generation(
            prompt=full_prompt,
            max_new_tokens=250,
            temperature=0.7,
            return_full_text=False
        ).strip()
    except Exception as e:
        return f"⚠️ Sorry, I couldn't reach the model right now. ({e})"

    # Remove system/user/assistant tags
    clean_reply = response.replace("<|system|>", "").replace("<|user|>", "").replace("<|assistant|>", "").strip()

    # Remove any repeated lines that echo system instructions
    lines = clean_reply.splitlines()
    deduped = []
    for line in lines:
        if line.strip() and "The student is feeling" not in line and line not in deduped:
            deduped.append(line.strip())
    return "\n".join(deduped)

# Send button logic
if st.button("Send", key="chat_send"):
    current_input = st.session_state.user_input.strip()
    if current_input:
        with st.spinner("Thinking with empathy..."):
            bot_response = get_wellness_response(current_input, st.session_state.mood)
            st.session_state.chat_history.append(("You", current_input))
            st.session_state.chat_history.append(("Bot", bot_response))
        st.session_state.user_input = ""  # Clear input box after sending

# Display chat history
for sender, message in st.session_state.chat_history:
    st.markdown(f"**{sender}:** {message}")


