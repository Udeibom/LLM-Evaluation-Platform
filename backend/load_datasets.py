import json
from app.db import SessionLocal
from app import models

db = SessionLocal()


def get_suite(name):

    return db.query(models.TestSuite).filter(
        models.TestSuite.name == name
    ).first()


def load_dataset(file_path, suite_name):

    suite = get_suite(suite_name)

    if not suite:
        raise Exception(f"Suite {suite_name} not found")

    with open(file_path) as f:
        dataset = json.load(f)

    prompts = dataset["prompts"]
    version = dataset["version"]

    for item in prompts:

        prompt = models.Prompt(
            test_suite_id=suite.id,
            input_text=item["question"],
            expected_output=item["reference_answer"],
            dataset_version=version
        )

        db.add(prompt)

    db.commit()

    print(f"Loaded {len(prompts)} prompts into {suite_name} ({version})")


load_dataset("datasets/factual_qa/v1.json", "factual_suite")
load_dataset("datasets/reasoning/v1.json", "reasoning_suite")
load_dataset("datasets/instructions/v1.json", "instruction_suite")

print("Datasets loaded successfully")