import sqlite3
from typing import List, Optional, Tuple


class Database:
    def __init__(self, db_path: str = "config/main.db"):
        self.db_path = db_path
        self.init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    price REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def add_product(self, name: str, description: str = "", price: float = 0.0) -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO products (name, description, price) VALUES (?, ?, ?)",
                (name, description, price)
            )
            conn.commit()
            return cursor.lastrowid

    def get_all_products(self) -> List[Tuple]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, description, price FROM products ORDER BY id")
            return cursor.fetchall()

    def get_product(self, product_id: int) -> Optional[Tuple]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, description, price FROM products WHERE id = ?",
                (product_id,)
            )
            return cursor.fetchone()

    def delete_product(self, product_id: int) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
            conn.commit()
            return cursor.rowcount > 0

    def update_product(self, product_id: int, name: str = None, description: str = None, price: float = None) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()

            # Get current product data
            current = self.get_product(product_id)
            if not current:
                return False

            # Update only provided fields
            new_name = name if name is not None else current[1]
            new_description = description if description is not None else current[2]
            new_price = price if price is not None else current[3]

            cursor.execute(
                "UPDATE products SET name = ?, description = ?, price = ? WHERE id = ?",
                (new_name, new_description, new_price, product_id)
            )
            conn.commit()
            return cursor.rowcount > 0