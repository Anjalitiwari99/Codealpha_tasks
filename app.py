from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__)

# Portfolio file path
PORTFOLIO_FILE = 'portfolio.csv'

def get_prices():
    """
    Returns the hardcoded dictionary of stock prices.
    """
    return {
        "AAPL": 150.00,
        "TSLA": 250.50,
        "GOOGL": 2800.00,
        "MSFT": 300.00,
        "AMZN": 3300.00
    }

def load_portfolio():
    """
    Loads the portfolio from the CSV file.
    Returns a list of dictionaries.
    """
    portfolio = []
    if os.path.exists(PORTFOLIO_FILE):
        try:
            with open(PORTFOLIO_FILE, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Convert types back from string
                    row['quantity'] = float(row['quantity'])
                    row['price'] = float(row['price'])
                    row['total_value'] = float(row['total_value'])
                    portfolio.append(row)
        except Exception as e:
            print(f"Error loading portfolio: {e}")
    return portfolio

def save_portfolio(portfolio):
    """
    Saves the portfolio to the CSV file.
    """
    try:
        with open(PORTFOLIO_FILE, mode='w', newline='') as file:
            fieldnames = ["ticker", "quantity", "price", "total_value"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for item in portfolio:
                writer.writerow(item)
    except IOError as e:
        print(f"Error saving portfolio: {e}")

@app.route("/", methods=["GET", "POST"])
def index():
    prices = get_prices()
    portfolio = load_portfolio()
    error = None

    if request.method == "POST":
        ticker = request.form.get("ticker").upper()
        try:
            quantity = float(request.form.get("quantity"))
            
            if ticker not in prices:
                error = f"Error: {ticker} not found. Available: {', '.join(prices.keys())}"
            elif quantity < 0:
                error = "Error: Quantity cannot be negative."
            else:
                price = prices[ticker]
                total_value = price * quantity
                
                # Add to portfolio
                new_item = {
                    "ticker": ticker,
                    "quantity": quantity,
                    "price": price,
                    "total_value": total_value
                }
                portfolio.append(new_item)
                save_portfolio(portfolio)
                
        except ValueError:
            error = "Error: Invalid quantity."

    grand_total = sum(item['total_value'] for item in portfolio)
    
    return render_template("index.html", portfolio=portfolio, grand_total=grand_total, error=error)

if __name__ == "__main__":
    app.run(debug=True)
