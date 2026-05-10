import faiss
import numpy as np

# embedding size for MiniLM
DIMENSION = 384

index = faiss.IndexFlatL2(DIMENSION)

documents = []  # stores chunks

def add_documents(chunks, embeddings, book_id):
    global documents

    index.add(np.array(embeddings).astype("float32"))

    for chunk in chunks:
        documents.append({
            "text": chunk,
            "book_id": book_id
        })


def search(query_embedding, book_id, k=5):
    if index.ntotal == 0:
        return []

    D, I = index.search(
        np.array([query_embedding]).astype("float32"), k
    )

    results = []

    for score, idx in zip(D[0], I[0]):

        if idx == -1:
            continue

        if idx < len(documents):
            doc = documents[idx]

            # filter by book
            if doc["book_id"] == book_id:
                results.append({
                    "text": doc["text"],
                    "score": float(score)
                })

    return results