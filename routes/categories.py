from fastapi import APIRouter
from crud import create_category, delete_category, get_categories, update_category
from models import CategoryCreate, CategoryResponse

router = APIRouter()

@router.post("/", response_model=CategoryResponse)
async def add_category(category: CategoryCreate):
    return create_category(category)

@router.get("/", response_model=list[CategoryResponse])
async def list_categories():
    return get_categories()

@router.put("/{category_id}", response_model=CategoryResponse)
async def edit_category(category_id: int, updated_category: CategoryCreate):
    return update_category(category_id, updated_category)

@router.delete("/{category_id}")
async def remove_category(category_id: int):
    return delete_category(category_id)