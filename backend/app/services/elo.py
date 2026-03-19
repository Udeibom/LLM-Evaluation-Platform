# backend/app/services/elo.py

K = 32


def expected_score(rating_a: float, rating_b: float) -> float:
    """
    Calculate the expected score for player/model A.
    """
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))


def update_elo(rating_a: float, rating_b: float, score_a: float):
    """
    Update ELO ratings after a match.

    score_a:
        1   -> A wins
        0   -> B wins
        0.5 -> tie
    """

    exp_a = expected_score(rating_a, rating_b)
    exp_b = expected_score(rating_b, rating_a)

    new_a = rating_a + K * (score_a - exp_a)
    new_b = rating_b + K * ((1 - score_a) - exp_b)

    return round(new_a, 2), round(new_b, 2)