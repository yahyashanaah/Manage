from fastapi import APIRouter, HTTPException
from crud import create_item, get_all_items, get_item_by_id, get_items_by_month, update_item, delete_item
from models import ItemCreate, ItemResponse

router = APIRouter()

@router.post("/", response_model=ItemResponse)
async def create_item_route(item: ItemCreate):
    return create_item(item)

@router.get("/", response_model=list[ItemResponse])
async def read_items():
    return get_all_items()

@router.get("/{item_id}", response_model=ItemResponse)
async def read_item(item_id: int):
    item = get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.get("/month/{month}", response_model=list[ItemResponse])
async def read_items_by_month(month: str):
    return get_items_by_month(month)

@router.put("/{item_id}", response_model=ItemResponse)
async def update_item_route(item_id: int, updated_item: ItemCreate):
    return update_item(item_id, updated_item)

@router.delete("/{item_id}")
async def delete_item_route(item_id: int):
    return delete_item(item_id)
