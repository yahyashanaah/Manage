from pydantic import BaseModel
from datetime import date

class CategoryCreate(BaseModel):
    name: str

class CategoryResponse(CategoryCreate):
    id: int

class ExpenseCreate(BaseModel):
    description: str
    date: date
    amount: float
    category_id: int

class ExpenseResponse(ExpenseCreate):
    id: int
    month: str

class TTSTextCreate(BaseModel):
    text: str
    language_id: int

class TTSTextResponse(TTSTextCreate):
    id: int
    audio_file: str
