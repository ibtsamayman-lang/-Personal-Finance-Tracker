import sqlite3
from pathlib import Path

from models import Transaction

DB_PATH = Path("data/finance.db")

# أوامر انشاء الجداول
SCHEMA = """
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT NOT NULL,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    note TEXT,
    date TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS budgets (
    category TEXT PRIMARY KEY,
    monthly_limit REAL NOT NULL
);
"""


class Database:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        conn = self.connect()
        conn.executescript(SCHEMA)
        conn.commit()
        conn.close()

    def connect(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def add_transaction(self, t):
        conn = self.connect()
        cur = conn.execute(
            "INSERT INTO transactions (type, category, amount, note, date, created_at) VALUES (?, ?, ?, ?, ?, ?)",
            (t.type, t.category, t.amount, t.note, t.date, t.created_at),
        )
        conn.commit()
        new_id = cur.lastrowid
        conn.close()
        return new_id

    def get_all_transactions(self):
        conn = self.connect()
        rows = conn.execute("SELECT * FROM transactions ORDER BY date DESC, id DESC").fetchall()
        conn.close()
        result = []
        for r in rows:
            result.append(Transaction(**dict(r)))
        return result

    def delete_transaction(self, transaction_id):
        conn = self.connect()
        conn.execute("DELETE FROM transactions WHERE id=?", (transaction_id,))
        conn.commit()
        conn.close()

    def clear_all(self):
        conn = self.connect()
        conn.execute("DELETE FROM transactions")
        conn.execute("DELETE FROM budgets")
        conn.commit()
        conn.close()

    def set_budget(self, category, monthly_limit):
        conn = self.connect()
        conn.execute(
            "INSERT INTO budgets (category, monthly_limit) VALUES (?, ?) "
            "ON CONFLICT(category) DO UPDATE SET monthly_limit=excluded.monthly_limit",
            (category, monthly_limit),
        )
        conn.commit()
        conn.close()

    def get_budgets(self):
        conn = self.connect()
        rows = conn.execute("SELECT * FROM budgets").fetchall()
        conn.close()
        budgets = {}
        for r in rows:
            budgets[r["category"]] = r["monthly_limit"]
        return budgets