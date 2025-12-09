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
        print("Welcome to the Stock Analyzer Application! --")
        print("Please select from the following options:")
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
        input("")
        return
        
    # Check if stock already exists
    for stock in stock_list:
        if stock.symbol == symbol:
            print(f"Stock {symbol} already exists in your portfolio")
            input("")
            return
    
    # Company name input
    name = input("Enter company name: ").strip()
    if not name:
        print("Invalid company name")
        input("")
        return
        
    # Number of shares input
    try:
        shares = float(input("Enter number of shares: "))
        new_stock = Stock(symbol, name, shares)
        stock_list.append(new_stock)
        print(f"Stock {symbol} added successfully!")
    except ValueError:
        print("Invalid number of shares")
    input("")

#Recheck these methods
# Buy or Sell Shares Menu
def update_shares(stock_list):
    option = ""
    while option != "0":
        clear_screen()
        print("Update Shares ---")
        print("1 - Buy Shares")
        print("2 - Sell Shares")
        print("0 - Exit Update Shares")
        option = input("Enter Menu Option: ")
        while option not in ["1","2","0"]:
            clear_screen()
            print("*** Invalid Option - Try again ***")
            print("Update Shares ---")
            print("1 - Buy Shares")
            print("2 - Sell Shares")
            print("0 - Exit Update Shares")
            option = input("Enter Menu Option: ")
        if option == "1":
            buy_stock(stock_list)
        elif option == "2":
            sell_stock(stock_list)
        else:
            print("Returning to Main Menu")


# Buy Stocks (add to shares)
def buy_stock(stock_list):
    clear_screen()
    print("Buy Shares ---")
    
    if len(stock_list) == 0:
        print("No stocks in portfolio")
        return
    
    print("Stock List: [", end="")
    for i, stock in enumerate(stock_list):
        if i > 0:
            print(", ", end="")
        print(stock.symbol, end="")
    print("]")
    
    symbol = input("Enter stock symbol: ").upper().strip()
    
    # Find the stock
    found_stock = None
    for stock in stock_list:
        if stock.symbol == symbol:
            found_stock = stock
            break
    
    if not found_stock:
        print(f"Stock {symbol} not found in portfolio")
        return
    
    try:
        shares = float(input("Enter number of shares to buy: "))
        if shares <= 0:
            print("Number of shares must be positive")
            return
        
        found_stock.buy(shares)
        print(f"Successfully bought {shares} shares of {symbol}")
        print(f"Total shares now: {found_stock.shares}")
    except ValueError:
        print("Invalid number of shares")

# Sell Stocks (subtract from shares)
def sell_stock(stock_list):
    clear_screen()
    print("Sell Shares ---")
    
    if len(stock_list) == 0:
        print("No stocks in portfolio")
        return
    
    print("Stock List: [", end="")
    for i, stock in enumerate(stock_list):
        if i > 0:
            print(", ", end="")
        print(stock.symbol, end="")
    print("]")
    
    symbol = input("Enter stock symbol: ").upper().strip()
    
    # Find the stock
    found_stock = None
    for stock in stock_list:
        if stock.symbol == symbol:
            found_stock = stock
            break
    
    if not found_stock:
        print(f"Stock {symbol} not found in portfolio")
        return
    
    try:
        shares = float(input("Enter number of shares to sell: "))
        if shares <= 0:
            print("Number of shares must be positive")
            return
        
        if shares > found_stock.shares:
            print(f"Cannot sell {shares} shares. You only have {found_stock.shares} shares")
            return
        
        found_stock.sell(shares)
        print(f"Successfully sold {shares} shares of {symbol}")
        print(f"Remaining shares: {found_stock.shares}")
    except ValueError:
        print("Invalid number of shares")

# Remove stock and all daily data
def delete_stock(stock_list):
    clear_screen()
    print("Delete Stock ---")
    
    if len(stock_list) == 0:
        print("No stocks in portfolio")
        return
    
    print("Stock List: [", end="")
    for i, stock in enumerate(stock_list):
        if i > 0:
            print(", ", end="")
        print(stock.symbol, end="")
    print("]")
    
    symbol = input("Enter stock symbol to delete: ").upper().strip()
    
    # Find the stock
    stock_to_delete = None
    stock_index = -1
    for i, stock in enumerate(stock_list):
        if stock.symbol == symbol:
            stock_to_delete = stock
            stock_index = i
            break
    
    if not stock_to_delete:
        print(f"Stock {symbol} not found in portfolio")
        return
    
    # delete stock
    stock_list.pop(stock_index)
    print(f"Stock {symbol} deleted successfully")


# List stocks being tracked
def list_stocks(stock_list):
    clear_screen()
    print("--- Stock Portfolio ---")
    
    # Setting appropriate column widths for display
    print(f"{'Symbol':<8} {'Name':<25} {'Shares':<15} {'Data Records':<12}")
    print("=" * 60)
    for stock in stock_list:
        print(f"{stock.symbol:<8} {stock.name:<25} {stock.shares:<15.0f} {len(stock.DataList):<12}")
    print(f"\nTotal stocks: {len(stock_list)}")
    
    input("Press Enter to Continue")

# Add Daily Stock Data
def add_stock_data(stock_list):
    clear_screen()
    print("Add Daily Stock Data ---")
    
    if len(stock_list) == 0:
        print("No stocks in portfolio")
        input("")
        return
    
    print("Stock List: [", end="")
    for i, stock in enumerate(stock_list):
        if i > 0:
            print(", ", end="")
        print(stock.symbol, end="")
    print("]")
    
    symbol = input("Enter stock symbol: ").upper().strip()
    
    # Find the stock
    found_stock = None
    for stock in stock_list:
        if stock.symbol == symbol:
            found_stock = stock
            break
    
    if not found_stock:
        print(f"Stock {symbol} not found in portfolio")
        input("")
        return
    
    # Get date input
    date_str = input("Enter date (MM/DD/YY): ").strip()
    try:
        date_obj = datetime.strptime(date_str, "%m/%d/%y")
    except ValueError:
        print("Invalid date format. Please use MM/DD/YY")
        input("")
        return
    
    # Get price input
    try:
        price = float(input("Enter closing price: $"))
        if price <= 0:
            print("Price must be positive")
            input("")
            return
    except ValueError:
        print("Invalid price")
        input("")
        return
    
    # Get volume input
    try:
        volume = float(input("Enter volume: "))
        if volume < 0:
            print("Volume cannot be negative")
            input("")
            return
    except ValueError:
        print("Invalid volume")
        input("")
        return
    
    # Create and add daily data
    daily_data = DailyData(date_obj, price, volume)
    found_stock.add_data(daily_data)
    print(f"Daily data added successfully for {symbol}")
    print(f"Date: {date_obj.strftime('%m/%d/%y')}, Price: ${price:.2f}, Volume: {volume:,.0f}")
    input("")

# Display Report for All Stocks
def display_report(stock_data):
    clear_screen()
    print("Stock Report ---")
    print("=" * 60)
    
    if len(stock_data) == 0:
        print("No stocks in portfolio")
        input("")
        return
    
    for stock in stock_data:
        print(f"\nStock: {stock.symbol} - {stock.name}")
        print(f"Shares: {stock.shares:,.0f}")
        print("=" * 60)
        
        if len(stock.DataList) > 0:
            sorted_data = sorted(stock.DataList, key=lambda x: x.date) # sorting by date
            
            # Setting appropriate column widths for display
            print(f"{'Date':<12} {'Price':<12} {'Volume':<15}")
            print("=" * 60)
            
            for daily_data in sorted_data:
                print(f"{daily_data.date.strftime('%m/%d/%y'):<12} ${daily_data.close:<11.2f} {daily_data.volume:>14,.0f}")
            
            # calculate and display stats
            prices = [data.close for data in sorted_data]
            current_price = prices[-1]
            start_price = prices[0]
            high_price = max(prices)
            low_price = min(prices)
            
            price_change = current_price - start_price
            if start_price != 0:
                percent_change = (price_change / start_price) * 100  
            else:
                percent_change = 0
            portfolio_value = current_price * stock.shares
            
            print("=" * 60)
            print(f"Current Price: ${current_price:.2f}")
            print(f"Price Range: ${low_price:.2f} - ${high_price:.2f}")
            print(f"Price Change: ${price_change:+.2f} ({percent_change:+.1f}%)")
            print(f"Portfolio Value: ${portfolio_value:,.2f}")
            print(f"Records: {len(sorted_data)}")
        else:
            print("No price data available")
            print("Use Manage Data -> Retrieve Data from Web to get historical data")
        
        print("=" * 60)
    
    input("")


# Display Chart
def display_chart(stock_list):
    clear_screen()
    print("Display Chart ---")
    
    if len(stock_list) == 0:
        print("No stocks in portfolio")
        input("")
        return
    
    print("Stock List: [", end="")
    # printing stock symbols
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
        input("")
        return
    
    if len(found_stock.DataList) == 0:
        print(f"No price data available for {symbol}")
        print("Use Retrieve Data from Web to get historical data Feature")
        input("")
        return
    
    try:
        display_stock_chart(stock_list, symbol)
        print(f"Chart displayed for {symbol}")
    except Exception as e:
        print(f"Error displaying chart: {str(e)}")
    
    input("")

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
    input("")

# Load stock data from database
def load_data(stock_list):
    clear_screen()
    print("Loading Data from Database ---")
    try:
        stock_data.load_stock_data(stock_list)
        print(f"Data loaded successfully! {len(stock_list)} stocks loaded.")
    except Exception as e:
        print(f"Error loading data: {str(e)}")
    input("")

# Get stock price and volume history from Yahoo! Finance using Web Scraping
def retrieve_from_web(stock_list):
    clear_screen()
    print("Retrieving Stock Data from Yahoo! Finance ---")
    
    # Check if there are any stocks to process
    if len(stock_list) == 0:
        print("No stocks in your portfolio. Please add stocks first.")
        input("")
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
    
    input("")

# Import stock price and volume history from Yahoo! Finance using CSV Import
def import_csv(stock_list):
    clear_screen()
    print("Import CSV file from Yahoo! Finance Selected ---")
    
    if len(stock_list) == 0:
        print("No stocks in your portfolio. Please add stocks first.")
        return
    
    # Displaying stock list
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
        input("")
        return
    
    # Get filename from user
    filename = input("Enter filename: ").strip()
    
    if not filename:
        print("Invalid filename")
        input("")
        return
    
    try:
        stock_data.import_stock_web_csv(stock_list, symbol, filename)
        print("CSV File Imported")
    except FileNotFoundError:
        print(f"File not found: {filename}")
    except Exception as e:
        print(f"Error importing CSV file: {str(e)}")
    
    input("")

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