# backend/app/routers/prompts.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID
from app.db import get_db
from app import schemas, crud

router = APIRouter(prefix="/test-suites/{suite_id}/prompts", tags=["Prompts"])


@router.post("/", response_model=schemas.PromptResponse)
def add_prompt(
    suite_id: UUID,
    prompt: schemas.PromptCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new prompt for the given test suite.
    """
    return crud.create_prompt(db, suite_id, prompt)


@router.get("/", response_model=list[schemas.PromptResponse])
def list_prompts(suite_id: UUID, db: Session = Depends(get_db)):
    """
    List all prompts for a given test suite.
    Ensures that metadata is serialized as a dictionary.
    """
    try:
        prompts = crud.get_prompts_by_suite(db, suite_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch prompts: {e}")

    serialized_prompts = []
    for p in prompts:
        # Convert metadata to dict for JSON serialization
        metadata_dict = (
            p.metadata.dict()  # if MetaData is a Pydantic model
            if hasattr(p.metadata, "dict")
            else dict(p.metadata)  # fallback for other objects
        )

        serialized_prompts.append(
            schemas.PromptResponse(
                id=p.id,
                input_text=p.input_text,
                expected_output=p.expected_output,
                metadata=metadata_dict,
                created_at=p.created_at
            )
        )

    return serialized_prompts