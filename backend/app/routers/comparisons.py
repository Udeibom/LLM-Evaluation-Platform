from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app import schemas, crud, models
from app.services.model_runner import run_experiment
from app.services.judge import evaluate_outputs
from app.services.comparison import compare_experiments

router = APIRouter(prefix="/comparisons", tags=["Comparisons"])


@router.post("/run", response_model=schemas.ComparisonResponse)
def run_comparison(
    request: schemas.RunComparisonRequest,
    db: Session = Depends(get_db),
):
    # 1️⃣ Validate test suite exists
    suite = db.query(models.TestSuite).filter(
        models.TestSuite.id == request.test_suite_id
    ).first()

    if not suite:
        raise HTTPException(status_code=404, detail="Test suite not found")

    metadata = {
        "provider": "groq",
        "temperature": 0.2,
        "max_tokens": 200
    }

    # 2️⃣ Create + run Experiment A
    exp_a = crud.create_experiment(
        db,
        request.test_suite_id,
        request.model_a,
        metadata
    )

    run_experiment(db, exp_a)
    evaluate_outputs(db, exp_a.id)
    crud.complete_experiment(db, exp_a)

    # 3️⃣ Create + run Experiment B
    exp_b = crud.create_experiment(
        db,
        request.test_suite_id,
        request.model_b,
        metadata
    )

    run_experiment(db, exp_b)
    evaluate_outputs(db, exp_b.id)
    crud.complete_experiment(db, exp_b)

    # 4️⃣ Compare using your existing logic
    comparison = compare_experiments(db, exp_a.id, exp_b.id)

    return {
        "experiment_a": exp_a.id,
        "experiment_b": exp_b.id,
        **comparison
    }