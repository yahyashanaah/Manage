from fastapi import APIRouter
from crud import create_expense, delete_expense, get_expenses, get_expenses_by_month, update_expense
from models import ExpenseCreate, ExpenseResponse

router = APIRouter()

@router.post("/", response_model=ExpenseResponse)
async def add_expense(expense: ExpenseCreate):
    return create_expense(expense)

@router.get("/", response_model=list[ExpenseResponse])
async def list_expenses():
    return get_expenses()

@router.get("/month/{month}", response_model=list[ExpenseResponse])
async def expenses_by_month(month: str):
    return get_expenses_by_month(month)

@router.put("/{expense_id}", response_model=ExpenseResponse)
async def edit_expense(expense_id: int, updated_expense: ExpenseCreate):
    return update_expense(expense_id, updated_expense)

@router.delete("/{expense_id}")
async def remove_expense(expense_id: int):
    return delete_expense(expense_id)
