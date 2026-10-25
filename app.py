from flask import Flask, render_template, request, redirect, url_for
from services.expense_manager import ExpenseManager
from services.analytics import Analytics
from services.forecasting import ExpenseForecaster
from models.transaction import Transaction
from models.budget import Budget
import datetime

app = Flask(__name__)

# Initialize all services
manager = ExpenseManager()
analytics = Analytics()
forecaster = ExpenseForecaster()

@app.route("/")
def dashboard():
    # 1. Get Data
    all_transactions = manager.get_all_transactions()
    
    # 2. Calculate Totals
    total_income = sum(t.amount for t in all_transactions if t.type == 'income')
    total_expense = sum(t.amount for t in all_transactions if t.type == 'expense')
    balance = total_income - total_expense
    recent = all_transactions[:5] 
    
    # 3. Generate Chart (Matplotlib)
    chart_url = analytics.generate_category_chart()
    
    # 4. Calculate Budgets
    budgets = manager.get_all_budgets()
    budget_data = []
    
    for b in budgets:
        spent = sum(t.amount for t in all_transactions if t.type == 'expense' and t.category.title() == b.category)
        remaining = b.monthly_limit - spent
        percent = min((spent / b.monthly_limit) * 100, 100) if b.monthly_limit > 0 else 0
        
        status = "safe"
        if remaining < 0:
            status = "danger"
        elif percent >= 80:
            status = "warning"

        budget_data.append({
            "category": b.category,
            "limit": b.monthly_limit,
            "spent": spent,
            "remaining": remaining,
            "percent": percent,
            "status": status
        })

    # 5. Generate ML Forecast (Scikit-Learn)
    forecast_data = forecaster.predict_next_month()

    today = datetime.date.today().strftime('%Y-%m-%d')
    
    # 6. Render the page with all the data
    return render_template("index.html", total_income=total_income, total_expense=total_expense,   balance=balance,
                              recent=recent,all_transactions=all_transactions , today=today, chart_url=chart_url, budget_data=budget_data,
                              forecast_data=forecast_data)

@app.route("/add", methods=["POST"])
def add():
    date = request.form.get("date")
    type_ = request.form.get("type")
    category = request.form.get("category")
    amount = float(request.form.get("amount"))
    description = request.form.get("description")

    new_tx = Transaction(date, type_, category, amount, description)
    manager.add_transaction(new_tx)
    
    return redirect(url_for("dashboard"))

@app.route("/add_budget", methods=["POST"])
def add_budget():
    category = request.form.get("category")
    limit = float(request.form.get("limit"))
    
    new_budget = Budget(category, limit)
    manager.add_budget(new_budget)
    
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True)