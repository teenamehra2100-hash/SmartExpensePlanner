import sqlite3
import random
import datetime
from database.db import DB_PATH

def seed_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Clear existing data so we start fresh (Optional, but good for a clean demo)
    cursor.execute("DELETE FROM transactions")
    cursor.execute("DELETE FROM budgets")
    
    categories = {
        "Food": (10, 80),
        "Transport": (5, 40),
        "Entertainment": (15, 100),
        "Shopping": (20, 150),
        "Bills": (50, 200)
    }
    
    today = datetime.date.today()
    
    # Generate data for the past 6 months
    for i in range(180):
        date = today - datetime.timedelta(days=i)
        
        # 1. Add a monthly salary on the 1st of every month
        if date.day == 1:
            cursor.execute(
                "INSERT INTO transactions (date, type, category, amount, description) VALUES (?, ?, ?, ?, ?)",
                (date.strftime('%Y-%m-%d'), 'income', 'Salary', 3000.00, 'Monthly Paycheck')
            )
        
        # 2. Add 1 or 2 random expenses per day
        if random.random() > 0.3: # 70% chance to spend money on a given day
            cat = random.choice(list(categories.keys()))
            min_val, max_val = categories[cat]
            amount = round(random.uniform(min_val, max_val), 2)
            
            cursor.execute(
                "INSERT INTO transactions (date, type, category, amount, description) VALUES (?, ?, ?, ?, ?)",
                (date.strftime('%Y-%m-%d'), 'expense', cat, amount, f"Random {cat} expense")
            )

    # Add some budgets
    cursor.execute("INSERT INTO budgets (category, monthly_limit) VALUES ('Food', 600)")
    cursor.execute("INSERT INTO budgets (category, monthly_limit) VALUES ('Entertainment', 300)")
    
    conn.commit()
    conn.close()
    print("Database seeded with 6 months of realistic data!")

if __name__ == "__main__":
    seed_database()