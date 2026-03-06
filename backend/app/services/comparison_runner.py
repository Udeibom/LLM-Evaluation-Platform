from app.db import SessionLocal
from sqlalchemy.orm import Session

from app import models, crud
from app.services.model_runner import run_experiment
from app.services.judge import evaluate_outputs
from app.services.comparison import compare_experiments


def run_full_comparison(comparison_id: int):

    db: Session = SessionLocal()

    try:
        comparison = db.query(models.Comparison).filter(
            models.Comparison.id == comparison_id
        ).first()

        metadata = {
            "provider": "groq",
            "temperature": 0.2,
            "max_tokens": 200
        }

        # Experiment A
        exp_a = crud.create_experiment(
            db,
            comparison.test_suite_id,
            comparison.model_a,
            metadata
        )

        run_experiment(db, exp_a)
        evaluate_outputs(db, exp_a.id)
        crud.complete_experiment(db, exp_a)

        # Experiment B
        exp_b = crud.create_experiment(
            db,
            comparison.test_suite_id,
            comparison.model_b,
            metadata
        )

        run_experiment(db, exp_b)
        evaluate_outputs(db, exp_b.id)
        crud.complete_experiment(db, exp_b)

        result = compare_experiments(db, exp_a.id, exp_b.id)

        # Guard against None result
        if result is None:
            raise ValueError("Comparison returned None")

        comparison.experiment_a_id = exp_a.id
        comparison.experiment_b_id = exp_b.id

        comparison.total_prompts = result["total_prompts"]

        comparison.wins_a = result["wins_a"]
        comparison.wins_b = result["wins_b"]
        comparison.ties = result["ties"]

        comparison.win_rate_a = result["win_rate_a"]
        comparison.win_rate_b = result["win_rate_b"]

        comparison.status = "completed"

        db.commit()

    finally:
        db.close()