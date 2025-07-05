import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime
import logging

# CONFIGURE LOGGING

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# DATABASE SETUP

conn = sqlite3.connect('prices.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL,
        price TEXT NOT NULL,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')
conn.commit()


# DB OPERATIONS

def save_to_db(url, price):
    logging.info(f"Saving to DB: URL={url}, Price={price}")
    cursor.execute(
        "INSERT INTO prices (url, price, date) VALUES (?, ?, ?)",
        (url, price, datetime.now())
    )
    conn.commit()
    logging.info("Saved successfully.")

def view_price_history():
    logging.info("Fetching price history from DB")
    cursor.execute("SELECT * FROM prices")
    rows = cursor.fetchall()
    if not rows:
        print("No price history found.")
    else:
        for row in rows:
            print(row)


# CLI MENU

def main_menu():
    while True:
        print("\n--- Product Price Tracker CLI ---")
        print("1. Add Product Price")
        print("2. View Price History")
        print("3. Exit")
        choice = input("Enter choice: ").strip()

        logging.info(f"User selected option {choice}")

        if choice == "1":
            url = input("Enter product URL: ").strip()
            price = input("Enter product price: ").strip()
            save_to_db(url, price)
        elif choice == "2":
            view_price_history()
        elif choice == "3":
            logging.info("Exiting application.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main_menu()
