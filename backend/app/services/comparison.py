from sqlalchemy.orm import Session
from app import models


def compare_experiments(db: Session, exp_a_id, exp_b_id):

    outputs_a = (
        db.query(models.Output)
        .filter(models.Output.experiment_id == exp_a_id)
        .all()
    )

    outputs_b = (
        db.query(models.Output)
        .filter(models.Output.experiment_id == exp_b_id)
        .all()
    )

    # Map prompt → score
    scores_a = {
        o.prompt_id: o.evaluations[0].score
        for o in outputs_a if o.evaluations
    }

    scores_b = {
        o.prompt_id: o.evaluations[0].score
        for o in outputs_b if o.evaluations
    }

    common_prompts = set(scores_a.keys()) & set(scores_b.keys())

    wins_a = wins_b = ties = 0

    for pid in common_prompts:
        if scores_a[pid] > scores_b[pid]:
            wins_a += 1
        elif scores_b[pid] > scores_a[pid]:
            wins_b += 1
        else:
            ties += 1

    total = len(common_prompts)

    if total == 0:
        return {
            "total_prompts": 0,
            "wins_a": 0,
            "wins_b": 0,
            "ties": 0,
            "win_rate_a": 0.0,
            "win_rate_b": 0.0,
        }

    win_rate_a = wins_a / total
    win_rate_b = wins_b / total

    return {
        "total_prompts": total,
        "wins_a": wins_a,
        "wins_b": wins_b,
        "ties": ties,
        "win_rate_a": win_rate_a,
        "win_rate_b": win_rate_b,
    }