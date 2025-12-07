# Summary: This module contains the user interface and logic for a console-based version of the stock manager program.

from datetime import datetime
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart
from os import path
import stock_data


# Main Menu
def main_menu(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Stock Analyzer ---")
        print("1 - Manage Stocks (Add, Update, Delete, List)")
        print("2 - Add Daily Stock Data (Date, Price, Volume)")
        print("3 - Show Report")
        print("4 - Show Chart")
        print("5 - Manage Data (Save, Load, Retrieve)")
        print("0 - Exit Program")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","5","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("Stock Analyzer ---")
            print("1 - Manage Stocks (Add, Update, Delete, List)")
            print("2 - Add Daily Stock Data (Date, Price, Volume)")
            print("3 - Show Report")
            print("4 - Show Chart")
            print("5 - Manage Data (Save, Load, Retrieve)")
            print("0 - Exit Program")
            option = input("Enter Menu Option: ")
        if option == "1":
            manage_stocks(stock_list)
        elif option == "2":
            add_stock_data(stock_list)
        elif option == "3":
            display_report(stock_list)
        elif option == "4":
            display_chart(stock_list)
        elif option == "5":
            manage_data(stock_list)
        else:
            print("Goodbye! Thank you using Stock Analyzer.")

# Manage Stocks
def manage_stocks(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Stocks ---")
        print("1 - Add Stock")
        print("2 - Update Shares")
        print("3 - Delete Stock")
        print("4 - List Stocks")
        print("0 - Exit Manage Stocks")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("1 - Add Stock")
            print("2 - Update Shares")
            print("3 - Delete Stock")
            print("4 - List Stocks")
            print("0 - Exit Manage Stocks")
            option = input("Enter Menu Option: ")
        if option == "1":
            add_stock(stock_list)
        elif option == "2":
            update_shares(stock_list)
        elif option == "3":
            delete_stock(stock_list)
        elif option == "4":
            list_stocks(stock_list)
        else:
            print("Returning to Main Menu")

# Add new stock to track
def add_stock(stock_list):
    clear_screen()
    print("Add Stock ---")
    symbol = input("Enter stock symbol: ").upper().strip()
    if not symbol:
        print("Invalid symbol")
        input("Press Enter to Continue")
        return
        
    # Check if stock already exists
    for stock in stock_list:
        if stock.symbol == symbol:
            print(f"Stock {symbol} already exists in portfolio")
            input("Press Enter to Continue")
            return
    
    name = input("Enter company name: ").strip()
    if not name:
        print("Invalid company name")
        input("Press Enter to Continue")
        return
        
    try:
        shares = float(input("Enter number of shares: "))
        new_stock = Stock(symbol, name, shares)
        stock_list.append(new_stock)
        print(f"Stock {symbol} added successfully!")
    except ValueError:
        print("Invalid number of shares")
    input("Press Enter to Continue")
        
# Buy or Sell Shares Menu
def update_shares(stock_list):
    option = ""
    while option != "0":
        pass


# Buy Stocks (add to shares)
def buy_stock(stock_list):
    clear_screen()
    print("Buy Shares ---")
    print("Stock List: [",end="")
    pass

# Sell Stocks (subtract from shares)
def sell_stock(stock_list):
    clear_screen()
    pass

# Remove stock and all daily data
def delete_stock(stock_list):
    clear_screen()
    pass


# List stocks being tracked
def list_stocks(stock_list):
    clear_screen()
    print("Stock List ---")
    
    if len(stock_list) == 0:
        print("No stocks in portfolio")
    else:
        print(f"{'Symbol':<8} {'Name':<25} {'Shares':<15} {'Data Records':<12}")
        print("-" * 60)
        for stock in stock_list:
            print(f"{stock.symbol:<8} {stock.name:<25} {stock.shares:<15.0f} {len(stock.DataList):<12}")
        print(f"\nTotal stocks: {len(stock_list)}")
    
    input("Press Enter to Continue")

# Add Daily Stock Data
def add_stock_data(stock_list):
    clear_screen()
    pass

# Display Report for All Stocks
def display_report(stock_data):
    clear_screen()
    print("Stock Report ---")
    print("=" * 60)
    
    if len(stock_data) == 0:
        print("No stocks in portfolio")
        input("Press Enter to Continue")
        return
    
    for stock in stock_data:
        print(f"\nStock: {stock.symbol} - {stock.name}")
        print(f"Shares: {stock.shares:,.0f}")
        print("-" * 40)
        
        if len(stock.DataList) > 0:
            # Sort data by date
            sorted_data = sorted(stock.DataList, key=lambda x: x.date)
            
            print(f"{'Date':<12} {'Price':<12} {'Volume':<15}")
            print("-" * 40)
            
            for daily_data in sorted_data:
                print(f"{daily_data.date.strftime('%m/%d/%y'):<12} ${daily_data.close:<11.2f} {daily_data.volume:>14,.0f}")
            
            # Calculate statistics
            prices = [data.close for data in sorted_data]
            current_price = prices[-1]
            start_price = prices[0]
            high_price = max(prices)
            low_price = min(prices)
            
            price_change = current_price - start_price
            percent_change = (price_change / start_price) * 100 if start_price != 0 else 0
            portfolio_value = current_price * stock.shares
            
            print("-" * 40)
            print(f"Current Price: ${current_price:.2f}")
            print(f"Price Range: ${low_price:.2f} - ${high_price:.2f}")
            print(f"Price Change: ${price_change:+.2f} ({percent_change:+.1f}%)")
            print(f"Portfolio Value: ${portfolio_value:,.2f}")
            print(f"Records: {len(sorted_data)}")
        else:
            print("No price data available")
            print("Use Manage Data -> Retrieve Data from Web to get historical data")
        
        print("=" * 60)
    
    input("Press Enter to Continue")


  


# Display Chart
def display_chart(stock_list):
    clear_screen()
    print("Display Chart ---")
    
    if len(stock_list) == 0:
        print("No stocks in portfolio")
        input("Press Enter to Continue")
        return
    
    print("Stock List: [", end="")
    for i, stock in enumerate(stock_list):
        if i > 0:
            print(", ", end="")
        print(stock.symbol, end="")
    print("]")
    
    symbol = input("Enter stock symbol to chart: ").upper().strip()
    
    # Find the stock
    found_stock = None
    for stock in stock_list:
        if stock.symbol == symbol:
            found_stock = stock
            break
    
    if not found_stock:
        print(f"Stock {symbol} not found in portfolio")
        input("Press Enter to Continue")
        return
    
    if len(found_stock.DataList) == 0:
        print(f"No price data available for {symbol}")
        print("Use Manage Data -> Retrieve Data from Web to get historical data")
        input("Press Enter to Continue")
        return
    
    try:
        display_stock_chart(stock_list, symbol)
        print(f"Chart displayed for {symbol}")
    except Exception as e:
        print(f"Error displaying chart: {str(e)}")
    
    input("Press Enter to Continue")

# Manage Data Menu
def manage_data(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Manage Data ---")
        print("1 - Save Data to Database")
        print("2 - Load Data from Database")
        print("3 - Retrieve Data from Yahoo! Finance")
        print("4 - Import CSV Data from Yahoo! Finance")
        print("0 - Exit Manage Data")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","3","4","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("Manage Data ---")
            print("1 - Save Data to Database")
            print("2 - Load Data from Database")
            print("3 - Retrieve Data from Yahoo! Finance")
            print("4 - Import CSV Data from Yahoo! Finance")
            print("0 - Exit Manage Data")
            option = input("Enter Menu Option: ")
        if option == "1":
            save_data(stock_list)
        elif option == "2":
            load_data(stock_list)
        elif option == "3":
            retrieve_from_web(stock_list)
        elif option == "4":
            import_csv(stock_list)
        else:
            print("Returning to Main Menu")


# Save stock data to database
def save_data(stock_list):
    clear_screen()
    print("Saving Data to Database ---")
    try:
        stock_data.save_stock_data(stock_list)
        print("Data saved successfully!")
    except Exception as e:
        print(f"Error saving data: {str(e)}")
    input("Press Enter to Continue")

# Load stock data from database
def load_data(stock_list):
    clear_screen()
    print("Loading Data from Database ---")
    try:
        stock_data.load_stock_data(stock_list)
        print(f"Data loaded successfully! {len(stock_list)} stocks loaded.")
    except Exception as e:
        print(f"Error loading data: {str(e)}")
    input("Press Enter to Continue")

# Get stock price and volume history from Yahoo! Finance using Web Scraping
def retrieve_from_web(stock_list):
    clear_screen()
    print("Retrieving Stock Data from Yahoo! Finance ---")
    print("This will retrieve data from all stocks in your stock list.")
    
    # Check if there are any stocks to process
    if len(stock_list) == 0:
        print("No stocks in your portfolio. Please add stocks first.")
        input("Press Enter to Continue")
        return
    
    # Get date range from user
    start_date = input("Enter Starting Date: (MM/DD/YY): ")
    end_date = input("Enter Ending Date: (MM/DD/YY): ")
    
    try:
        # Call the web scraping function from stock_data module
        record_count = stock_data.retrieve_stock_web(start_date, end_date, stock_list)
        print(f"Records Retrieved: {record_count}")
    except Exception as e:
        print(f"Error retrieving data: {str(e)}")
        print("Please check your Chrome Driver installation and internet connection.")
    
    input("Press Enter to Continue")

# Import stock price and volume history from Yahoo! Finance using CSV Import
def import_csv(stock_list):
    clear_screen()
    print("Import CSV file from Yahoo! Finance Selected ---")
    
    if len(stock_list) == 0:
        print("No stocks in your portfolio. Please add stocks first.")
        input("Press Enter to Continue")
        return
    
    # Display stock list
    print("Stock List: [", end="")
    for i, stock in enumerate(stock_list):
        if i > 0:
            print(", ", end="")
        print(stock.symbol, end="")
    print("]")
    
    # Get stock selection from user
    symbol = input("Which stock do you want to use?: ").upper().strip()
    
    # Find the stock
    found_stock = None
    for stock in stock_list:
        if stock.symbol == symbol:
            found_stock = stock
            break
    
    if not found_stock:
        print(f"Stock {symbol} not found in portfolio")
        input("Press Enter to Continue")
        return
    
    # Get filename from user
    filename = input("Enter filename: ").strip()
    
    if not filename:
        print("Invalid filename")
        input("Press Enter to Continue")
        return
    
    try:
        # Call the CSV import function from stock_data module
        stock_data.import_stock_web_csv(stock_list, symbol, filename)
        print("CSV File Imported")
    except FileNotFoundError:
        print(f"File not found: {filename}")
    except Exception as e:
        print(f"Error importing CSV file: {str(e)}")
    
    input("Press Enter to Continue")

# Begin program
def main():
    #check for database, create if not exists
    if path.exists("stocks.db") == False:
        stock_data.create_database()
    stock_list = []
    main_menu(stock_list)

# Program Starts Here
if __name__ == "__main__":
    # execute only if run as a stand-alone script
    main()