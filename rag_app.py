
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

load_dotenv()



st.set_page_config(page_title="Gemini RAG Researcher", layout="wide")
st.title("🌐 Gemini-Powered RAG Web Research Assistant")

user_query = st.text_area(
    "🔍 Ask your question (web research will be performed):",
    placeholder="Write you query here" ,
    height=120
)
# ─── Sidebar API Key Inputs ─────────────────────────────────
st.sidebar.markdown("### 🔑 API Keys")

user_gemini_key = st.sidebar.text_input(
    label="🧠 Gemini API Key",
    type="password",
    placeholder="Paste your Gemini API key..."
)

genai.configure(api_key=user_gemini_key if user_gemini_key else GEMINI_API_KEY)
 
 # ─── Sidebar User Controls ───────────────────────────────────
st.sidebar.markdown("### ⚙️ Settings")

num_links = st.sidebar.number_input(
    "🔗 Number of valid pages to scrape",
    min_value=1,
    max_value=15,
    value=4,
    step=1,
    placeholder="Max 15"
)

max_crawl_depth = st.sidebar.number_input(
    "🌐 Crawler depth (homepage links)",
    min_value=1,
    max_value=3,
    value=2,
    step=1,
    placeholder="Max 3"
)

max_crawl_pages = st.sidebar.number_input(
    "📄 Pages per homepage to crawl",
    min_value=1,
    max_value=3,
    value=2,
    step=1,
    placeholder="Max 3"
)



if user_query:
    st.info("Running full RAG pipeline...")

    search_tool = GoogleCSESearchTool(api_key=GOOGLE_CSE_API_KEY, cse_id=GOOGLE_CSE_CX)
    scraper = WebScraperTool()
    chunker = TextChunker()
    embedding_model = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004",
        google_api_key=GEMINI_API_KEY
    )
   
    keyword_chunks = analyze_query(user_query)
    scraped_results, all_chunks = search_and_scrape(
        keyword_chunks, search_tool, scraper, chunker, user_query,
        max_links=num_links,
        max_pages=3  # This is still for Google pagination
    )
    chroma_store = embed_and_store_chunks(all_chunks, embedding_model)
    retriever = chroma_store.as_retriever(search_kwargs={"k": 4})
    generate_answer(user_query, retriever, scraped_results)
