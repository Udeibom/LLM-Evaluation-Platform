import json
import random
import os


def generate_factual():
    capitals = [
        ("France", "Paris"),
        ("Germany", "Berlin"),
        ("Italy", "Rome"),
        ("Spain", "Madrid"),
        ("Japan", "Tokyo"),
        ("Canada", "Ottawa"),
        ("Brazil", "Brasilia"),
        ("Australia", "Canberra"),
        ("India", "New Delhi"),
        ("Egypt", "Cairo")
    ]

    scientists = [
        ("penicillin", "Alexander Fleming"),
        ("gravity", "Isaac Newton"),
        ("relativity", "Albert Einstein"),
        ("radioactivity", "Marie Curie"),
        ("evolution", "Charles Darwin")
    ]

    questions = []
    i = 1

    for country, capital in capitals:
        questions.append({
            "id": f"qa_{i:03}",
            "question": f"What is the capital of {country}?",
            "reference_answer": capital,
            "category": "factual_qa"
        })
        i += 1

    for discovery, scientist in scientists:
        questions.append({
            "id": f"qa_{i:03}",
            "question": f"Who discovered {discovery}?",
            "reference_answer": scientist,
            "category": "factual_qa"
        })
        i += 1

    return questions


def generate_reasoning():
    questions = []

    for i in range(1, 101):
        a = random.randint(2, 20)
        b = random.randint(2, 20)

        questions.append({
            "id": f"reason_{i:03}",
            "question": f"If you multiply {a} by {b}, what is the result?",
            "reference_answer": str(a * b),
            "category": "reasoning"
        })

    return questions


def generate_instructions():
    base_sentences = [
        "Artificial intelligence is transforming many industries.",
        "Climate change affects ecosystems and weather patterns.",
        "Machine learning allows computers to learn from data.",
        "Space exploration has advanced rapidly in recent decades.",
        "Education is essential for economic development."
    ]

    questions = []
    i = 1

    for sentence in base_sentences:

        questions.append({
            "id": f"inst_{i:03}",
            "question": f"Summarize this sentence: {sentence}",
            "reference_answer": sentence,
            "category": "instruction"
        })
        i += 1

        questions.append({
            "id": f"inst_{i:03}",
            "question": f"Rewrite this sentence in simpler language: {sentence}",
            "reference_answer": sentence,
            "category": "instruction"
        })
        i += 1

    return questions


datasets = {
    "datasets/factual_qa/v1.json": {
        "dataset": "factual_qa",
        "version": "v1",
        "prompts": generate_factual()
    },
    "datasets/reasoning/v1.json": {
        "dataset": "reasoning",
        "version": "v1",
        "prompts": generate_reasoning()
    },
    "datasets/instructions/v1.json": {
        "dataset": "instructions",
        "version": "v1",
        "prompts": generate_instructions()
    }
}


for file_path, data in datasets.items():

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)


print("Datasets generated.")