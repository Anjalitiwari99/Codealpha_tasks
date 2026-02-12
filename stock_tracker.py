import csv
import os

def create_price_dict():
    """
    Creates a hardcoded dictionary of stock prices.
    Returns:
        dict: A dictionary where keys are stock symbols (str) and values are prices (float).
    """
    return {
        "AAPL": 150.00,
        "TSLA": 250.50,
        "GOOGL": 2800.00,
        "MSFT": 300.00,
        "AMZN": 3300.00
    }

def get_user_portfolio(price_dict):
    """
    Prompts the user for stock symbols and quantities.
    Args:
        price_dict (dict): Dictionary of available stock prices.
    Returns:
        list: A list of dictionaries, each containing 'ticker', 'quantity', 'price', and 'total_value'.
    """
    portfolio = []
    print("Welcome to the Stock Portfolio Tracker!")
    print("Available stocks: " + ", ".join(price_dict.keys()))
    
    while True:
        ticker = input("\nEnter stock symbol (or 'done' to finish): ").upper()
        if ticker == 'DONE':
            break
        
        if ticker not in price_dict:
            print(f"Error: {ticker} not found in price list.")
            continue
        
        try:
            quantity_str = input(f"Enter quantity for {ticker}: ")
            quantity = float(quantity_str)
            if quantity < 0:
                print("Quantity cannot be negative.")
                continue
        except ValueError:
            print("Invalid quantity. Please enter a number.")
            continue
            
        price = price_dict[ticker]
        total_value = price * quantity
        portfolio.append({
            "ticker": ticker,
            "quantity": quantity,
            "price": price,
            "total_value": total_value
        })
        print(f"Added {quantity} shares of {ticker} at ${price:.2f} each. Total: ${total_value:.2f}")

    return portfolio

def save_portfolio(portfolio, filename="portfolio.csv"):
    """
    Saves the portfolio to a CSV file.
    Args:
        portfolio (list): List of portfolio items.
        filename (str): Name of the file to save to.
    """
    if not portfolio:
        print("No portfolio data to save.")
        return

    try:
        with open(filename, mode='w', newline='') as file:
            fieldnames = ["ticker", "quantity", "price", "total_value"]
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            
            writer.writeheader()
            for item in portfolio:
                writer.writerow(item)
        print(f"\nPortfolio saved to {filename}")
    except IOError as e:
        print(f"Error saving to file: {e}")

def main():
    prices = create_price_dict()
    portfolio = get_user_portfolio(prices)
    
    grand_total = sum(item['total_value'] for item in portfolio)
    
    print("\n--- Portfolio Summary ---")
    for item in portfolio:
        print(f"{item['ticker']}: {item['quantity']} shares @ ${item['price']:.2f} = ${item['total_value']:.2f}")
    
    print(f"\nGrand Total Portfolio Value: ${grand_total:.2f}")
    
    save_portfolio(portfolio)

if __name__ == "__main__":
    main()
