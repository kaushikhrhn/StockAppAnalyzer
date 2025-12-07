#Helper Functions

import matplotlib.pyplot as plt

from os import system, name

# Function to Clear the Screen
def clear_screen():
    if name == "nt": # User is running Windows
        _ = system('cls')
    else: # User is running Linux or Mac
        _ = system('clear')

# Function to sort the stock list (alphabetical)
def sortStocks(stock_list):
    stock_list.sort(key=lambda x: x.symbol)


# Function to sort the daily stock data (oldest to newest) for all stocks
def sortDailyData(stock_list):
    for stock in stock_list:
        stock.DataList.sort(key=lambda x: x.date)

# Function to create stock chart
def display_stock_chart(stock_list,symbol):
    for stock in stock_list:
        if stock.symbol == symbol:
            if len(stock.DataList) > 0:
                # Sort data by date
                sorted_data = sorted(stock.DataList, key=lambda x: x.date)
                dates = [data.date for data in sorted_data]
                prices = [data.close for data in sorted_data]
                
                plt.figure(figsize=(12, 6))
                plt.plot(dates, prices, 'b-', linewidth=2, markersize=4)
                plt.title(f'{stock.name} ({stock.symbol}) - Stock Price History', fontsize=14)
                plt.xlabel('Date', fontsize=12)
                plt.ylabel('Price ($)', fontsize=12)
                plt.grid(True, alpha=0.3)
                plt.xticks(rotation=45)
                plt.tight_layout()
                
                # Format y-axis to show dollar signs
                plt.gca().yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'${x:.2f}'))
                
                plt.show()
            else:
                print(f"No data available for {symbol}")
            break
    else:
        print(f"Stock {symbol} not found")