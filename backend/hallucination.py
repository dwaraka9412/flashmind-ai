def detect_hallucinations(flashcards):

    suspicious = []

    valid_keywords = [
        "tcp",
        "http",
        "ai",
        "machine learning",
        "python",
        "protocol",
        "network",
        "intelligence",
        "data"
    ]

    for card in flashcards:

        text = card.lower()

        found = False

        for word in valid_keywords:

            if word in text:
                found = True
                break

        if not found:

            suspicious.append({
                "flashcard": card,
                "warning": "Potential hallucination detected"
            })

    return suspicious