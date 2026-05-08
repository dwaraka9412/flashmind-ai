from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from similarity import detect_duplicates
from hallucination import detect_hallucinations

from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA

model = SentenceTransformer("all-MiniLM-L6-v2")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():

    return {
        "message": "FlashMind AI Backend Running"
    }

@app.post("/upload")
async def upload_files(
    files: List[UploadFile] = File(...)
):

    flashcards = []

    for file in files:

        content = await file.read()

        text = content.decode("utf-8")

        lines = text.split("\n")

        for line in lines:

            clean = line.strip()

            if clean:
                flashcards.append(clean)

    # Duplicate Detection
    duplicates = detect_duplicates(flashcards)

    # Hallucination Detection
    hallucinations = detect_hallucinations(
        flashcards
    )

    # Remove Duplicates
    duplicate_items = set()

    for item in duplicates:

        duplicate_items.add(
            item["flashcard2"]
        )

    cleaned_flashcards = []

    for card in flashcards:

        if card not in duplicate_items:

            cleaned_flashcards.append(card)

    # AI Scatter Plot Data
    plot_data = []

    if len(flashcards) >= 2:

        embeddings = model.encode(
            flashcards
        )

        pca = PCA(n_components=2)

        points = pca.fit_transform(
            embeddings
        )

        for i, point in enumerate(points):

            plot_data.append({

                "x": float(point[0]),
                "y": float(point[1]),
                "name": flashcards[i]

            })

    # Average Similarity
    avg_similarity = 0

    if len(duplicates) > 0:

        avg_similarity = sum(

            d["score"]
            for d in duplicates

        ) / len(duplicates)

    unique_flashcards = len(
        cleaned_flashcards
    )

    return {

        "message":
        "Duplicate analysis completed",

        "duplicates":
        duplicates,

        "hallucinations":
        hallucinations,

        "plot_data":
        plot_data,

        "cleaned_flashcards":
        cleaned_flashcards,

        "total_flashcards":
        len(flashcards),

        "duplicate_count":
        len(duplicates),

        "unique_flashcards":
        unique_flashcards,

        "average_similarity":
        round(avg_similarity * 100, 2)

    }