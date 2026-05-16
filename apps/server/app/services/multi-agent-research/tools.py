from pathlib import Path

from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
from rich import print

print("Tools Output:")

load_dotenv(),

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def web_search(query : str) -> str:
    """Search the web for recent and reliable information on a topic . Returns Titles , URLs and snippets."""
    results = tavily.search(query=query,max_results=5)
    print("[web_search] raw response:", results)

    out = []

    for r in results['results']:
        out.append(
            f"Title: {r['title']}\nURL: {r['url']}\nSnippet: {r['content'][:300]}\n"
        )

    formatted = "\n----\n".join(out)
    print("[web_search] formatted output:\n", formatted)
    return formatted

@tool
def scrape_url(url: str) -> str:
    """Scrape and return clean text content from a given URL for deeper reading."""
    try:
        resp = requests.get(url, timeout=8, headers={"User-Agent": "Mozilla/5.0"})
        print(f"[scrape_url] status={resp.status_code} url={url}")
        soup = BeautifulSoup(resp.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        text = soup.get_text(separator=" ", strip=True)[:3000]
        print(f"[scrape_url] text preview ({len(text)} chars):\n", text[:500])
        return text
    except Exception as e:
        print(f"[scrape_url] error: {e}")
        return f"Could not scrape URL: {str(e)}"


if __name__ == "__main__":
    if not os.getenv("TAVILY_API_KEY"):
        print("Missing TAVILY_API_KEY in .env — web_search will fail.")
    else:
        print("=== Testing web_search ===")
        search_out = web_search.invoke({"query": "What is LangChain?"})
        print("\n=== web_search returned ===\n", search_out)

    print("\n=== Testing scrape_url ===")
    scrape_out = scrape_url.invoke({"url": "https://example.com"})
    print("\n=== scrape_url returned (first 300 chars) ===\n", scrape_out[:300])

