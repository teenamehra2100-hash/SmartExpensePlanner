from dataclasses import dataclass

@dataclass
class Transaction:
    date: str
    type: str       # 'income' or 'expense'
    category: str
    amount: float
    description: str = ""
    id: int = None

    def is_valid(self):
        if self.type not in ['income', 'expense']:
            return False, "Type must be 'income' or 'expense'."
        if self.amount <= 0:
            return False, "Amount must be greater than zero."
        if not self.date:
            return False, "Date is required."
        return True, "Valid"