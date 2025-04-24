# app.py

import streamlit as st
from agent.query_analyzer import QueryAnalyzer
from agent.search_tool import GoogleCSESearchTool
from agent.scraper_tool import WebScraperTool
from agent.content_analyzer import ContentAnalyzer
from agent.synthesizer import Synthesizer
from agent.config import GOOGLE_CSE_API_KEY, GOOGLE_CSE_CX

# ─── Page Config ─────────────────────────────────────────────
st.set_page_config(page_title="Web Research Agent", layout="wide")
st.title("🌐 AI-Powered Web Research Assistant")

# ─── Sidebar Inputs ──────────────────────────────────────────
st.sidebar.header("🔎 Start Your Research")
user_query = st.sidebar.text_input("Enter your query:", placeholder="e.g., India US trade deal 2025")
run_button = st.sidebar.button("Run Research")

# ─── Initialize Modules ──────────────────────────────────────
query_analyzer = QueryAnalyzer()
search_tool = GoogleCSESearchTool(api_key=GOOGLE_CSE_API_KEY, cse_id=GOOGLE_CSE_CX)
scraper = WebScraperTool()
analyzer = ContentAnalyzer()
synthesizer = Synthesizer()

# ─── Run Research Flow ───────────────────────────────────────
if run_button and user_query:
    metadata = query_analyzer.analyze_query(user_query)
    results = search_tool.search(metadata["Keywords"], num_results=15)

    articles = []
    summaries = []

    for result in results:
        scraped = scraper.scrape(result["link"])
        if scraped["content"]:
            summary = analyzer.analyze(scraped["content"], result["link"], user_query)
            articles.append(summary)
            summaries.append((result["link"], summary["summary"]))

    st.sidebar.markdown("### 📌 Query Breakdown")
    st.sidebar.json(metadata)

    # ─── Main Panel: Final Synthesized Report ────────────────
    st.subheader("🔗 Top Search Results")
    for item in results:
        st.markdown(f"- [{item['title']}]({item['link']})")
    
    st.sidebar.markdown("### 📄 Article Summaries")
    for url, summary in summaries:
        st.sidebar.markdown(f"**Summary from:** [{url}]({url})")
        st.sidebar.markdown(summary)
        
    st.subheader("🧠 Final Synthesized Report")
    if articles:
        report = synthesizer.synthesize(articles, user_query)
        st.markdown(report)
    else:
        st.warning("No valid content to synthesize a report.")
