import streamlit as st
import random
import datetime
import time

# --------------------------
# CONFIG
# --------------------------
st.set_page_config(page_title="💖 Grievance Portal", layout="wide")

# Floating emoji CSS
st.markdown("""
<style>
body {
    background-color: #ffe6f0;
}
@keyframes float {
  0% { transform: translateY(0); opacity: 1; }
  50% { transform: translateY(-20px); opacity: 0.7; }
  100% { transform: translateY(0); opacity: 1; }
}
.emoji {
  position: fixed;
  font-size: 30px;
  animation: float 3s infinite;
}
.chat-bubble {
    background-color: #fff0f5;
    padding: 10px 15px;
    border-radius: 15px;
    margin-bottom: 5px;
    max-width: 70%;
}
.user-bubble {
    background-color: #ffe6f0;
    align-self: flex-end;
}
.chat-container {
    display: flex;
    flex-direction: column;
}
</style>
<div class="emoji" style="top:10%;left:5%;">❤️</div>
<div class="emoji" style="top:20%;left:90%;">⭐</div>
<div class="emoji" style="top:40%;left:10%;">😇</div>
<div class="emoji" style="top:70%;left:80%;">🤲</div>
<div class="emoji" style="top:60%;left:50%;">👐</div>
""", unsafe_allow_html=True)

# --------------------------
# USER DATA
# --------------------------
if "grievances" not in st.session_state:
    st.session_state.grievances = []
if "forgiveness" not in st.session_state:
    st.session_state.forgiveness = 0
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "show_goodbye" not in st.session_state:
    st.session_state.show_goodbye = False

# --------------------------
# LOGIN SYSTEM
# --------------------------
users = {
    "vinitheprettiest": "ihatemybf",
    "manav": "boilttle"
}

# Goodbye screen
if st.session_state.show_goodbye:
    st.markdown("<h1 style='text-align:center;'>💖 Goodbye for now 💖</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align:center;'>See you soon cutie 🥺💕</h3>", unsafe_allow_html=True)
    st.balloons()
    time.sleep(2)  # show for 2 seconds
    st.session_state.show_goodbye = False
    st.rerun()

if not st.session_state.logged_in:
    st.title("💌 Cute Grievance Portal")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if username in users and password == users[username]:
        st.session_state.logged_in = True
        st.session_state.username = username
        st.rerun()
    elif username or password:
        st.error("Wrong credentials 😢")

else:
    username = st.session_state.username
    st.success(f"Welcome, {username}! 💖")

    # --------------------------
    # HER VIEW
    # --------------------------
    if username == "vinitheprettiest":
        st.header("✨ Submit a grievance")

        category = st.selectbox("Pick a category 💭", [
            "You forgot something 😒",
            "You annoyed me 🙄",
            "You’re too cute to be mad at 😍",
            "I just need attention 🥺",
            "Other..."
        ])
        mood = st.radio("How mad are you? 🤔", ["😇", "😐", "😡", "🤯"])
        text = st.text_area("What happened? 📝")

        if st.button("Submit grievance 💌"):
            grievance = {
                "user": username,
                "time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
                "category": category,
                "mood": mood,
                "text": text,
                "reply": None,
                "resolved": False
            }
            st.session_state.grievances.append(grievance)
            messages = [
                "Grievance noted 💕 cuddle pending 🤗",
                "Uh oh! Pizza bribe coming 🍕",
                "I’ll make it up to you with extra hugs 🫂",
                "Noted, guilty as charged 😅",
                "Love you, sorryyy 💖"
            ]
            st.success(random.choice(messages))

        st.header("📜 My Grievances History")
        for g in st.session_state.grievances:
            if g["user"] == "vinitheprettiest":
                st.markdown(
                    f"<div class='chat-container'><div class='chat-bubble user-bubble'>**[{g['time']}] {g['category']} {g['mood']}**<br>{g['text']}</div></div>",
                    unsafe_allow_html=True
                )
                if g["reply"]:
                    st.markdown(
                        f"<div class='chat-container'><div class='chat-bubble'>💌 {g['reply']}</div></div>",
                        unsafe_allow_html=True
                    )
                if g["resolved"]:
                    st.success("✔️ Resolved")

    # --------------------------
    # HIS VIEW
    # --------------------------
    elif username == "manav":
        st.header("📋 Grievances Dashboard")

        for i, g in enumerate(st.session_state.grievances):
            st.markdown(f"**[{g['time']}] {g['category']} {g['mood']}**")
            st.markdown(f"{g['text']}")
            reply = st.text_input(f"Reply to grievance {i+1}", key=f"reply_{i}")
            if st.button(f"Send Reply {i+1}"):
                st.session_state.grievances[i]["reply"] = reply
                st.success("Reply sent 💌")
            if not g["resolved"] and st.button(f"Mark Resolved {i+1}"):
                st.session_state.grievances[i]["resolved"] = True
                st.session_state.forgiveness += 1
                st.balloons()
                st.success("Grievance resolved ❤️")

        st.header("💖 Forgiveness Meter")
        st.progress(min(st.session_state.forgiveness, 10)/10)
        st.write(f"Forgiveness points: {st.session_state.forgiveness} ❤️")

    # --------------------------
    # LOGOUT BUTTON
    # --------------------------
    if st.button("Logout 🚪"):
        st.session_state.clear()
        st.session_state.show_goodbye = True
        st.rerun()
