# pipeline/crawler.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from typing import List, Dict, Tuple, Set
from pipeline.link_ranker import rank_links_by_query

def extract_internal_links(soup: BeautifulSoup, base_url: str) -> List[str]:
    internal_links = []
    base_domain = urlparse(base_url).netloc

    for a in soup.find_all("a", href=True):
        href = a["href"]
        full_url = urljoin(base_url, href)
        parsed = urlparse(full_url)

        if parsed.netloc == base_domain:
            internal_links.append(full_url)

    return list(set(internal_links))

def crawl_site(start_url: str, user_query: str, max_depth: int = 2, max_links: int = 5) -> List[Dict]:
    visited: Set[str] = set()
    queue: List[Tuple[str, int]] = [(start_url, 0)]
    crawled_pages = []

    while queue and len(crawled_pages) < max_links:
        url, depth = queue.pop(0)
        if url in visited or depth > max_depth:
            continue
        visited.add(url)

        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            html = response.text
            soup = BeautifulSoup(html, "html.parser")
            content = "\n".join(p.get_text() for p in soup.find_all("p") if p.get_text())

            crawled_pages.append({
                "url": url,
                "depth": depth,
                "content": content.strip()
            })

            if len(crawled_pages) >= max_links:
                break

            internal_links = extract_internal_links(soup, url)
            ranked_links = rank_links_by_query(internal_links, user_query, top_k=5)
            queue.extend([(link, depth + 1) for link in ranked_links if link not in visited])

        except Exception as e:
            print(f"[Crawler] Failed to crawl {url}: {e}")
            continue

    return crawled_pages
