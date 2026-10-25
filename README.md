# Smart Expense & Budget Planner

A full-stack, personal finance web application that allows users to track income and expenses, set category budgets, visualize spending patterns, and predict future expenses using Machine Learning.

Designed with a UI philosophy: featuring a restrained color palette , whitespace, and clean typography.

## Features

*   Dashboard: Real-time overview of total balance, income, and expenses.
*   Transaction Manager: Add and categorize income and expenses securely stored in an SQLite database.
*   Analytics and Charts: Server-side generated visual charts using Matplotlib and Pandas to show spending breakdowns by category.
*   Budget Planner: Set monthly limits per category. Features dynamic progress bars that turn amber (warning) or red (danger) if you exceed your limit.
*   Machine Learning Forecasting: An optional ML layer using Scikit-Learn Linear Regression to predict next month's total expenses based on historical spending trends.
*   Single Page Application Feel: Seamless view switching between Dashboard, Transactions, and Budgets without full page reloads, powered by vanilla JavaScript.

## Tech Stack

*   Backend: Python 3, Flask
*   Database: SQLite 3
*   Data Science and ML: Pandas, NumPy, Matplotlib, Scikit-Learn
*   Frontend: HTML5, CSS3 (Custom Vanilla CSS), JavaScript
*   OOP: Classes for Transaction, Budget, and services like ExpenseManager, Analytics, and ExpenseForecaster.

## Project Structure

```text
smart-expense-planner/
│
├── app.py                  # Flask application entry point
├── requirements.txt        # Project dependencies
├── seed_data.py            # Script to generate 6 months of dummy data
│
├── models/                 # OOP Data models
│   ├── transaction.py
│   └── budget.py
│
├── services/               # Business logic and analytics
│   ├── expense_manager.py  # CRUD operations for DB
│   ├── analytics.py        # Matplotlib chart generation
│   └── forecasting.py      # Scikit-Learn ML prediction
│
├── database/               # Database connection and schema
│   ├── db.py
│   └── schema.sql
│
├── templates/              # Jinja2 HTML templates
│   └── index.html
│
└── static/                 # Frontend assets
    ├── style.css
    └── script.js
