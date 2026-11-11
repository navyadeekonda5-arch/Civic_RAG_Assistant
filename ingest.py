import chromadb
from pypdf import PdfReader

PDF_PATH = "charter.pdf"
CHUNK_SIZE = 800
OVERLAP = 150

reader = PdfReader(PDF_PATH)
chunks, metadatas, ids = [], [], []

for page_num, page in enumerate(reader.pages, start=1):
    text = (page.extract_text() or "").strip()
    start = 0
    while start < len(text):
        piece = text[start:start + CHUNK_SIZE]
        if piece.strip():
            chunks.append(piece)
            metadatas.append({"page": page_num})
            ids.append(f"p{page_num}_c{start}")
        start += CHUNK_SIZE - OVERLAP

client = chromadb.PersistentClient(path="db")
try:
    client.delete_collection("charter")
except Exception:
    pass
collection = client.create_collection("charter")
collection.add(documents=chunks, metadatas=metadatas, ids=ids)

print(f"Done: {len(chunks)} chunks from {len(reader.pages)} pages")