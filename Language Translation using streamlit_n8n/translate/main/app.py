import streamlit as st
import requests

st.set_page_config(page_title="Text Translator", layout="centered")

st.title("🌍 Text Translator App")
st.write("Enter text and select a language to translate.")

# -----------------------------
# Input text
# -----------------------------
input_text = st.text_area(
    "✍️ Enter text to translate",
    placeholder="Type your text here..."
)

# -----------------------------
# Language mapping
# -----------------------------
languages = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "Kannada": "kn",
    "Chinese": "zh",
    "Japanese": "ja"
}

target_language = st.selectbox(
    "🌐 Select target language",
    list(languages.keys())
)

# -----------------------------
# Translate button
# -----------------------------
if st.button("🔁 Translate"):
    if not input_text.strip():
        st.warning("⚠️ Please enter text to translate.")
    else:
        payload = {
            "text": input_text.strip(),
            "target_language": languages[target_language]
        }

        headers = {
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(
                "https://anna-sovice1.app.n8n.cloud/webhook/translate-text",  # 🔁 Replace with your n8n PRODUCTION webhook URL
                json=payload,
                headers=headers,
                timeout=30
            )

            if response.status_code == 200:
                data = response.json()

                st.success("✅ Translation Successful")
                st.write("### 📝 Translated Text")
                st.write(data.get("translated_text", "No translation received"))

            else:
                st.error(f"❌ Error {response.status_code}")
                st.write(response.text)

        except requests.exceptions.RequestException as e:
            st.error("🚨 Failed to connect to translation service")
            st.write(str(e))
