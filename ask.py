import os
import time
from google.genai import types
import chromadb
from dotenv import load_dotenv
from google import genai

load_dotenv()
llm = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options=types.HttpOptions(timeout=15000),
)
MODELS = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-3.8-flash"]


def generate(prompt):
    last = None
    for model in MODELS:
        try:
            return llm.models.generate_content(model=model, contents=prompt)
        except Exception as e:
            last = e
    raise last

db = chromadb.PersistentClient(path="db")
collection = db.get_collection("charter")


def answer(question, k=4):
    res = collection.query(query_texts=[question], n_results=k)
    docs = res["documents"][0]
    metas = res["metadatas"][0]

    context = "\n\n".join(
        f"[Page {m['page']}]\n{d}" for d, m in zip(docs, metas)
    )
    prompt = (
        "Answer the question using ONLY the passages below. "
        "Mention the page number like (Page 3) after each fact. "
        "If the answer is not in the passages, say: "
        "'I couldn't find this in the charter.'\n\n"
        f"PASSAGES:\n{context}\n\nQUESTION: {question}"
    )
    resp = generate(prompt)
    return resp.text, metas


if __name__ == "__main__":
    q = input("Ask: ")
    text, metas = answer(q)
    print("\n" + text)
    print("\nSources: pages", sorted({m["page"] for m in metas}))