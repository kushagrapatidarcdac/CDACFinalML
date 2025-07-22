from fastapi import APIRouter, status
from app import models

import app.predict_rating as pr

router = APIRouter(prefix="/predictrating", tags=["predictrating"])


@router.get("/", status_code=status.HTTP_200_OK)
def predictrating(playerdata: models.PredictData):
    print("Prediction Request Received")
    rating = pr.predict_rating(playerdata.segment, playerdata.game, playerdata.totalrounds, playerdata.kd)
    print(f"Predicted Rating: {rating}")
    return {"rating": rating}