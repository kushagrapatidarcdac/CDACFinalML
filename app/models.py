from pydantic import BaseModel
from typing import Dict

class PredictData(BaseModel):
    segment: str
    game: str
    totalrounds: int
    kd: float

class Incremental(PredictData):
    rating: float

class Recommend(BaseModel):
    data: Dict
    player_id: str
    player_segement: str
    game: str
    n: int =5