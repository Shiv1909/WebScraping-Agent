
import streamlit as st
import google.generativeai as genai
from collections import defaultdict
import math

def score_documents_with_gemini(docs, user_query):
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
        except:
            score = 3  # fallback

        scored_docs.append({
            "doc": doc,
            "url": url,
            "score": score
        })

    scored_docs.sort(key=lambda x: x["score"], reverse=True)
    return scored_docs

def get_diverse_documents(scored_docs, min_required):
    by_url = defaultdict(list)
    for entry in scored_docs:
        by_url[entry["url"]].append(entry)

    diverse_docs = []
    for entries in by_url.values():
        if len(diverse_docs) >= min_required:
            break
        diverse_docs.append(entries[0])  # take top scoring for each unique URL

    return diverse_docs

def generate_answer(user_query, retriever, scraped_results):
    raw_docs = retriever.get_relevant_documents(user_query)
    scored_docs = score_documents_with_gemini(raw_docs, user_query)

    min_required = max(1, int(0.7 * len(scraped_results)))
    selected_docs = get_diverse_documents(scored_docs, min_required=math.ceil(0.7 * len(scraped_results)))


    context = ""
    unique_sources = {}
    for i, entry in enumerate(selected_docs):
        doc = entry["doc"]
        url = doc.metadata.get("url", "No URL Provided")
        if url not in unique_sources:
            unique_sources[url] = f"Source {len(unique_sources) + 1}"
        label = unique_sources[url]
        context += f"[{label}] ({url}):\n{doc.page_content}\n\n"

    prompt = f"""
        You are a senior research analyst generating professional and comprehensive reports based on provided source documents.

        Please create a well-structured response to the user query using the information below. Your goal is to present both qualitative and quantitative data (including tables and pricing breakdowns) in clean, readable Markdown.

        ### Instructions:
        - Use markdown headings for sections.
        - Format numbers or pricing data in tables if applicable.
        - Cite facts using inline citations like [Source 1].
        - Use bullet points where useful.
        - If structured data (e.g., features, specs, pricing, tables) is mentioned in sources, render it **as a table** with proper headers.
        - You MUST incorporate information from **at least 3 different sources** in your response.
        - If some sources contain overlapping content, reference each one explicitly.
        - Avoid relying only on a single source unless it's the only one that contains all details.
        - Use inline citations like [Source 1], [Source 2], etc. after each fact or quote.
        - If you cannot extract anything unique from a source, say so in the "Source Coverage" section at the bottom.

        ### Output Format:
        - Clean, structured Markdown
        - Use headers like `## Overview`, `## Key Pricing Details`, `## Comparison`, etc.
        - Always include citations and distinguish when info comes from different sources.

        ## Source Coverage
        - Source 1: Used in Model Comparison and Free Usage info
        - Source 2: Confirmed pricing differences
        - Source 3: Mentioned rate limits and billing tags
        - Source 4: Not used due to repetition with Source 1
 
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

    # Relevance Table UI
    with st.expander("📊 Document Relevance Ranking"):
        for entry in scored_docs:
            url = entry["url"]
            score = entry["score"]
            label = unique_sources.get(url, "-")
            rating = "High" if score >= 4 else "Medium" if score == 3 else "Low"
            st.markdown(f"<small>🔹 **{label}** | {rating} Relevance | Score: {score}/5 — <a href='{url}' target='_blank'>{url}</a></small>", unsafe_allow_html=True)

    # Final Source List
    with st.expander("🔗 Source Citations"):
        if unique_sources:
            for url, label in unique_sources.items():
                st.markdown(f"<small>🔹 **{label}**: <a href='{url}' target='_blank'>{url}</a></small>", unsafe_allow_html=True)
        else:
            st.markdown("<small>No sources available.</small>", unsafe_allow_html=True)
