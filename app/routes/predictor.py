from fastapi import APIRouter, status
from app import models
from app.ml import predictor as prdctr

router = APIRouter(prefix="/predictor", tags=["predictor"])

# Predictor API

# Get Predictions
@router.post("/", status_code=status.HTTP_201_CREATED)
async def make_predictions(player: models.PredictMLInput):
    player=player.model_dump()
    features={'total_rounds': player['total_rounds'], 'kd': player['kd']}
    predictor= await prdctr.Predictor(player.segment, player.game, features)
    
    return predictor.prediction
