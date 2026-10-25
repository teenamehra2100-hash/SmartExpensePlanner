from database.db import get_connection
from models.transaction import Transaction
from models.budget import Budget

class ExpenseManager:
    
    def add_transaction(self, transaction: Transaction):
        """Validates and saves a new transaction to the database."""
        is_valid, message = transaction.is_valid()
        if not is_valid:
            return False, message

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO transactions (date, type, category, amount, description)
            VALUES (?, ?, ?, ?, ?)
        ''', (transaction.date, transaction.type, transaction.category, 
              transaction.amount, transaction.description))
        
        conn.commit()
        conn.close()
        return True, "Transaction added successfully!"

    def get_all_transactions(self):
        """Retrieves all transactions from the database."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM transactions ORDER BY date DESC")
        rows = cursor.fetchall()
        conn.close()
        
        # Convert database rows into our Transaction OOP objects
        transactions = []
        for row in rows:
            transactions.append(Transaction(
                id=row['id'],
                date=row['date'],
                type=row['type'],
                category=row['category'],
                amount=row['amount'],
                description=row['description']
            ))
        return transactions

    def delete_transaction(self, transaction_id):
        """Deletes a transaction by its ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
        conn.commit()
        conn.close()
        return True, "Transaction deleted."


    def add_budget(self, budget: Budget):
        """Saves or updates a budget for a category."""
        conn = get_connection()
        cursor = conn.cursor()
        
        # INSERT OR REPLACE handles both new budgets and updating existing ones
        # We use .title() so "food", "Food", and "FOOD" all become "Food"
        cursor.execute(
            "INSERT OR REPLACE INTO budgets (category, monthly_limit) VALUES (?, ?)",
            (budget.category.title(), budget.monthly_limit)
        )
        
        conn.commit()
        conn.close()
        return True, "Budget saved!"

    def get_all_budgets(self):
        """Retrieves all budgets from the database."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM budgets")
        rows = cursor.fetchall()
        conn.close()
        
        # Convert database rows into our Budget OOP objects
        budgets = []
        for row in rows:
            budgets.append(Budget(
                category=row['category'],
                monthly_limit=row['monthly_limit']
            ))
        return budgets