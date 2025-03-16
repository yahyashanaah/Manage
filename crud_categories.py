from database import get_db
from models import CategoryCreate


# Category Section 

# ✅ Add new category
def create_category(category: CategoryCreate):
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO categories (name) VALUES (?)", (category.name,))
        conn.commit()
        return {"id": cursor.lastrowid, "name": category.name}

# ✅ Get all categories
def get_categories():
    with get_db() as conn:
        categories = conn.execute("SELECT * FROM categories").fetchall()
        return [dict(cat) for cat in categories]

def update_category(category_id: int, updated_category: CategoryCreate):
    with get_db() as conn:
        conn.execute("""
        UPDATE categories SET name = ? WHERE id = ?
        """, (updated_category.name, category_id))
        conn.commit()
        return {"id": category_id, "name": updated_category.name}


def delete_category(category_id: int):
    with get_db() as conn:
        conn.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        conn.commit()
        return {"message": "Category deleted successfully"}