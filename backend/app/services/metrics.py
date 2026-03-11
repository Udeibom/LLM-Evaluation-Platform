from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app import models


def compute_experiment_metrics(db: Session, experiment_id: int):

    query = (
        db.query(
            func.count(models.Evaluation.id).label("num_samples"),

            func.avg(models.Evaluation.score).label("mean_score"),

            func.stddev(models.Evaluation.score).label("std_dev"),

            func.avg(models.Output.latency_ms).label("avg_latency"),

            func.sum(
                case(
                    (models.Evaluation.score <= 2, 1),
                    else_=0
                )
            ).label("hallucinations"),

            func.sum(
                case(
                    (models.Evaluation.score >= 4, 1),
                    else_=0
                )
            ).label("passes"),
        )
        .join(models.Output, models.Output.id == models.Evaluation.output_id)
        .filter(models.Output.experiment_id == experiment_id)
    )

    result = query.one()

    num_samples = result.num_samples or 0
    hallucinations = result.hallucinations or 0
    passes = result.passes or 0

    hallucination_rate = 0
    pass_rate = 0

    if num_samples > 0:
        hallucination_rate = hallucinations / num_samples
        pass_rate = passes / num_samples

    return {
        "num_samples": int(num_samples),
        "mean_score": float(result.mean_score or 0),
        "std_dev": float(result.std_dev or 0),
        "avg_latency": float(result.avg_latency or 0),
        "hallucination_rate": float(hallucination_rate),
        "pass_rate": float(pass_rate),
    }