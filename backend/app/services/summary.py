from sqlalchemy.orm import Session
from sqlalchemy import func
from app import models


def get_experiment_summary(db: Session, experiment_id):

    # ----- Metrics -----
    metrics = (
        db.query(
            func.count(models.Evaluation.id).label("num_samples"),
            func.avg(models.Evaluation.score).label("mean_score"),
            func.stddev(models.Evaluation.score).label("std_dev"),
            func.avg(
                func.cast(models.Evaluation.hallucination, models.Integer)
            ).label("hallucination_rate")
        )
        .join(models.Output, models.Output.id == models.Evaluation.output_id)
        .filter(models.Output.experiment_id == experiment_id)
        .one()
    )

    # ----- Latency -----
    latency = (
        db.query(
            func.avg(models.Output.latency_ms).label("avg_latency"),
            func.max(models.Output.latency_ms).label("max_latency"),
            func.min(models.Output.latency_ms).label("min_latency")
        )
        .filter(models.Output.experiment_id == experiment_id)
        .one()
    )

    return {
        "num_samples": metrics.num_samples or 0,
        "mean_score": float(metrics.mean_score or 0),
        "std_dev": float(metrics.std_dev or 0),
        "hallucination_rate": float(metrics.hallucination_rate or 0),
        "avg_latency": float(latency.avg_latency or 0),
        "max_latency": int(latency.max_latency or 0),
        "min_latency": int(latency.min_latency or 0),
    }