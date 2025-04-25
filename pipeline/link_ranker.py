# pipeline/link_ranker.py

from typing import List
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def rank_links_by_query(links: List[str], query: str, top_k: int = 5) -> List[str]:
    """
    Rank internal links based on relevance to the query using TF-IDF cosine similarity.

    Args:
        links (List[str]): Anchor texts or hrefs to rank.
        query (str): User's question or topic.
        top_k (int): Number of top links to return.

    Returns:
        List[str]: Ranked list of links most relevant to the query.
    """
    if not links:
        return []

    try:
        vectorizer = TfidfVectorizer().fit([query] + links)
        vectors = vectorizer.transform([query] + links)
        query_vec = vectors[0]
        link_vecs = vectors[1:]
        scores = cosine_similarity(query_vec, link_vecs).flatten()
        ranked_links = [link for _, link in sorted(zip(scores, links), reverse=True)]
        return ranked_links[:top_k]
    except Exception as e:
        print(f"[LinkRanker] Failed to rank links: {e}")
        return links[:top_k]
