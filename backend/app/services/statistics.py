from sqlalchemy.orm import Session
from scipy.stats import ttest_rel
from app import models


def paired_t_test(db: Session, exp_a_id, exp_b_id):

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

    scores_a = {
        o.prompt_id: o.evaluations[0].score
        for o in outputs_a if o.evaluations
    }

    scores_b = {
        o.prompt_id: o.evaluations[0].score
        for o in outputs_b if o.evaluations
    }

    common = set(scores_a.keys()) & set(scores_b.keys())

    a = [scores_a[p] for p in common]
    b = [scores_b[p] for p in common]

    if len(a) < 2:
        return {
            "t_statistic": 0,
            "p_value": 1,
            "significant": False
        }

    t_stat, p_value = ttest_rel(a, b)

    return {
        "t_statistic": float(t_stat),
        "p_value": float(p_value),
        "significant": p_value < 0.05
    }