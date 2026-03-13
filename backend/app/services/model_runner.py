import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from groq import Groq
from sqlalchemy.orm import Session

from app.config import GROQ_API_KEY, GROQ_GENERATION_MODEL
from app import models


# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)


# Allowed models
ALLOWED_MODELS = {
    "mixtral-8x7b-32768",
    "llama3-8b-8192",
    "llama-3.3-70b-versatile"
}


def call_model(model_name: str, prompt: str) -> tuple[str, int]:
    """
    Sends a prompt to the specified Groq model and returns:
    - model response text
    - latency in milliseconds
    """

    if model_name not in ALLOWED_MODELS:
        raise ValueError(f"Model {model_name} not allowed")

    start = time.time()

    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=200,
        )

        latency = int((time.time() - start) * 1000)
        output_text = response.choices[0].message.content

        return output_text, latency

    except Exception as e:
        # Added logging for debugging Groq errors
        print("GROQ ERROR:", e)
        latency = int((time.time() - start) * 1000)
        return f"MODEL_ERROR: {str(e)}", latency


def run_single_prompt(experiment_id, model_name, prompt):
    """
    Runs a single prompt through the model and returns an Output object.
    """

    output_text, latency = call_model(model_name, prompt.input_text)

    # Always return an Output object (even if the model failed)
    return models.Output(
        experiment_id=experiment_id,
        prompt_id=prompt.id,
        output_text=output_text,
        latency_ms=latency,
    )


def run_experiment(db: Session, experiment: models.Experiment) -> None:
    """
    Runs the model against all prompts in the experiment's test suite
    and stores the outputs in the database.
    """

    prompts = (
        db.query(models.Prompt)
        .filter(models.Prompt.test_suite_id == experiment.test_suite_id)
        .all()
    )

    outputs = []

    with ThreadPoolExecutor(max_workers=10) as executor:

        futures = [
            executor.submit(
                run_single_prompt,
                experiment.id,
                experiment.model_name,
                prompt
            )
            for prompt in prompts
        ]

        for future in as_completed(futures):
            result = future.result()

            if result:
                outputs.append(result)

    # Safety check so silent failures don't pass unnoticed
    if not outputs:
        raise RuntimeError("Experiment produced zero outputs")

    db.add_all(outputs)
    db.commit()