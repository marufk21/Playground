import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

# ── 1. Load your OpenAI API key from .env ───────────────────────────────────
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY is missing. Add it to your .env file.")

# ── 2. Initialise the embeddings model ─────────────────────────────────────
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",  # cheap & fast; use "text-embedding-3-large" for higher accuracy
    api_key=api_key,
)

# ── 3. Embed a single query ─────────────────────────────────────────────────
query = "What is LangChain?"
query_vector = embeddings.embed_query(query)

print(f"Query  : {query}")
print(f"Vector : {query_vector[:5]} ...  (dim={len(query_vector)})")

# ── 4. Embed multiple documents at once ────────────────────────────────────
documents = [
    "LangChain is a framework for building LLM-powered applications.",
    "OpenAI provides powerful embedding models via its API.",
    "Embeddings represent text as dense numerical vectors.",
]
doc_vectors = embeddings.embed_documents(documents)

print(f"\nEmbedded {len(doc_vectors)} documents, each with dim={len(doc_vectors[0])}")

# ── 5. Simple cosine-similarity search (no vector DB needed) ───────────────
import math

def cosine_similarity(a, b):
    dot   = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x ** 2 for x in a))
    mag_b = math.sqrt(sum(x ** 2 for x in b))
    return dot / (mag_a * mag_b)

print("\n── Similarity scores for query vs each document ──")
for doc, vec in zip(documents, doc_vectors):
    score = cosine_similarity(query_vector, vec)
    print(f"  {score:.4f}  |  {doc}")

# ── 6. (Optional) Store in a FAISS vector store ────────────────────────────
# pip install faiss-cpu
try:
    from langchain_community.vectorstores import FAISS

    store = FAISS.from_texts(documents, embeddings)
    results = store.similarity_search("LangChain framework", k=2)

    print("\n── FAISS top-2 results ──")
    for r in results:
        print(" •", r.page_content)
except ImportError:
    print("\n(Install faiss-cpu to enable the vector-store example)")