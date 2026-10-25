import matplotlib
matplotlib.use('Agg') # Required for generating charts on a server
import matplotlib.pyplot as plt
import pandas as pd
import io
import base64
from database.db import get_connection

class Analytics:
    def generate_category_chart(self):
        """Generates a base64 encoded Matplotlib bar chart of expenses by category."""
        conn = get_connection()
        df = pd.read_sql_query("SELECT * FROM transactions WHERE type = 'expense'", conn)
        conn.close()

        if df.empty:
            return None

        # Capitalize the first letter so "food" and "Food" merge together
        df['category'] = df['category'].str.title()

        # Group by category and sum the amounts
        category_spending = df.groupby('category')['amount'].sum().sort_values(ascending=False)

        # Create the Matplotlib chart
        plt.figure(figsize=(7, 4))
        
        # Use colors that match your Quiet Luxury palette
        colors = ['#315C50', '#C6A66B', '#B9C9B5', '#172B2A', '#6B7A78']
        top_categories = category_spending.head(5)
        
        bars = plt.bar(top_categories.index, top_categories.values, color=colors[:len(top_categories)], width=0.4)
        
        plt.title('Top Expense Categories', color='#2D3736', fontsize=14, pad=15)
        plt.xlabel('Category', color='#2D3736')
        plt.ylabel('Amount ($)', color='#2D3736')
        
        # Add the dollar amount text on top of each bar
        for bar in bars:
            yval = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2, yval + 0.5, f'${yval:.2f}', 
                     ha='center', va='bottom', color='#2D3736', fontweight='bold')

        # THE FIX: Stop a single bar from stretching across the whole screen
        plt.xlim(-1, len(top_categories))

        # Clean up the look
        plt.tight_layout()
        ax = plt.gca()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#B9C9B5')
        ax.spines['bottom'].set_color('#B9C9B5')

        # Save the plot to a memory buffer
        img = io.BytesIO()
        plt.savefig(img, format='png', transparent=True, dpi=150)
        img.seek(0)
        
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()
        
        return plot_url