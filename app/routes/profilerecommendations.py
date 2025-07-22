from fastapi import APIRouter, status
from app import models

import app.recommend_players as rp

router = APIRouter(prefix="/profilerecommendations", tags=["profilerecommendations"])


@router.get("/", status_code=status.HTTP_200_OK)
def playerrecommend(playerdata: models.Recommend):
    playerids = rp.recommendPlayers(playerdata.data, playerdata.player_id, playerdata.player_segement, playerdata.game, playerdata.n)
    return {"Player IDs": playerids}