import streamlit as st
import pickle
import re
from PIL import Image

# Load model
model = pickle.load(open("model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

# Page config
st.set_page_config(
    page_title="Fake News Detection System",
    page_icon="📰",
    layout="centered"
)

# Load image
try:
    banner = Image.open("news.jpg")
except:
    banner = None

# ------------------ CSS Styling ------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #e3f2fd, #ffffff);
}

.main-title {
    text-align: center;
    color: #0d47a1;
    font-size: 42px;
    font-weight: bold;
}

.sub-title {
    text-align: center;
    color: #333;
    font-size: 18px;
}

.card {
    background-color: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.1);
    margin-top: 20px;
}

.login-title {
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    color: #0d47a1;
}
</style>
""", unsafe_allow_html=True)

# ------------------ Session ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ------------------ Clean text ------------------
def clean_text(text):
    text = text.lower()
    text = re.sub(r"\W", " ", text)
    text = re.sub(r"\d", "", text)
    text = re.sub(r"\s+", " ", text)
    return text

# ------------------ LOGIN PAGE ------------------
def login_page():
    if banner:
        st.image(banner, use_container_width=True)

    st.markdown("<div class='login-title'>🔐 Login to Fake News Detection System</div>", unsafe_allow_html=True)
    st.write("")

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    if st.button("🚀 Login"):
        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.success("✅ Login Successful!")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")
    st.markdown("</div>", unsafe_allow_html=True)

# ------------------ MAIN APP ------------------
def main_app():
    if banner:
        st.image(banner, use_container_width=True)

    st.markdown("<div class='main-title'>📰 Fake News Detection System</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>AI Powered News Authenticity Checker</div>", unsafe_allow_html=True)

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.write("### ✍️ Paste the news article below:")

    user_input = st.text_area("", height=180)

    if st.button("🔍 Check News"):
        if user_input.strip() == "":
            st.warning("⚠️ Please enter some news text.")
        else:
            cleaned = clean_text(user_input)
            vector = vectorizer.transform([cleaned])
            prediction = model.predict(vector)

            if prediction[0] == 1:
                st.success("🟢 This News is REAL")
            else:
                st.error("🔴 This News is FAKE")

    st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

# ------------------ Router ------------------
if st.session_state.logged_in:
    main_app()
else:
    login_page()
