# main.py

from agent.query_analyzer import QueryAnalyzer
from agent.search_tool import GoogleCSESearchTool
from agent.scraper_tool import WebScraperTool
from agent.content_analyzer import ContentAnalyzer
from agent.synthesizer import Synthesizer
from agent.config import GOOGLE_CSE_API_KEY, GOOGLE_CSE_CX

def run_web_research_agent(user_query: str):
    print(f"\n🧠 Research Topic: {user_query}\n")

    # Step 1: Analyze the query
    analyzer = QueryAnalyzer()
    query_metadata = analyzer.analyze_query(user_query)
    print("🔍 Query Analysis:")
    for k, v in query_metadata.items():
        print(f"{k}: {v}")
    print()

    # Step 2: Perform web search
    search_tool = GoogleCSESearchTool(api_key=GOOGLE_CSE_API_KEY, cse_id=GOOGLE_CSE_CX)
    search_results = search_tool.search(query_metadata["Keywords"], num_results=3)

    print("🔗 Top Search Results:")
    for idx, item in enumerate(search_results):
        print(f"{idx + 1}. {item['title']} \n   {item['link']}\n")

    # Step 3: Scrape and analyze each URL
    scraper = WebScraperTool()
    content_analyzer = ContentAnalyzer()
    articles = []

    for result in search_results:
        scraped = scraper.scrape(result["link"])
        if scraped["content"]:
            summary = content_analyzer.analyze(scraped["content"], result["link"])
            articles.append(summary)

    # Step 4: Synthesize report
    synthesizer = Synthesizer()
    final_report = synthesizer.synthesize(articles, user_query)

    print("\n📄 Final Synthesized Report:\n")
    print(final_report)


if __name__ == "__main__":
    topic = input("🔎 Enter your research topic: ")
    run_web_research_agent(topic)
