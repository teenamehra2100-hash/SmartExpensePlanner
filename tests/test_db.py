from services.expense_manager import ExpenseManager
from models.transaction import Transaction

manager = ExpenseManager()

# 1. Create a fake transaction object
new_tx = Transaction(
    date="2026-10-25", 
    type="expense", 
    category="Food", 
    amount=15.50, 
    description="Lunch at cafe"
)

# 2. Try to save it using our OOP manager
success, message = manager.add_transaction(new_tx)
print(f"Save status: {success} - {message}")

# 3. Try to retrieve all transactions
all_tx = manager.get_all_transactions()
print(f"\nTotal transactions in database: {len(all_tx)}")
for tx in all_tx:
    print(f"[{tx.date}] {tx.category}: ${tx.amount} ({tx.description})")