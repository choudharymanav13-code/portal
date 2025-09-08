import streamlit as st
import random

# ---------------- SETTINGS ----------------
USERS = {
    "vinitheprettiest": "ihatemybf",
    "manav": "boilttle"
}

CATEGORIES = [
    "Late replies ⏳",
    "Didn’t call 📞",
    "Forgot something important 😒",
    "Food fight 🍕",
    "Other 📝"
]

PRESET_REPLIES = [
    "I'm sowwy 🥺👉👈",
    "Next time pakka better ❤️",
    "Forgive me na 🤲",
    "Pizza treat on me 🍕",
    "Love you too much to fight 💕"
]

THEME_CSS = """
<style>
body {
    background-color: #ffeef8;
}
.stApp {
    background-color: #fff;
    border-radius: 25px;
    padding: 20px;
}
.chat-bubble-user {
    background: #ffb6c1;
    color: black;
    padding: 10px 15px;
    border-radius: 20px;
    margin: 5px;
    max-width: 70%;
}
.chat-bubble-reply {
    background: #fff0f5;
    color: black;
    padding: 10px 15px;
    border-radius: 20px;
    margin: 5px;
    max-width: 70%;
    align-self: flex-end;
}
.emoji-bg {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    font-size: 24px;
    opacity: 0.2;
}
</style>
"""

EMOJIS = ["💖","✨","🥺","🤲","💕","⭐"]

# ---------------- APP ----------------
st.set_page_config(page_title="Grievance Portal 💌", layout="centered")
st.markdown(THEME_CSS, unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "forgiveness" not in st.session_state:
    st.session_state.forgiveness = 50
if "chat" not in st.session_state:
    st.session_state.chat = []

# Login
if not st.session_state.logged_in:
    st.title("💌 Cute Grievance Portal")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.user = username
            st.success(f"Welcome {username} 💕")
        else:
            st.error("No entry 🚫 Wrong credentials")
    st.stop()

# Main App
st.title("💗 Grievance Chat 💗")

# Floating emoji background
st.markdown(
    f"<div class='emoji-bg'>{' '.join(random.choices(EMOJIS, k=100))}</div>",
    unsafe_allow_html=True
)

# Chat history
for speaker, msg in st.session_state.chat:
    if speaker == "user":
        st.markdown(f"<div class='chat-bubble-user'>{msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-reply'>{msg}</div>", unsafe_allow_html=True)

# Add grievance
with st.form("grievance_form", clear_on_submit=True):
    category = st.selectbox("Pick a grievance category 💔", CATEGORIES)
    grievance = st.text_area("Your grievance goes here 📝")
    submitted = st.form_submit_button("Send 💌")
    if submitted and grievance.strip():
        st.session_state.chat.append(("user", f"[{category}] {grievance}"))
        reply = random.choice(PRESET_REPLIES)
        st.session_state.chat.append(("reply", reply))
        # forgiveness meter effect
        if "sorry" in reply.lower() or "love" in reply.lower():
            st.session_state.forgiveness += 5
        else:
            st.session_state.forgiveness -= 2

# Forgiveness meter
st.subheader("💟 Forgiveness Meter")
st.progress(min(max(st.session_state.forgiveness, 0), 100))

if st.button("Logout 🚪"):
    st.session_state.logged_in = False
    st.experimental_rerun()
