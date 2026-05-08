from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import os

from similarity import detect_duplicates
from hallucination import detect_hallucinations

from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA

app = FastAPI()

# CORS (for frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")


@app.get("/")
def home():
    return {"message": "FlashMind AI Backend Running 🚀"}


@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):

    flashcards = []

    for file in files:
        content = await file.read()
        text = content.decode("utf-8")

        for line in text.split("\n"):
            clean = line.strip()
            if clean:
                flashcards.append(clean)

    # Detect duplicates
    duplicates = detect_duplicates(flashcards)

    # Detect hallucinations
    hallucinations = detect_hallucinations(flashcards)

    # Remove duplicates
    duplicate_items = set(d["flashcard2"] for d in duplicates)

    cleaned_flashcards = [
        card for card in flashcards if card not in duplicate_items
    ]

    # PCA visualization
    plot_data = []

    if len(flashcards) >= 2:
        embeddings = model.encode(flashcards)
        pca = PCA(n_components=2)
        points = pca.fit_transform(embeddings)

        for i, point in enumerate(points):
            plot_data.append({
                "x": float(point[0]),
                "y": float(point[1]),
                "name": flashcards[i]
            })

    # Average similarity
    avg_similarity = (
        sum(d["score"] for d in duplicates) / len(duplicates)
        if duplicates else 0
    )

    return {
        "message": "Duplicate analysis completed",
        "duplicates": duplicates,
        "hallucinations": hallucinations,
        "plot_data": plot_data,
        "cleaned_flashcards": cleaned_flashcards,
        "total_flashcards": len(flashcards),
        "duplicate_count": len(duplicates),
        "unique_flashcards": len(cleaned_flashcards),
        "average_similarity": round(avg_similarity * 100, 2)
    }


# Render compatibility (IMPORTANT)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=port)