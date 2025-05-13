import streamlit as st
import requests
import google.generativeai as genai
from datetime import date

# ---------------- Sidebar ----------------
st.sidebar.title("🔑 API Keys")
gemini_key = st.sidebar.text_input("Enter your Gemini API Key", type="password")

# Initialize Gemini
if gemini_key:
    genai.configure(api_key=gemini_key)
    gemini_model = genai.GenerativeModel("gemini-2.0-flash")
else:
    gemini_model = None

# Load NewsData.io key from secrets
newsdata_key = st.secrets.get("newsdata_api_key", None)

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
st.markdown("Generate the **latest news summaries** using [NewsData.io](https://newsdata.io) and **Gemini 2.0 Flash** ✨")

genre = st.selectbox("Choose a news category", GENRES)
user_query = st.text_input("🧠 Want something specific? Ask your own query:")

st.markdown("---")

# -------------- NewsData Fetcher --------------
def fetch_newsdata(genre):
    if not newsdata_key:
        return ["❌ NewsData.io API key not provided."]

    today = date.today().isoformat()  # Format: 'YYYY-MM-DD'
    url = (
        f"https://newsdata.io/api/1/news"
        f"?apikey={newsdata_key}"
        f"&country=us"
        f"&category={genre.lower()}"
        f"&language=en"
        f"&pub_date={today}"
    )
    try:
        response = requests.get(url)
        data = response.json()
        return [
            article['title'] + ":\n" + article.get('description', '')
            for article in data.get('results', [])[:5]
        ]
    except Exception as e:
        return [f"❌ Error fetching news: {str(e)}"]

# -------------- Gemini Summarizer --------------
def summarize_with_gemini(text):
    if not gemini_model:
        return "❌ Gemini API key not provided."
    try:
        response = gemini_model.generate_content(f"Summarize the following news article:\n\n{text}")
        return response.text
    except Exception as e:
        return f"❌ Error summarizing with Gemini: {str(e)}"

# ----------- Display News --------------
if st.button("📱 Fetch News"):
    with st.spinner("Fetching and summarizing news..."):
        if user_query:
            # Direct Gemini query
            result = summarize_with_gemini(user_query)
            st.success("Here’s your AI-generated news update:")
            st.write(result)
        else:
            news_list = fetch_newsdata(genre)
            for i, news in enumerate(news_list):
                st.markdown(f"### 🗕️ Article {i+1}")
                st.write(news)
                summary = summarize_with_gemini(news)
                st.markdown("**🧠 Summary:**")
                st.write(summary)

st.markdown("---")
st.caption("✨ Powered by NewsData.io + Gemini 2.0 Flash")
