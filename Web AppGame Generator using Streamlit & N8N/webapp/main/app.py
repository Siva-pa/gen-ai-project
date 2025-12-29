import streamlit as st
import requests
import subprocess
import os
import sys
import re

# ------------------ CONFIG ------------------
st.set_page_config(
    page_title="AI Web App / Game Generator",
    layout="centered"
)

N8N_URL = "https://anna-sovice1.app.n8n.cloud/webhook/ai-generator"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GENERATED_DIR = os.path.join(BASE_DIR, "generated")

APP_FILE = os.path.join(GENERATED_DIR, "generated_app.py")
GAME_FILE = os.path.join(GENERATED_DIR, "generated_game.py")

os.makedirs(GENERATED_DIR, exist_ok=True)

# ------------------ SESSION STATE ------------------
if "last_generated" not in st.session_state:
    st.session_state.last_generated = None

# ------------------ UI ------------------
st.title("🤖 AI-Powered Web App / Game Generator")

prompt = st.text_area(
    "Describe your app or game",
    placeholder="Create a calculator using Streamlit or make a tic tac toe game using pygame"
)

# ------------------ UTILS ------------------
def sanitize_code(code: str) -> str:
    """
    1. Remove hidden / control characters
    2. Fix deprecated Streamlit APIs
    """
    # Remove non-printable characters
    code = re.sub(r"[^\x09\x0A\x0D\x20-\x7E]", "", code)

    # Fix deprecated Streamlit APIs
    code = code.replace("st.experimental_rerun()", "st.rerun()")

    return code


def call_n8n(app_type):
    if not prompt.strip():
        st.error("❌ Prompt cannot be empty")
        return None

    payload = {
        "type": app_type,
        "prompt": prompt
    }

    try:
        res = requests.post(N8N_URL, json=payload, timeout=120)
    except Exception as e:
        st.error(f"❌ Failed to connect to n8n: {e}")
        return None

    try:
        data = res.json()
    except Exception:
        st.error("❌ n8n did not return valid JSON")
        st.text(res.text)
        return None

    code = data.get("code")

    if not isinstance(code, str) or not code.strip():
        st.error("❌ 'code' field missing or empty in n8n response")
        st.json(data)
        return None

    code = sanitize_code(code)

    if len(code) < 50:
        st.error("❌ Generated code is too short or invalid")
        return None

    return code


def save_code(file_path, code):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(code)
    return os.path.getsize(file_path) > 50

# ------------------ GENERATE BUTTONS ------------------
col1, col2 = st.columns(2)

with col1:
    if st.button("🧩 Generate App (Streamlit)"):
        code = call_n8n("app")
        if code and save_code(APP_FILE, code):
            st.session_state.last_generated = "app"
            st.success("✅ App generated successfully")

with col2:
    if st.button("🎮 Generate Game (pygame)"):
        code = call_n8n("game")
        if code and save_code(GAME_FILE, code):
            st.session_state.last_generated = "game"
            st.success("✅ Game generated successfully")

st.divider()

# ------------------ RUN BUTTON ------------------
if st.button("▶️ Run Generated App/Game"):

    if st.session_state.last_generated == "app":
        if os.path.exists(APP_FILE):
            subprocess.Popen(
                ["streamlit", "run", APP_FILE],
                cwd=GENERATED_DIR,
                shell=True
            )
            st.info("🚀 Streamlit app opened in a new browser tab")
        else:
            st.error("❌ App file not found")

    elif st.session_state.last_generated == "game":
        if os.path.exists(GAME_FILE):
            subprocess.Popen(
                [sys.executable, GAME_FILE],
                cwd=GENERATED_DIR,
                shell=True
            )
            st.info("🎮 Game window launched")
        else:
            st.error("❌ Game file not found")

    else:
        st.error("❌ Generate an app or game first")
