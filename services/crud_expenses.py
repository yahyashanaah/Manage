from database import get_db
from models import ExpenseCreate


# ✅ Add new expense
def create_expense(expense: ExpenseCreate):
    expense_month = expense.date.strftime("%Y-%m")
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO expenses (description, date, amount, category_id, month)
        VALUES (?, ?, ?, ?, ?)
        """, (expense.description, expense.date, expense.amount, expense.category_id, expense_month))
        conn.commit()
        return {**expense.dict(), "id": cursor.lastrowid, "month": expense_month}

# ✅ Get all expenses
def get_expenses():
    with get_db() as conn:
        expenses = conn.execute("SELECT * FROM expenses").fetchall()
        return [dict(exp) for exp in expenses]

# ✅ Get expenses by month
def get_expenses_by_month(month: str):
    with get_db() as conn:
        expenses = conn.execute("SELECT * FROM expenses WHERE month = ?", (month,)).fetchall()
        return [dict(exp) for exp in expenses]

def update_expense(expense_id: int, updated_expense: ExpenseCreate):
    expense_month = updated_expense.date.strftime("%Y-%m")
    with get_db() as conn:
        conn.execute("""
        UPDATE expenses SET 
            description = ?, 
            date = ?, 
            amount = ?, 
            category_id = ?, 
            month = ?
        WHERE id = ?
        """, (updated_expense.description, updated_expense.date, updated_expense.amount, updated_expense.category_id, expense_month, expense_id))
        conn.commit()
        return {**updated_expense.dict(), "id": expense_id, "month": expense_month}

def delete_expense(expense_id: int):
    with get_db() as conn:
        conn.execute("DELETE FROM expenses WHERE id = ?", (expense_id,))
        conn.commit()
        return {"message": "Expense deleted successfully"}

