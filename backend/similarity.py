from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")

def detect_duplicates(flashcards):

    embeddings = model.encode(flashcards)

    similarity_matrix = cosine_similarity(embeddings)

    duplicates = []

    for i in range(len(flashcards)):

        for j in range(i + 1, len(flashcards)):

            score = similarity_matrix[i][j]

            if score > 0.85:

                duplicates.append({
                    "flashcard1": flashcards[i],
                    "flashcard2": flashcards[j],
                    "score": float(score)
                })

    return duplicates