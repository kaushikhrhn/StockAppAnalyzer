# Summary: This module contains the user interface and logic for a graphical user interface version of the stock manager program.

from datetime import datetime
from os import path
from tkinter import *
from tkinter import ttk
from tkinter import messagebox, simpledialog, filedialog
import csv
import stock_data
from stock_class import Stock, DailyData
from utilities import clear_screen, display_stock_chart, sortStocks, sortDailyData

class StockApp:
    def __init__(self):
        self.stock_list = []
        #check for database, create if not exists
        if path.exists("stocks.db") == False:
            stock_data.create_database()

        # Create Window
        self.root = Tk()
        self.root.title("Stock Analyzer Application")
        # self.root.geometry("800x600")  # Set a reasonable default size

        # Add Menubar
        self.menubar = Menu(self.root)

        # Add File Menu
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Load Data", command=self.load)
        self.filemenu.add_command(label="Save Data", command=self.save)
        self.menubar.add_cascade(label="File", menu=self.filemenu)

        # Add Web Menu
        self.webmenu = Menu(self.menubar, tearoff=0)
        self.webmenu.add_command(label="Scrape Data from Yahoo! Finance...", command=self.scrape_web_data)
        self.webmenu.add_command(label="Import CSV from Yahoo! Finance...", command=self.importCSV_web_data)
        self.menubar.add_cascade(label="Web", menu=self.webmenu)

        # Add Chart Menu
        self.chartmenu = Menu(self.menubar, tearoff=0)
        self.chartmenu.add_command(label="Display Stock Chart", command=self.display_chart)
        self.menubar.add_cascade(label="Chart", menu=self.chartmenu)

        # Add menus to window
        self.root.config(menu=self.menubar)

        # Add heading information
        self.headingLabel = Label(self.root, text="My Stock Portfolio", font=("Arial", 16, "bold"))
        self.headingLabel.pack(pady=10)

        # Add stock list
        self.stockFrame = Frame(self.root)
        self.stockFrame.pack(padx=10, pady=10, fill=BOTH, expand=True)
        
        Label(self.stockFrame, text="Stock List:", font=("Arial", 12, "bold")).pack(anchor=W)
        self.stockList = Listbox(self.stockFrame, height=6)
        self.stockList.pack(fill=X, pady=(5, 10))
        self.stockList.bind("<<ListboxSelect>>", self.update_data)
        
        # Add Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Set Up Main Tab
        self.mainTab = ttk.Frame(self.notebook)
        self.notebook.add(self.mainTab, text="Main")
        
        # Add stock controls (vertical layout)
        self.addFrame = LabelFrame(self.mainTab, text="Add New Stock", font=("Arial", 10, "bold"))
        self.addFrame.pack(fill=X, padx=10, pady=5)
        
        Label(self.addFrame, text="Symbol:").grid(row=0, column=0, sticky=W, padx=5, pady=2)
        self.addSymbolEntry = Entry(self.addFrame, width=30)
        self.addSymbolEntry.grid(row=0, column=1, sticky=W+E, padx=5, pady=2)
        
        Label(self.addFrame, text="Name:").grid(row=1, column=0, sticky=W, padx=5, pady=2)
        self.addNameEntry = Entry(self.addFrame, width=30)
        self.addNameEntry.grid(row=1, column=1, sticky=W+E, padx=5, pady=2)
        
        Label(self.addFrame, text="Shares:").grid(row=2, column=0, sticky=W, padx=5, pady=2)
        self.addSharesEntry = Entry(self.addFrame, width=30)
        self.addSharesEntry.grid(row=2, column=1, sticky=W+E, padx=5, pady=2)
        
        Button(self.addFrame, text="Add Stock", command=self.add_stock).grid(row=3, column=0, columnspan=2, pady=10)
        
        # Configure column weights for resizing
        self.addFrame.columnconfigure(1, weight=1)

        # Setup History Tab
        self.historyTab = ttk.Frame(self.notebook)
        self.notebook.add(self.historyTab, text="History")
        
        Label(self.historyTab, text="Stock Price History", font=("Arial", 12, "bold")).pack(pady=5)
        self.dailyDataList = Text(self.historyTab, height=15, width=50, font=("Courier", 10))
        self.dailyDataList.pack(fill=BOTH, expand=True, padx=10, pady=5)
        
        # Setup Report Tab
        self.reportTab = ttk.Frame(self.notebook)
        self.notebook.add(self.reportTab, text="Report")
        
        Label(self.reportTab, text="Stock Report", font=("Arial", 12, "bold")).pack(pady=5)
        self.stockReport = Text(self.reportTab, height=15, width=50, font=("Courier", 10))
        self.stockReport.pack(fill=BOTH, expand=True, padx=10, pady=5)


        ## Call MainLoop
        self.root.mainloop()

# This section provides the functionality
       
    # Load stocks and history from database.
    def load(self):
        self.stockList.delete(0,END)
        stock_data.load_stock_data(self.stock_list)
        sortStocks(self.stock_list)
        for stock in self.stock_list:
            self.stockList.insert(END,stock.symbol)
        messagebox.showinfo("Load Data","Data Loaded")

    # Save stocks and history to database.
    def save(self):
        stock_data.save_stock_data(self.stock_list)
        messagebox.showinfo("Save Data","Data Saved")

    # Refresh history and report tabs
    def update_data(self, evt):
        try:
            if self.stockList.curselection():
                self.display_stock_data()
        except:
            pass

    # Display stock price and volume history.
    def display_stock_data(self):
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
                self.dailyDataList.delete("1.0",END)
                self.stockReport.delete("1.0",END)
                
                # Display history data
                self.dailyDataList.insert(END,"    Date      Price      Volume\n")
                self.dailyDataList.insert(END,"=================================\n")
                for daily_data in stock.DataList:
                    row = daily_data.date.strftime("%m/%d/%y") + "   " + '${:8.2f}'.format(daily_data.close) + "   " + '{:,}'.format(int(daily_data.volume)) + "\n"
                    self.dailyDataList.insert(END,row)

                # display report
                if len(stock.DataList) > 0:
                    # Sorting the data for report
                    sorted_data = sorted(stock.DataList, key=lambda x: x.date)
                    
                    prices = [data.close for data in sorted_data]
                    volumes = [data.volume for data in sorted_data]
                    
                    current_price = prices[-1]
                    start_price = prices[0]
                    high_price = max(prices)
                    low_price = min(prices)
                    avg_price = sum(prices) / len(prices)
                    avg_volume = sum(volumes) / len(volumes)
                    
                    price_change = current_price - start_price
                    percent_change = (price_change / start_price) * 100 if start_price != 0 else 0
                    
                    
                    portfolio_value = current_price * stock.shares
                    
                    # Generate report
                    report = f"STOCK REPORT FOR {stock.symbol}\n"
                    report += f"="*40 + "\n"
                    report += f"Company: {stock.name}\n"
                    report += f"Shares Owned: {stock.shares:,.0f}\n\n"
                    
                    report += f"PRICE ANALYSIS\n"
                    report += f"-" * 20 + "\n"
                    report += f"Current Price: ${current_price:,.2f}\n"
                    report += f"Starting Price: ${start_price:,.2f}\n"
                    report += f"Highest Price: ${high_price:,.2f}\n"
                    report += f"Lowest Price: ${low_price:,.2f}\n"
                    report += f"Average Price: ${avg_price:,.2f}\n\n"
                    
                    report += f"PERFORMANCE\n"
                    report += f"-" * 20 + "\n"
                    report += f"Price Change: ${price_change:+,.2f}\n"
                    report += f"Percent Change: {percent_change:+.2f}%\n\n"
                    
                    report += f"PORTFOLIO VALUE\n"
                    report += f"-" * 20 + "\n"
                    report += f"Current Value: ${portfolio_value:,.2f}\n"
                    report += f"Average Volume: {avg_volume:,.0f}\n\n"
                    
                    report += f"DATA SUMMARY\n"
                    report += f"-" * 20 + "\n"
                    report += f"Records Available: {len(sorted_data)}\n"
                    report += f"Date Range: {sorted_data[0].date.strftime('%m/%d/%y')} to {sorted_data[-1].date.strftime('%m/%d/%y')}\n"
                    
                    self.stockReport.insert(END, report)
                else:
                    self.stockReport.insert(END, f"No price data available for {stock.symbol}\n\n")
                    self.stockReport.insert(END, "Use Scrape Data from Yahoo! Finance Feature\n")
                break


            
    # Add new stock to track.
    def add_stock(self):
        try:
            # input the stock symbol, name, and shares
            symbol = self.addSymbolEntry.get().upper().strip()
            name = self.addNameEntry.get().strip()
            shares = float(self.addSharesEntry.get())
            
            # Error checking and validations
            if not symbol or not name:
                messagebox.showerror("Error", "Please enter both symbol and name")
                return
                
            for stock in self.stock_list:
                if stock.symbol == symbol:
                    messagebox.showerror("Error", f"Stock {symbol} already exists")
                    return

            # Add stock to list
            new_stock = Stock(symbol, name, shares)
            self.stock_list.append(new_stock)
            self.stockList.insert(END, symbol)
            self.addSymbolEntry.delete(0,END)
            self.addNameEntry.delete(0,END)
            self.addSharesEntry.delete(0,END)
            messagebox.showinfo("Success", f"Added {symbol} to portfolio")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number of shares")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add stock: {str(e)}")

    # Buy shares of stock.
    def buy_shares(self):
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.buy(float(self.updateSharesEntry.get()))
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
        messagebox.showinfo("Buy Shares","Shares Purchased")
        self.updateSharesEntry.delete(0,END)

    # Sell shares of stock.
    def sell_shares(self):
        symbol = self.stockList.get(self.stockList.curselection())
        for stock in self.stock_list:
            if stock.symbol == symbol:
                stock.sell(float(self.updateSharesEntry.get()))
                self.headingLabel['text'] = stock.name + " - " + str(stock.shares) + " Shares"
        messagebox.showinfo("Sell Shares","Shares Sold")
        self.updateSharesEntry.delete(0,END)

    # Remove stock and all history from being tracked.
    def delete_stock(self):
        pass

    # Get data from web scraping.
    def scrape_web_data(self):
        dateFrom = simpledialog.askstring("Starting Date","Enter Starting Date (m/d/yy)")
        dateTo = simpledialog.askstring("Ending Date","Enter Ending Date (m/d/yy")
        try:
            stock_data.retrieve_stock_web(dateFrom,dateTo,self.stock_list)
        except:
            messagebox.showerror("Cannot Get Data from Web","Check Path for Chrome Driver")
            return
        self.display_stock_data()
        messagebox.showinfo("Get Data From Web","Data Retrieved")

    # Import CSV stock history file.
    def importCSV_web_data(self):
        symbol = self.stockList.get(self.stockList.curselection())
        filename = filedialog.askopenfilename(title="Select " + symbol + " File to Import",filetypes=[('Yahoo Finance! CSV','*.csv')])
        if filename != "":
            stock_data.import_stock_web_csv(self.stock_list,symbol,filename)
            self.display_stock_data()
            messagebox.showinfo("Import Complete",symbol + "Import Complete")   
    
    # Display stock price chart.
    def display_chart(self):
        symbol = self.stockList.get(self.stockList.curselection())
        display_stock_chart(self.stock_list,symbol)


def main():
        app = StockApp()
        

if __name__ == "__main__":
    # execute only if run as a script
    main()