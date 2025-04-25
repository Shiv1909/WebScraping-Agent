# rag_app.py

import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from langchain.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from agent.config import GOOGLE_CSE_API_KEY, GOOGLE_CSE_CX, GEMINI_API_KEY
from agent.search_tool import GoogleCSESearchTool
from agent.scraper_tool import WebScraperTool
from agent.chunker import TextChunker
from pipeline.query_handler import analyze_query
from pipeline.search_and_scrape import search_and_scrape
from pipeline.embed_and_store import embed_and_store_chunks
from pipeline.answer_generator import generate_answer

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

load_dotenv()

# ─── Streamlit UI Setup ───────────────────────────────────────
st.set_page_config(page_title="Gemini RAG Researcher", layout="wide")
st.title("🌐 Gemini-Powered RAG Web Research Assistant")

user_query = st.text_area(
    "🔍 Ask your question (web research will be performed):",
    placeholder="e.g., India-US space cooperation 2025",
    height=120
)

# ─── Sidebar API Key Input ────────────────────────────────────
st.sidebar.markdown("### 🔑 API Keys")

user_gemini_key = st.sidebar.text_input(
    label="🧠 Gemini API Key",
    type="password",
    placeholder="Paste your Gemini API key..."
)

# Override env key if user provides custom one
genai.configure(api_key=user_gemini_key if user_gemini_key else GEMINI_API_KEY)
api_key=user_gemini_key if user_gemini_key else GEMINI_API_KEY
# ─── Sidebar Settings ─────────────────────────────────────────
st.sidebar.markdown("### ⚙️ Settings")

num_links = st.sidebar.number_input("🔗 Pages to scrape", min_value=1, max_value=15, value=4, step=1)
max_crawl_depth = st.sidebar.number_input("🌐 Crawl depth", min_value=1, max_value=3, value=2, step=1)
max_crawl_pages = st.sidebar.number_input("📄 Pages per homepage", min_value=1, max_value=3, value=2, step=1)

# ─── Main Execution ───────────────────────────────────────────
if user_query:
    try:
        st.info("Running full RAG pipeline...")

        # Tool initialization
        search_tool = GoogleCSESearchTool(api_key=GOOGLE_CSE_API_KEY, cse_id=GOOGLE_CSE_CX)
        scraper = WebScraperTool()
        chunker = TextChunker()
        embedding_model = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=api_key
        )

        # RAG steps
        keyword_chunks = analyze_query(user_query)
        scraped_results, all_chunks = search_and_scrape(
            keyword_chunks, search_tool, scraper, chunker, user_query,
            max_links=num_links, max_pages=3,
            max_crawl_depth=max_crawl_depth, max_crawl_pages=max_crawl_pages
        )
        chroma_store = embed_and_store_chunks(all_chunks, embedding_model)
        if chroma_store is None:
            st.error("Failed to embed and store documents.")
        else:
            retriever = chroma_store.as_retriever(search_kwargs={"k": 4})
            generate_answer(user_query, retriever, scraped_results)

    except Exception as e:
        logger.exception("Pipeline failed.")
        st.error(f"Something went wrong: {e}")
