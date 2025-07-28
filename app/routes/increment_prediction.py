from fastapi import APIRouter, status
from app import models

router = APIRouter(prefix="/incrementpredictor", tags=["incrementpredictor"])

# Incremental Trainer

# Create Incremental Trainer API
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(newdata: models.IncrementalMLInput):
    print("Under Development")
    return {"Not Available": "Route Under Development"}
