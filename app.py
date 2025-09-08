import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Forgiveness Portal 💖", page_icon="💝", layout="wide")

# ---------------- SESSION STATE ---------------- #
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "forgiveness_points" not in st.session_state:
    st.session_state.forgiveness_points = 0

# ---------------- LOGIN PAGE ---------------- #
def login_page():
    st.title("💖 Forgiveness Portal")
    username = st.text_input("Enter your name:")
    if st.button("Login 🚪"):
        if username.strip() != "":
            st.session_state.logged_in = True
            st.session_state.username = username
            st.experimental_rerun()
        else:
            st.warning("Please enter your name to continue 💌")

# ---------------- MAIN APP ---------------- #
def main_app():
    st.success(f"Welcome, {st.session_state.username}! 💖")

    st.markdown("### 📝 Grievances Dashboard 😇")
    st.markdown("### 💖 Forgiveness Meter")

    st.markdown("---")
    st.write(f"Forgiveness points: {st.session_state.forgiveness_points} 💘")

    # Grievance DB logic
    if not os.path.exists("grievances.csv"):
        pd.DataFrame(columns=["From", "To", "Message"]).to_csv("grievances.csv", index=False)

    df = pd.read_csv("grievances.csv")

    # Show grievances in chat-bubble style
    if not df.empty:
        st.subheader("💬 Past Grievances")
        for _, row in df.iterrows():
            st.markdown(
                f"<div style='background:#fff0f5; padding:10px; border-radius:12px; margin:5px 0;'>"
                f"<b>{row['From']}</b> → <i>{row['To']}</i><br>💭 {row['Message']}</div>",
                unsafe_allow_html=True
            )
    else:
        st.info("✨ No grievances yet. Start fresh!")

    # Download button (always works, unlike raw link)
    st.download_button(
        label="📥 Download Grievance Database",
        data=df.to_csv(index=False),
        file_name="grievances.csv",
        mime="text/csv"
    )

    # Logout
    if st.button("Logout 🚪"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.experimental_rerun()

# ---------------- EMOJI FLOAT CSS ---------------- #
st.markdown("""
<style>
body {
    background-color: #ffe6f0;
}

/* floating animation */
@keyframes float {
  0%   { transform: translate(0, 0); opacity: 1; }
  25%  { transform: translate(-10px, -20px); opacity: 0.9; }
  50%  { transform: translate(15px, -40px); opacity: 0.8; }
  75%  { transform: translate(-5px, -60px); opacity: 0.9; }
  100% { transform: translate(0, -80px); opacity: 1; }
}

.emoji {
  position: fixed;
  font-size: 34px;
  z-index: 9999; 
  animation: float 6s ease-in-out infinite;
}

.emoji1 { top: 90%; left: 10%; animation-delay: 0s; }
.emoji2 { top: 80%; left: 80%; animation-delay: 1.5s; }
.emoji3 { top: 70%; left: 20%; animation-delay: 3s; }
.emoji4 { top: 60%; left: 70%; animation-delay: 2.5s; }
.emoji5 { top: 85%; left: 40%; animation-delay: 1s; }
</style>

<div class="emoji emoji1">❤️</div>
<div class="emoji emoji2">⭐</div>
<div class="emoji emoji3">😇</div>
<div class="emoji emoji4">🤲</div>
<div class="emoji emoji5">👐</div>
""", unsafe_allow_html=True)

# ---------------- APP ROUTER ---------------- #
if not st.session_state.logged_in:
    login_page()
else:
    main_app()
