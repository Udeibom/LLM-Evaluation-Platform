from sqlalchemy import Column, Integer, String, Float
from app.db import Base


class ModelRating(Base):
    __tablename__ = "model_ratings"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String, unique=True, nullable=False)

    elo_rating = Column(Float, default=1000)

    matches_played = Column(Integer, default=0)

    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    ties = Column(Integer, default=0)