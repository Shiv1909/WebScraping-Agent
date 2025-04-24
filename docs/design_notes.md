 ## 📈 Detailed Working of the Web Research Agent

The Web Research Agent follows a modular, multi-step pipeline that transforms a user query into a reliable, summarized report. It leverages Google Gemini for natural language processing, Google Custom Search for information retrieval, and BeautifulSoup for scraping.

---

### 🔹 Step-by-Step Flow

#### 1. **User Input**
- User enters a natural language research query in the Streamlit interface.
- Example: "India US trade deal 2025"

#### 2. **Query Analyzer (query_analyzer.py)**
- Gemini 2.5 Pro model is used to extract structured metadata from the input query.
- Returns:
  - **Intent** (e.g., news, opinion, analysis)
  - **Keywords** (extracted for search)
  - **Information Types** (e.g., statistics, policy summaries)
  - **Time Range** (e.g., "last year")

#### 3. **Google Search Tool (search_tool.py)**
- Uses the `GOOGLE_CSE_API_KEY` and `GOOGLE_CSE_CX` to perform a search via Google Custom Search API.
- Pulls top `n` results (default = 15) based on relevance to query keywords.
- Returns list of dictionaries with:
  - Title
  - URL
  - Snippet

#### 4. **Web Scraper Tool (scraper_tool.py)**
- Visits each URL and extracts readable `<p>` tags using BeautifulSoup.
- Clips long text to 5000 characters for optimal LLM processing.
- Returns:
  - Page content
  - URL

#### 5. **Content Analyzer (content_analyzer.py)**
- Uses Gemini 2.5 to summarize scraped content.
- Adds metadata such as:
  - **Summary** (in bullet points)
  - **Content Type** (e.g., "news report")
  - **Relevance Rating** (high, medium, low)

#### 6. **Synthesizer (synthesizer.py)**
- Receives all article summaries and the original query.
- Synthesizes content using Gemini with the following logic:
  - Group similar insights across sources.
  - Highlight contradictions.
  - End with a unified **"Final Takeaway"**.
- Returns the final report in Markdown format.

#### 7. **Streamlit Output (app.py)**
- Displays the following to the user:
  - Sidebar: Query analysis & article summaries.
  - Main view: Top links and final synthesized report.

---

### 🛠️ Tech Stack & Tools

| Component         | Technology/Library         |
|------------------|----------------------------|
| UI               | Streamlit                  |
| LLM              | Google Gemini 2.5 Pro      |
| Search API       | Google Custom Search (CSE) |
| Scraper          | BeautifulSoup, Requests    |
| Config Management| Python-dotenv              |

---

### 🚀 Example End-to-End Flow

**Query:** "Electric vehicle subsidies in Europe 2024"

**Result:**
- 15 relevant articles scraped
- 12 summaries processed
- Synthesized final markdown with policy trends, contradictions in subsidy effectiveness, and a closing insight.


