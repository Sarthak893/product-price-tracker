import requests
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

DB_NAME = "prices.db"

# ------------------------------
# Database Functions
# ------------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_name TEXT,
            url TEXT,
            price REAL,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_price(product_name, url, price):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        INSERT INTO price_history (product_name, url, price, timestamp)
        VALUES (?, ?, ?, ?)
    ''', (product_name, url, price, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_history():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT * FROM price_history ORDER BY timestamp DESC')
    rows = c.fetchall()
    conn.close()
    return rows

# ------------------------------
# Scraping Function
# ------------------------------
def scrape_price(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(f"Error fetching page: {res.status_code}")
        return None, None

    soup = BeautifulSoup(res.text, "html.parser")

    # For Books to Scrape

    product_name = soup.find("div", class_="product_main").h1.get_text().strip()
    price_string = soup.find("p", class_="price_color").get_text().strip()
    print(f"[DEBUG] Raw price string : {price_string}")

    # Price is like '£51.77'
    price_numeric=''.join(c for c in price_string if c.isdigit() or c == '.')
    price_value = float(price_numeric)

    return product_name, price_value

# ------------------------------
# Main CLI
# ------------------------------
def main():
    init_db()

    print("=== Price Tracker ===")
    print("1. Track new product URL")
    print("2. Show history")
    choice = input("Choose an option (1 or 2): ")

    if choice == '1':
        url = input("Enter product URL: ").strip()
        try:
            name, price = scrape_price(url)
            if name and price:
                print(f"\nProduct: {name}")
                print(f"Price: £{price}")
                insert_price(name, url, price)
                print("✅ Price saved to database.\n")
            else:
                print("⚠️ Could not extract product details.")
        except Exception as e:
            print(f"Error: {e}")

    elif choice == '2':
        history = get_history()
        print("\n=== Price History ===")
        for row in history:
            print(f"{row[4]} | {row[1]} | £{row[3]} | {row[2]}")
    else:
        print("Invalid choice.")

if __name__ == '__main__':
    main()
