import streamlit as st
import google.generativeai as genai
from datetime import date

# ---------------- Sidebar ----------------
st.sidebar.title("🔑 API Key")
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
st.title("🗕️ AI News Generator")
st.markdown("Generate **news updates or summaries** using **Gemini 2.0 Flash** ✨")

genre = st.selectbox("Choose a news category", GENRES)
user_query = st.text_input("🧠 Want something specific? Ask your own query:")

st.markdown("---")

# -------------- Gemini Content Generator --------------
def generate_news_summary(prompt):
    if not gemini_model:
        return "❌ Gemini API key not provided."
    try:
        response = gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error generating content with Gemini: {str(e)}"

# ----------- Display Content --------------
if st.button("📱 Generate News"):
    with st.spinner("Generating news content..."):
        if user_query:
            prompt = f"Please provide a detailed update or summary on the topic: {user_query}. Focus on today's developments ({date.today().isoformat()})."
        else:
            prompt = f"Provide a summary of the top {genre} news in the United States for today ({date.today().isoformat()})."
        result = generate_news_summary(prompt)
        st.success("Here’s your AI-generated news update:")
        st.write(result)

st.markdown("---")
st.caption("✨ Powered by Gemini 2.0 Flash")
