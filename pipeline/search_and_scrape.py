
# pipeline/search_and_scrape.py

import streamlit as st
from urllib.parse import urlparse
from pipeline.crawler import crawl_site

def search_and_scrape(keyword_chunks, search_tool, scraper, chunker, user_query, max_links=4, max_pages=3, max_crawl_depth=2, max_crawl_pages=3):
    st.sidebar.markdown("### 🔗 Scraped Sources")
    scraped_results = []
    all_chunks = []

    for chunk in keyword_chunks:
        if len(scraped_results) >= max_links:
            break

        query = " ".join(chunk)
        chunk_results = search_tool.search(query, num_results=10, max_pages=max_pages)

        for result in chunk_results:
            if len(scraped_results) >= max_links:
                break

            # Check if it's a homepage-style URL
            parsed = urlparse(result["link"])
            if parsed.path in ["", "/", "/index.html", "/home"]:
                try:
                    crawled_pages = crawl_site(result["link"], user_query, max_depth=max_crawl_depth, max_links=max_crawl_pages)
                    for page in crawled_pages:
                        if len(scraped_results) >= max_links:
                            break
                        doc_chunks = chunker.chunk_text(page["content"], {"url": page["url"], "title": f"Crawled from {result['link']}"})
                        all_chunks.extend(doc_chunks)
                        scraped_results.append({"title": f"Crawled from {result['link']}", "link": page["url"], "page": result.get("page", 1)})
                        st.sidebar.markdown(f"<span style='color:green'>🌐 Crawled</span> 🔹 <a href='{page['url']}' target='_blank'>{page['url']}</a>", unsafe_allow_html=True)
                except Exception as e:
                    st.sidebar.warning(f"Failed to crawl {result['link']} — {e}")
                continue

            # Standard page scraping
            scraped = scraper.scrape(result["link"])
            if scraped["content"]:
                doc_chunks = chunker.chunk_text(scraped["content"], {
                    "url": result["link"],
                    "title": result["title"]
                })
                all_chunks.extend(doc_chunks)
                scraped_results.append(result)

                page_info = result.get("page", 1)
                if page_info > 1:
                    st.sidebar.markdown(
                        f"<span style='color:orange'>📄 Page {page_info}</span> 🔹 <a href='{result['link']}' target='_blank'>{result['title']}</a>",
                        unsafe_allow_html=True)
                else:
                    st.sidebar.markdown(f"🔹 [Page {page_info}] [{result['title']}]({result['link']})")

    return scraped_results, all_chunks
