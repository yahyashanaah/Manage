from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import expenses, categories
from database import create_tables

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    create_tables()

app.include_router(categories.router, prefix="/categories", tags=["Categories"])
app.include_router(expenses.router, prefix="/expenses", tags=["Expenses"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Expense Tracker API!"}
