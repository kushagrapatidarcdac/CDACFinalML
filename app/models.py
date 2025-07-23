from pydantic import BaseModel
from typing import List, Optional

class Dataset(BaseModel):
    id: str
    features: List[float]
    label: Optional[int]

class MLInput(BaseModel):
    data: List[float]

class MLOutput(BaseModel):
    prediction: int

class RecommendRequest(BaseModel):
    user_id: str
    top_k: int = 10

class RecommendResponse(BaseModel):
    recommendations: List[str]
