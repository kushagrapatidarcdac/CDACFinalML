from fastapi import APIRouter, status
from app import models
from app.ml import recommender as rcmndr

router = APIRouter(prefix="/predictor", tags=["predictor"])

# Predictor API

# Get Predictions
@router.post("/", status_code=status.HTTP_201_CREATED)
async def get_recommendations(player: models.RecommendMLInput):
    player=player.model_dump()
    recommender= await rcmndr.Recommender(player.segment, player.game, player.player_name, player.k)
    
    return recommender.recommendations