import streamlit as st
import google.generativeai as genai

# ---------------- Sidebar ----------------
st.sidebar.title("🔑 Gemini API Key")
gemini_key = st.sidebar.text_input("Enter your Gemini API Key", type="password")

# Initialize Gemini
if gemini_key:
    genai.configure(api_key=gemini_key)
    gemini_model = genai.GenerativeModel("gemini-2.0-flash")
else:
    gemini_model = None

# -------------- Genre Choices --------------
GENRES = [
    "World",
    "Technology",
    "Science",
    "Health",
    "Business",
    "Entertainment",
    "Sports",
    "Politics",
    "Environment",
    "Education"
]

# -------------- App UI ------------------
st.set_page_config(page_title="🗞️ AI News Generator", layout="wide")
st.title("🗞️ AI News Generator")
st.markdown("Generate the **latest news summaries** using real-time data from Gemini 2.0 Flash ✨")

genre = st.selectbox("Choose a news category", GENRES)
user_query = st.text_input("🧠 Want something specific? Ask your own query:")

st.markdown("---")

# -------------- Gemini News Generator --------------
def generate_news(genre=None, custom_query=None):
    if not gemini_model:
        return "❌ Gemini API key not provided."

    if custom_query:
        prompt = f"Get the latest news and summarize it on: {custom_query}"
    else:
        prompt = f"Provide a brief and latest news summary in the {genre} category. Make it sound current and relevant."

    try:
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"

# ----------- Display News --------------
if st.button("📡 Fetch News"):
    with st.spinner("Fetching fresh news from Gemini..."):
        result = generate_news(genre=genre, custom_query=user_query)
        st.success("Here’s your AI-generated news update:")
        st.write(result)

st.markdown("---")
st.caption("✨ Powered by Gemini 2.0 Flash | No external news API used")
