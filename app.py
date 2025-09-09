import streamlit as st
import sqlite3
import datetime
from streamlit_autorefresh import st_autorefresh

# --------------------------
# CONFIG & THEME
# --------------------------
st.set_page_config(page_title="💖 Grievance Portal", layout="wide")

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
# DB INIT
# --------------------------
conn = sqlite3.connect("grievances.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS grievances (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_by TEXT,
    assigned_to TEXT,
    category TEXT,
    status TEXT,
    created_at TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    grievance_id INTEGER,
    sender TEXT,
    text TEXT,
    timestamp TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS love_notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT,
    text TEXT,
    timestamp TEXT
)
""")

conn.commit()

# --------------------------
# LOGIN
# --------------------------
users = {
    "vinitheprettiest": "ihatemybf",
    "manav": "boilttle"
}

st.title("💌 Cute Grievance Portal")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

if not st.session_state.logged_in:
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
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.rerun()

    # Auto-refresh just chat areas
    st_autorefresh(interval=5000, key="refresh")

    # --------------------------
    # VINITA VIEW: CREATE GRIEVANCE
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
        text = st.text_area("What happened? 📝")

        if st.button("Submit grievance 💌"):
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            c.execute("INSERT INTO grievances (created_by, assigned_to, category, status, created_at) VALUES (?, ?, ?, ?, ?)",
                      (username, "manav", category, "Pending", now))
            grievance_id = c.lastrowid
            c.execute("INSERT INTO messages (grievance_id, sender, text, timestamp) VALUES (?, ?, ?, ?)",
                      (grievance_id, username, text, now))
            conn.commit()
            st.success("Grievance submitted 💕")

    # --------------------------
    # GRIEVANCE DASHBOARD (BOTH USERS)
    # --------------------------
    st.header("📋 Grievances Dashboard")

    grievances = c.execute("SELECT * FROM grievances ORDER BY id DESC").fetchall()

    for g in grievances:
        gid, created_by, assigned_to, category, status, created_at = g
        st.markdown(f"**[{created_at}] {category}** — *{status}*")

        messages = c.execute("SELECT sender, text, timestamp FROM messages WHERE grievance_id=? ORDER BY id ASC", (gid,)).fetchall()
        for m in messages:
            sender, text, ts = m
            bubble_class = "chat-bubble user-bubble" if sender == username else "chat-bubble"
            st.markdown(f"<div class='chat-container'><div class='{bubble_class}'>**{sender} [{ts}]**<br>{text}</div></div>", unsafe_allow_html=True)

        if status == "Pending":
            reply = st.text_input(f"Reply to grievance {gid}", key=f"reply_{gid}")
            if st.button(f"Send Reply {gid}"):
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                c.execute("INSERT INTO messages (grievance_id, sender, text, timestamp) VALUES (?, ?, ?, ?)",
                          (gid, username, reply, now))
                conn.commit()
                st.success("Reply sent 💌")
                st.rerun()

            if st.button(f"Mark Resolved {gid}"):
                c.execute("UPDATE grievances SET status='Resolved' WHERE id=?", (gid,))
                conn.commit()
                st.balloons()
                st.success("Grievance resolved ❤️")
                st.rerun()

        st.write("---")

    # --------------------------
    # FORGIVENESS METER
    # --------------------------
    st.header("💖 Forgiveness Meter")
    resolved_count = c.execute("SELECT COUNT(*) FROM grievances WHERE status='Resolved'").fetchone()[0]
    st.progress(min(resolved_count, 10) / 10)
    st.write(f"Forgiveness points: {resolved_count} ❤️")

    # --------------------------
    # LOVE NOTES
    # --------------------------
    st.header("💌 Love Notes (Not Grievances)")
    note = st.text_input("Send a sweet note 🥰", key="note_input")
    if st.button("Send Note"):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        c.execute("INSERT INTO love_notes (sender, text, timestamp) VALUES (?, ?, ?)",
                  (username, note, now))
        conn.commit()
        st.success("Note sent 💖")
        st.rerun()

    notes = c.execute("SELECT sender, text, timestamp FROM love_notes ORDER BY id DESC").fetchall()
    for n in notes:
        sender, text, ts = n
        bubble_class = "chat-bubble user-bubble" if sender == username else "chat-bubble"
        st.markdown(f"<div class='chat-container'><div class='{bubble_class}'>**{sender} [{ts}]**<br>{text}</div></div>", unsafe_allow_html=True)
