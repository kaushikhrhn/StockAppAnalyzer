# Summary: This module contains the functions used by both console and GUI programs to manage stock data.


import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
import csv
import time
from datetime import datetime
from utilities import clear_screen
from utilities import sortDailyData
from stock_class import Stock, DailyData

# Create the SQLite database
def create_database():
    stockDB = "stocks.db"
    conn = sqlite3.connect(stockDB)
    cur = conn.cursor()
    createStockTableCmd = """CREATE TABLE IF NOT EXISTS stocks (
                            symbol TEXT NOT NULL PRIMARY KEY,
                            name TEXT,
                            shares REAL
                        );"""
    createDailyDataTableCmd = """CREATE TABLE IF NOT EXISTS dailyData (
                                symbol TEXT NOT NULL,
                                date TEXT NOT NULL,
                                price REAL NOT NULL,
                                volume REAL NOT NULL,
                                PRIMARY KEY (symbol, date)
                        );"""   
    cur.execute(createStockTableCmd)
    cur.execute(createDailyDataTableCmd)

# Save stocks and daily data into database
def save_stock_data(stock_list):
    stockDB = "stocks.db"
    conn = sqlite3.connect(stockDB)
    cur = conn.cursor()
    insertStockCmd = """INSERT INTO stocks
                            (symbol, name, shares)
                            VALUES
                            (?, ?, ?); """
    insertDailyDataCmd = """INSERT INTO dailyData
                                    (symbol, date, price, volume)
                                    VALUES
                                    (?, ?, ?, ?);"""
    for stock in stock_list:
        insertValues = (stock.symbol, stock.name, stock.shares)
        try:
            cur.execute(insertStockCmd, insertValues)
            cur.execute("COMMIT;")
        except:
            pass
        for daily_data in stock.DataList: 
            insertValues = (stock.symbol,daily_data.date.strftime("%m/%d/%y"),daily_data.close,daily_data.volume)
            try:
                cur.execute(insertDailyDataCmd, insertValues)
                cur.execute("COMMIT;")
            except:
                pass
    
# Load stocks and daily data from database
def load_stock_data(stock_list):
    stock_list.clear()
    stockDB = "stocks.db"
    conn = sqlite3.connect(stockDB)
    stockCur = conn.cursor()
    stockSelectCmd = """SELECT symbol, name, shares
                    FROM stocks; """
    stockCur.execute(stockSelectCmd)
    stockRows = stockCur.fetchall()
    for row in stockRows:
        new_stock = Stock(row[0],row[1],row[2])
        dailyDataCur = conn.cursor()
        dailyDataCmd = """SELECT date, price, volume
                        FROM dailyData
                        WHERE symbol=?; """
        selectValue = (new_stock.symbol)
        dailyDataCur.execute(dailyDataCmd,(selectValue,))
        dailyDataRows = dailyDataCur.fetchall()
        for dailyRow in dailyDataRows:
            daily_data = DailyData(datetime.strptime(dailyRow[0],"%m/%d/%y"),float(dailyRow[1]),float(dailyRow[2]))
            new_stock.add_data(daily_data)
        stock_list.append(new_stock)
    sortDailyData(stock_list)

# Get stock price history from web using Web Scraping
def retrieve_stock_web(dateStart,dateEnd,stock_list):
    dateFrom = str(int(time.mktime(time.strptime(dateStart,"%m/%d/%y"))))
    dateTo = str(int(time.mktime(time.strptime(dateEnd,"%m/%d/%y"))))
    recordCount = 0
    for stock in stock_list:
        stockSymbol = stock.symbol
        url = "https://finance.yahoo.com/quote/"+stockSymbol+"/history?period1="+dateFrom+"&period2="+dateTo+"&interval=1d&filter=history&frequency=1d"
        # Note this code assumes the use of the Chrome browser.
        # You will have to modify if you are using a different browser.
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches',['enable-logging'])
        options.add_experimental_option("prefs",{'profile.managed_default_content_settings.javascript': 2})
        
        # Set the path to chromedriver using the modern Service approach
        chromedriver_path = os.path.join(os.path.dirname(__file__), 'webdriver', 'chromedriver')
        service = Service(executable_path=chromedriver_path)
        
        try:
            driver = webdriver.Chrome(service=service, options=options)
            driver.implicitly_wait(60)
            driver.get(url)
        except Exception as e:
            raise RuntimeWarning(f"Chrome Driver Not Found: {str(e)}")

        soup = BeautifulSoup(driver.page_source,"html.parser")
        row = soup.find('table',class_="W(100%) M(0)")
        dataRows = soup.find_all('tr')
        for row in dataRows:
            td = row.find_all('td')
            rowList = [i.text for i in td]
            columnCount = len(rowList)
            if columnCount == 7: # This row is a standard data row (otherwise it's a special case such as dividend which will be ignored)
                daily_data = DailyData(datetime.strptime(rowList[0],"%b %d, %Y"),float(rowList[5].replace(',','')),float(rowList[6].replace(',','')))
                stock.add_data(daily_data)
                recordCount += 1
        
        # Close the browser window for this stock
        driver.quit()
    print("Retrieved "+str(recordCount)+" records from web.")
    return recordCount

# Get price and volume history from Yahoo! Finance using CSV import.
def import_stock_web_csv(stock_list,symbol,filename):
    record_count = 0
    for stock in stock_list:
        if stock.symbol == symbol:
            try:
                with open(filename, newline='', encoding='utf-8') as stockdata:
                    datareader = csv.reader(stockdata,delimiter=',')
                    header = next(datareader)  # Skip header row and get column info
                    print(f"CSV Header: {header}")  # Debug info
                    
                    for row in datareader:
                        if len(row) >= 5:  # Minimum columns needed: Date,Open,High,Low,Close,Volume
                            try:
                                # Handle different CSV formats
                                date_str = row[0].strip()
                                
                                # Determine close price and volume column indices based on CSV structure
                                if len(row) == 6:  # Format: Date,Open,High,Low,Close,Volume
                                    close_price_str = row[4].strip().replace('"', '').replace(',', '')
                                    volume_str = row[5].strip().replace('"', '').replace(',', '')
                                elif len(row) == 7:  # Format: Date,Open,High,Low,Close,Adj Close,Volume
                                    close_price_str = row[4].strip().replace('"', '').replace(',', '')
                                    volume_str = row[6].strip().replace('"', '').replace(',', '')
                                else:
                                    # Try to use Close as column 4 and Volume as last column
                                    close_price_str = row[4].strip().replace('"', '').replace(',', '')
                                    volume_str = row[-1].strip().replace('"', '').replace(',', '')
                                
                                close_price = float(close_price_str)
                                volume = float(volume_str)
                                
                                # Try different date formats
                                try:
                                    # Try MM/DD/YYYY format first (most common for your CSV)
                                    if '/' in date_str:
                                        daily_data = DailyData(datetime.strptime(date_str,"%m/%d/%Y"), close_price, volume)
                                    else:
                                        # Try YYYY-MM-DD format
                                        daily_data = DailyData(datetime.strptime(date_str,"%Y-%m-%d"), close_price, volume)
                                except ValueError as date_error:
                                    # Try other common formats
                                    try:
                                        daily_data = DailyData(datetime.strptime(date_str,"%Y-%m-%d"), close_price, volume)
                                    except ValueError:
                                        try:
                                            daily_data = DailyData(datetime.strptime(date_str,"%m/%d/%y"), close_price, volume)
                                        except ValueError:
                                            print(f"Could not parse date: {date_str} - {date_error}")
                                            continue
                                
                                stock.add_data(daily_data)
                                record_count += 1
                                
                            except (ValueError, IndexError) as e:
                                print(f"Skipping invalid row: {row} - Error: {e}")
                                continue
                                
                print(f"Imported {record_count} records for {symbol}")
                return record_count
            except FileNotFoundError:
                raise FileNotFoundError(f"CSV file not found: {filename}")
            except Exception as e:
                raise Exception(f"Error reading CSV file: {str(e)}")
    
    raise ValueError(f"Stock {symbol} not found in portfolio")

def main():
    # clear_screen()
    print("This module will handle data storage and retrieval.")

if __name__ == "__main__":
    # execute only if run as a stand-alone script
    main()