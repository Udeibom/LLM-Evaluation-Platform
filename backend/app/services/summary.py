from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models


def get_experiment_summary(db: Session, experiment_id):

    result = (
        db.query(
            func.count(models.Evaluation.id).label("num_samples"),
            func.avg(models.Evaluation.score).label("mean_score"),
            func.stddev(models.Evaluation.score).label("std_dev"),
            func.avg(models.Output.latency_ms).label("avg_latency"),
            func.max(models.Output.latency_ms).label("max_latency"),
            func.min(models.Output.latency_ms).label("min_latency"),
            func.avg(
                func.cast(models.Evaluation.hallucination, models.Integer)
            ).label("hallucination_rate"),
        )
        .join(models.Output, models.Output.id == models.Evaluation.output_id)
        .filter(models.Output.experiment_id == experiment_id)
        .one()
    )

    return {
        "num_samples": result.num_samples or 0,
        "mean_score": float(result.mean_score or 0),
        "std_dev": float(result.std_dev or 0),
        "hallucination_rate": float(result.hallucination_rate or 0),
        "avg_latency": float(result.avg_latency or 0),
        "max_latency": int(result.max_latency or 0),
        "min_latency": int(result.min_latency or 0),
    }