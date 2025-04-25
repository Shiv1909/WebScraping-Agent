
from agent.query_analyzer import QueryAnalyzer

def analyze_query(user_query: str):
    analyzer = QueryAnalyzer()
    metadata = analyzer.analyze_query(user_query)
    keyword_chunks = metadata.get("KeywordChunks", [[user_query]])
    return keyword_chunks
