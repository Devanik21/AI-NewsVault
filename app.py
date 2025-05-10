import streamlit as st
import requests
import google.generativeai as genai

# Set your API keys
NEWS_API_KEY = "your_news_api_key_here"
GEMINI_API_KEY = "your_gemini_api_key_here"

# Initialize Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-pro")

# Genre choices
GENRES = {
    "Top Headlines": "general",
    "Technology": "technology",
    "Science": "science",
    "Health": "health",
    "Business": "business",
    "Entertainment": "entertainment",
    "Sports": "sports"
}

# Streamlit UI
st.set_page_config(page_title="🗞️ AI News Summarizer", layout="wide")
st.title("🗞️ AI News Summarizer")
st.markdown("Stay updated with **real-time news** and get quick summaries powered by **Gemini**!")

# Genre selection
genre = st.selectbox("Choose a news category", list(GENRES.keys()))
st.markdown("---")

# Fetch news from NewsAPI
def fetch_news(category):
    url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    return response.json().get("articles", [])

# Generate Gemini summary
def summarize_with_gemini(text, mode="normal"):
    if mode == "normal":
        prompt = f"Summarize the following news article:\n\n{text}"
    else:
        prompt = f"Explain the following news article like I'm 5 years old:\n\n{text}"
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Fetch and show news
articles = fetch_news(GENRES[genre])

if articles:
    for i, article in enumerate(articles[:5]):  # limit to 5 articles
        with st.expander(f"📰 {article['title']}"):
            st.write(f"**Source**: {article.get('source', {}).get('name', 'N/A')}")
            st.write(f"**Published At**: {article.get('publishedAt', 'N/A')}")
            st.image(article.get("urlToImage"), width=500)
            st.write(article.get("description", "No description available."))
            
            # AI summary modes
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"🧠 Gemini Summary {i}"):
                    with st.spinner("Thinking..."):
                        summary = summarize_with_gemini(article.get("content", ""))
                        st.success(summary)
            with col2:
                if st.button(f"👶 Explain Like I'm 5 {i}"):
                    with st.spinner("Explaining..."):
                        summary = summarize_with_gemini(article.get("content", ""), mode="eLI5")
                        st.info(summary)
else:
    st.warning("No news found. Please try a different category or check API limits.")

st.markdown("---")
st.caption("Made with ❤️ using NewsAPI + Gemini ✨")

