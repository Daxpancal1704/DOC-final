from transformers import pipeline

detector = pipeline(
    "text-classification",
    model="roberta-base-openai-detector"
)

def detect_ai(sentence):

    result = detector(sentence)

    label = result[0]['label']
    score = result[0]['score']

    if label == "Fake":
        ai_prob = score
        human_prob = 1 - score
    else:
        human_prob = score
        ai_prob = 1 - score

    classification = classify_text(ai_prob)


    return {
        "sentence": sentence,
        "ai_probability": round(ai_prob, 2),
        "human_probability": round(human_prob, 2),
        "classification": classification,
    }


def analyze_sentences(sentences):

    results = []

    for sentence in sentences:

        # 🚫 Skip empty or useless input
        if not sentence or not sentence.strip():
            continue

        # 🔒 Hard limit (avoid RoBERTa crash)
        words = sentence.split()

        if len(words) > 400:
            sentence = " ".join(words[:400])

        try:
            prediction = detect_ai(sentence)
            results.append(prediction)

        except Exception as e:
            # 🧠 Don't let one failure break entire pipeline
            results.append({
                "sentence": sentence,
                "classification": "Error",
                "confidence": 0,
                "error": str(e)
            })

    return results


def classify_text(ai_prob):

    if ai_prob >= 0.65:
        return "AI"

    elif ai_prob <= 0.35:
        return "Human"

    else:
        return "Mixed"