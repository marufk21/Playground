from __future__ import annotations

import os
from urllib.parse import urlparse

# Set early so langchain loaders pick it up at import/runtime.
os.environ.setdefault("USER_AGENT", "rag-website-loader/1.0")

from langchain_community.document_loaders import WebBaseLoader


def _is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def load_website(url: str):
    if not _is_valid_url(url):
        raise ValueError(f"Invalid URL: {url}")

    loader = WebBaseLoader(url)
    return loader.load()


if __name__ == "__main__":
    target_url = "https://snackstack-gold.vercel.app/"
    docs = load_website(target_url)

    print(f"Loaded documents: {len(docs)}")
    for i, doc in enumerate(docs, start=1):
        preview = doc.page_content[:300].replace("\n", " ")
        safe_preview = preview.encode("ascii", "ignore").decode("ascii")
        print(f"[{i}] Source: {doc.metadata.get('source', 'N/A')}")
        print(f"    Preview: {safe_preview}...")
