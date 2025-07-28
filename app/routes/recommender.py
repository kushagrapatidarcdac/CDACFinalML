from fastapi import APIRouter, status
from app import models
from app.ml import recommender as rcmndr

router = APIRouter(prefix="/recommender", tags=["recommender"])

# Recommender API

# Get Recommmendations
@router.post("/", status_code=status.HTTP_201_CREATED)
async def get_recommendations(player: models.RecommendMLInput):
    recommender= rcmndr.Recommender(player.segment, player.game, player.player_name, player.k)
    
    return recommender.recommendations
    
    # Test Output Data
    # return player.model_dump()
    
    