import sqlite3
from tabulate import tabulate  # helps make the data look nice in the terminal

# Trying to connect to a database (or it makes one if it doesn't exist)
conn = sqlite3.connect('finance.db')
cursor = conn.cursor()

# This creates a table to store our transactions (only if it's not already there)
cursor.execute('''
CREATE TABLE IF NOT EXISTS transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    description TEXT,
    amount REAL
)
''')
conn.commit()

# Function to add a new transaction to the table
def add_transaction():
    print("\nAdd a New Transaction")
    # These are the details we collect from the user
    date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter category (e.g. Food, Rent, Salary): ")
    description = input("Enter a short description: ")
    
    # Trying to turn the amount into a number
    try:
        amount = float(input("Enter amount (negative = expense, positive = income): "))
    except ValueError:
        print("Invalid number. Please try again.")
        return  # stops the function if input is wrong

    # This adds the data to the database
    cursor.execute('''
    INSERT INTO transactions (date, category, description, amount)
    VALUES (?, ?, ?, ?)
    ''', (date, category, description, amount))

    conn.commit()
    print("✅ Transaction added!\n")

# Function to show all past transactions
def view_transactions():
    cursor.execute('SELECT * FROM transactions ORDER BY date DESC')
    rows = cursor.fetchall()

    # If there are any transactions, show them in a table
    if rows:
        print("\nAll Transactions:\n")
        print(tabulate(rows, headers=["ID", "Date", "Category", "Description", "Amount"], tablefmt="pretty"))
    else:
        print("\nYou have no transactions saved yet.\n")

# Function to show a summary by category (how much spent/earned)
def show_summary():
    cursor.execute('''
    SELECT category, SUM(amount)
    FROM transactions
    GROUP BY category
    ''')
    rows = cursor.fetchall()

    print("\nSummary by Category:\n")
    print(tabulate(rows, headers=["Category", "Total Amount"], tablefmt="pretty"))

# This is the main loop that keeps the app running
def main():
    while True:
        print("\n==============================")
        print("📊 Personal Finance Tracker")
        print("==============================")
        print("1. Add a transaction")
        print("2. View all transactions")
        print("3. View summary by category")
        print("4. Exit")
        print("==============================")

        choice = input("Choose an option (1-4): ")

        # Depending on what the user picks, we run a different function
        if choice == '1':
            add_transaction()
        elif choice == '2':
            view_transactions()
        elif choice == '3':
            show_summary()
        elif choice == '4':
            print("👋 Goodbye! Stay on top of your finances!")
            break
        else:
            print("Oops! That's not a valid option. Try again.")

# This makes sure the app runs only when this file is executed directly
if __name__ == '__main__':
    main()

