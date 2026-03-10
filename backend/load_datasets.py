import json
from app.db import SessionLocal
from app import models

db = SessionLocal()

def load_dataset(file_path):

    with open(file_path) as f:
        data = json.load(f)

    for item in data:

        prompt = models.Prompt(
            input_text=item["question"],
            expected_output=item["reference_answer"]
        )

        db.add(prompt)

    db.commit()


load_dataset("datasets/factual_qa.json")
load_dataset("datasets/reasoning.json")
load_dataset("datasets/instructions.json")

print("Datasets loaded successfully")