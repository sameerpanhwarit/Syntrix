from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")


def verify_answer(answer: str, context: str, threshold: float = 0.6) -> bool:


    if not answer or not context:
        return False

    answer_embedding = model.encode([answer])[0]
    context_embedding = model.encode([context])[0]

    similarity = np.dot(answer_embedding, context_embedding) / (
        np.linalg.norm(answer_embedding) * np.linalg.norm(context_embedding)
    )

    return similarity >= threshold