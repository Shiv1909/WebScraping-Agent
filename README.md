## 📚 Web Research Agent

An AI-powered assistant built with Gemini 2.5 Pro and Streamlit that performs end-to-end web research. It analyzes user queries, performs custom Google searches, scrapes and summarizes content, checks source reliability, and synthesizes information into a coherent report.

---

### 🧠 Key Features

- **Query Understanding**: Gemini extracts intent, keywords, info types, and time filters.
- **Web Search**: Uses Google Custom Search API to fetch relevant links.
- **Web Scraping**: Extracts textual content from links using BeautifulSoup.
- **Content Analysis**: Summarizes content, tags content type, and checks topical relevance.
- **Information Synthesis**: Groups insights, resolves contradictions, and presents a final takeaway.
- **Streamlit Interface**: Interactive research flow with real-time summaries and a final report.

---

### 🗂️ Project Structure

```bash
WebResearchAgent/
│
├── app.py                        # Streamlit UI & orchestration logic
├── .env                          # API Keys and environment settings
├── README.md                     # This file
│
├── agent/
│   ├── config.py                 # Loads API keys from environment
│   ├── query_analyzer.py         # Gemini-powered query breakdown
│   ├── search_tool.py            # Google CSE search interface
│   ├── scraper_tool.py           # Web scraping with BeautifulSoup
│   ├── content_analyzer.py       # Summarizes and rates reliability
│   └── synthesizer.py            # Gemini synthesis of multi-article insights
│
└── requirements.txt              # Python dependencies
```

---

### 🔧 Setup & Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/web-research-agent.git
   cd web-research-agent
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup environment variables**
   Create a `.env` file with the following:
   ```env
   GOOGLE_CSE_API_KEY=your_api_key_here
   GOOGLE_CSE_CX=your_custom_search_engine_id
   GEMINI_API_KEY=your_gemini_api_key
   ```

4. **Run the Streamlit app**
   ```bash
   streamlit run app.py
   ```

---

### 🧬 Architecture Overview

![Architecture Diagram](docs/architecture.png)


