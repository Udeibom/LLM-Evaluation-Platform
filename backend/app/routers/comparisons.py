from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session

from app.db import get_db
from app import schemas, models
from app.services.comparison_runner import run_full_comparison

router = APIRouter(prefix="/comparisons", tags=["Comparisons"])


@router.post("/run", response_model=schemas.ComparisonJobResponse)
def run_comparison(
    request: schemas.RunComparisonRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
):
    # Validate test suite exists
    suite = db.query(models.TestSuite).filter(
        models.TestSuite.id == request.test_suite_id
    ).first()

    if not suite:
        raise HTTPException(status_code=404, detail="Test suite not found")

    # Create comparison job
    comparison = models.Comparison(
        test_suite_id=request.test_suite_id,
        model_a=request.model_a,
        model_b=request.model_b,
        status="running"
    )

    db.add(comparison)
    db.commit()
    db.refresh(comparison)

    # Run comparison in background
    background_tasks.add_task(run_full_comparison, db, comparison)

    return comparison


@router.get("/{comparison_id}")
def get_comparison(
    comparison_id: UUID,
    db: Session = Depends(get_db)
):
    comparison = db.query(models.Comparison).filter(
        models.Comparison.id == comparison_id
    ).first()

    if not comparison:
        raise HTTPException(status_code=404, detail="Comparison not found")

    return comparison