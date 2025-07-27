from fastapi import APIRouter, Path, Query, status
from app import crud, models

router = APIRouter(prefix="/incrementpredictor", tags=["incrementpredictor"])

# Orders API

# Create Order API
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(order: models.Order):
    oid = await crud.create_order(order.model_dump())
    return {"id": oid}

# Get List of Orders
@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def list_orders(
    user_id: str = Path(..., description="User ID whose orders to retrieve"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    orders = await crud.get_orders(user_id, limit, offset)
    next_offset = offset + limit
    return {
        "orders": orders,
        "page": {
            "next": next_offset,
            "limit": limit,
            "previous": offset if offset > 0 else None,
        }
    }
