from fastapi import APIRouter, status
from app import models

import app.train_newrating_predict as tnrp

router = APIRouter(prefix="/update", tags=["update"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def incrementallearn(playerdata: models.Incremental):
    tnrp.trainNewRating(playerdata.segement, playerdata.game, playerdata.totalrounds, playerdata.kd, playerdata.rating)