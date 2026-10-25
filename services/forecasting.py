import pandas as pd
from sklearn.linear_model import LinearRegression
from database.db import get_connection
import numpy as np

class ExpenseForecaster:
    def predict_next_month(self):
        """Uses Linear Regression to predict next month's total expenses."""
        conn = get_connection()
        # Get only expenses
        df = pd.read_sql_query("SELECT date, amount FROM transactions WHERE type = 'expense'", conn)
        conn.close()

        if df.empty or len(df) < 15:
            return None # Not enough data to train

        # Convert date string to datetime and extract the month (YYYY-MM)
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M')

        # Group by month and sum the expenses
        monthly_spending = df.groupby('month')['amount'].sum().reset_index()

        if len(monthly_spending) < 2:
            return None # Need at least 2 months to find a trend

        
        X = np.array(range(1, len(monthly_spending) + 1)).reshape(-1, 1)
        # y is the actual spending amount
        y = monthly_spending['amount'].values

        # Train the Linear Regression model
        model = LinearRegression()
        model.fit(X, y)

        # Predict the next month (e.g., if we have 6 months, predict month 7)
        next_month_index = len(monthly_spending) + 1
        prediction = model.predict([[next_month_index]])[0]

        # Ensure prediction isn't negative (which can happen mathematically)
        prediction = max(0, prediction)

        return {
            "predicted_amount": round(prediction, 2),
            "months_analyzed": len(monthly_spending),
            "trend": "up" if model.coef_[0] > 0 else "down"
        }