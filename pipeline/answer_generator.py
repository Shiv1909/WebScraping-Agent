# pipeline/answer_generator.py

import streamlit as st
import google.generativeai as genai
from collections import defaultdict
import math
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def score_documents_with_gemini(docs, user_query):
    """
    Uses Gemini to rate how relevant each document is to the user's query (scale 1–5).
    """
    model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05")
    scored_docs = []

    for i, doc in enumerate(docs):
        url = doc.metadata.get("url", "No URL")
        snippet = doc.page_content[:500]

        prompt = f"""
        You are a relevance evaluator assistant.

        Given the user's query and a document snippet, score how relevant this document is (1 to 5 scale):

        User Query:
        \"\"\"{user_query}\"\"\"

        Document Snippet:
        \"\"\"{snippet}\"\"\"

        Return a single number (1-5):
        """

        try:
            response = model.generate_content(prompt)
            score = int("".join(filter(str.isdigit, response.text.strip())))
        except Exception as e:
            logger.warning(f"Scoring failed for URL {url}: {e}")
            score = 3  # Default fallback score

        scored_docs.append({
            "doc": doc,
            "url": url,
            "score": score
        })

    scored_docs.sort(key=lambda x: x["score"], reverse=True)
    return scored_docs

def get_diverse_documents(scored_docs, min_required):
    """
    Ensure documents are picked from diverse URLs.
    """
    by_url = defaultdict(list)
    for entry in scored_docs:
        by_url[entry["url"]].append(entry)

    diverse_docs = []
    for entries in by_url.values():
        if len(diverse_docs) >= min_required:
            break
        diverse_docs.append(entries[0])

    return diverse_docs

def generate_answer(user_query, retriever, scraped_results):
    """
    Final stage — Synthesizes a markdown answer using top documents and Gemini.
    """
    try:
        raw_docs = retriever.get_relevant_documents(user_query)
        scored_docs = score_documents_with_gemini(raw_docs, user_query)

        min_required = max(1, math.ceil(0.7 * len(scraped_results)))
        selected_docs = get_diverse_documents(scored_docs, min_required)

        context = ""
        unique_sources = {}

        for i, entry in enumerate(selected_docs):
            doc = entry["doc"]
            url = doc.metadata.get("url", "No URL Provided")
            if url not in unique_sources:
                unique_sources[url] = f"Source {len(unique_sources) + 1}"
            label = unique_sources[url]
            context += f"[{label}] ({url}):\n{doc.page_content}\n\n"

        # Generate markdown report
        prompt = f"""
        You are a senior research analyst generating professional and comprehensive reports based on the provided source documents.

        Your task is to synthesize a detailed, structured, and insight-rich report in Markdown format **based strictly on the content below**.

        ---

        ### Instructions:
        - Use markdown headings (##, ###) for report sections.
        - Use bullet points only where necessary. Prefer **paragraphs with facts**.
        - If **tabular or comparative data** (e.g., pricing, features, plans, specs, performance) is mentioned in any source, format it as a **Markdown table** with headers.
        - Do not skip important numerical, plan, or policy info just because it's complex — break it down in tables or bulleted blocks as needed.
        - Use inline citations like [Source 1], [Source 2], etc. after each fact.
        - You MUST incorporate information from **at least 3 different sources**.
        - If some sources contain overlapping content, reference each one explicitly.
        - Avoid relying on just one source unless it's the only one with that information.
        - If you cannot extract anything unique from a source, mention this in the "Source Coverage" section at the end.

        ---

        ### Output Format:
        - Clean, structured Markdown
        - Use clear section titles like `## Overview`, `## Key Pricing Details`, `## Feature Comparison`, `## Industry Use Cases`, etc.
        - Include at least **one table** if the data structure allows.
        - End with a **Source Coverage Summary** explaining which sources were used and how.

        ---

        ### SOURCE DOCUMENTS:
        {context}

        ---

        ### USER QUERY:
        \"\"\"{user_query}\"\"\"

        Please begin.

        """

        model = genai.GenerativeModel("gemini-2.0-pro-exp-02-05")
        response = model.generate_content(prompt)
        answer = response.text.strip()

        st.markdown("### 🧠 Answer")
        if any(r.get("page", 1) > 1 for r in scraped_results):
            st.markdown("<span style='color:orange; font-weight:bold;'>⚠️ Includes content from deeper Google search pages</span>", unsafe_allow_html=True)
        st.markdown(answer, unsafe_allow_html=True)

        with st.expander("📊 Document Relevance Ranking"):
            for entry in scored_docs:
                url = entry["url"]
                score = entry["score"]
                label = unique_sources.get(url, "-")
                rating = "High" if score >= 4 else "Medium" if score == 3 else "Low"
                st.markdown(f"<small>🔹 **{label}** | {rating} Relevance | Score: {score}/5 — <a href='{url}' target='_blank'>{url}</a></small>", unsafe_allow_html=True)

        with st.expander("🔗 Source Citations"):
            for url, label in unique_sources.items():
                st.markdown(f"<small>🔹 **{label}**: <a href='{url}' target='_blank'>{url}</a></small>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Failed to generate answer: {e}")
        logger.exception("Gemini synthesis failed.")
