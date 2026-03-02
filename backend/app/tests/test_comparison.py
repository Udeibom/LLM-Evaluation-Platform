import uuid
from app.services.comparison import compare_experiments
from app import models


def test_compare_experiments(db_session):
    # Create experiments
    exp_a = models.Experiment(id=uuid.uuid4(), name="A")
    exp_b = models.Experiment(id=uuid.uuid4(), name="B")

    db_session.add_all([exp_a, exp_b])
    db_session.commit()

    # Create prompts
    prompt_ids = [uuid.uuid4() for _ in range(3)]

    # Create outputs for A
    for i, pid in enumerate(prompt_ids):
        output = models.Output(
            experiment_id=exp_a.id,
            prompt_id=pid,
        )
        db_session.add(output)
        db_session.flush()

        evaluation = models.Evaluation(
            output_id=output.id,
            score=i  # 0, 1, 2
        )
        db_session.add(evaluation)

    # Create outputs for B
    for i, pid in enumerate(prompt_ids):
        output = models.Output(
            experiment_id=exp_b.id,
            prompt_id=pid,
        )
        db_session.add(output)
        db_session.flush()

        evaluation = models.Evaluation(
            output_id=output.id,
            score=2 - i  # 2, 1, 0
        )
        db_session.add(evaluation)

    db_session.commit()

    result = compare_experiments(db_session, exp_a.id, exp_b.id)

    assert result["total_prompts"] == 3
    assert result["wins_a"] == 1
    assert result["wins_b"] == 1
    assert result["ties"] == 1