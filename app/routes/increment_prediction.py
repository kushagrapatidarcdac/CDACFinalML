from fastapi import APIRouter, status
from app import models
from pprint import pprint

router = APIRouter(prefix="/incrementpredictor", tags=["incrementpredictor"])

# Incremental Trainer

# Create Incremental Trainer API
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(newdata: models.IncrementalMLInput):
    segment=newdata.segment
    game=newdata.game
    data={
        "player_name": newdata.player_name,
        "country": newdata.country,
        "team": newdata.team,
        "total_rounds": newdata.total_rounds,
        "kd": newdata.kd,
        "rating": newdata.rating
        
    }
    
    payload={
        "segment": segment,
        "game": game,
        "data": data
    }
    pprint(payload)
    
    return {"status": "Not Available...\nRoute Under Development"}
