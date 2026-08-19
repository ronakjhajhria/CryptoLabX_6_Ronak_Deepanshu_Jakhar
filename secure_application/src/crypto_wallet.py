import sqlite3

# Vulnerability 1: Hardcoded Secrets
# A hardcoded administrative token that could be extracted from the source code.
ADMIN_TOKEN = "super_admin_secret_999"

def init_db():
    conn = sqlite3.connect('wallet.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT,
            balance REAL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            receiver TEXT,
            amount REAL
        )
    ''')
    conn.commit()
    conn.close()

def create_wallet(username, password):
    conn = sqlite3.connect('wallet.db')
    cursor = conn.cursor()
    try:
        # Give 100 initial balance to new wallets for testing
        cursor.execute("INSERT INTO users (username, password, balance) VALUES (?, ?, ?)", (username, password, 100.0)) 
        conn.commit()
        print(f"Wallet created successfully for {username}!")
    except sqlite3.IntegrityError:
        print("Username already exists.")
    conn.close()

def balance_inquiry(target_username):
    # Vulnerability 2: Broken Access Control
    # Notice that we do not verify if the logged-in user matches the target_username.
    # Any user can check the balance of any other user.
    conn = sqlite3.connect('wallet.db')
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE username=?", (target_username,))
    result = cursor.fetchone()
    conn.close()
    if result:
        print(f"Balance for {target_username}: {result[0]} coins")
    else:
        print("User not found.")

def transaction_history(target_username):
    # Vulnerability 2: Broken Access Control
    # Similar to balance inquiry, any user can view the transaction history of anyone else.
    conn = sqlite3.connect('wallet.db')
    cursor = conn.cursor()
    cursor.execute("SELECT sender, receiver, amount FROM transactions WHERE sender=? OR receiver=?", (target_username, target_username))
    results = cursor.fetchall()
    conn.close()
    print(f"\n--- Transaction History for {target_username} ---")
    for row in results:
        print(f"Sender: {row[0]} | Receiver: {row[1]} | Amount: {row[2]}")
    print("---------------------------------------")

def transaction_request(sender, receiver, amount):
    conn = sqlite3.connect('wallet.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT balance FROM users WHERE username=?", (sender,))
    sender_result = cursor.fetchone()
    cursor.execute("SELECT balance FROM users WHERE username=?", (receiver,))
    receiver_result = cursor.fetchone()
    
    if sender_result and receiver_result:
        # Vulnerability 3: Input Validation Errors
        # We DO NOT check if the amount is negative. A malicious user could send a negative amount to steal funds.
        # We DO NOT check if the sender has sufficient balance (amount <= balance). 
        # A user can send money they don't have, resulting in a negative balance.
        
        new_sender_balance = sender_result[0] - float(amount)
        new_receiver_balance = receiver_result[0] + float(amount)
        
        cursor.execute("UPDATE users SET balance=? WHERE username=?", (new_sender_balance, sender))
        cursor.execute("UPDATE users SET balance=? WHERE username=?", (new_receiver_balance, receiver))
        cursor.execute("INSERT INTO transactions (sender, receiver, amount) VALUES (?, ?, ?)", (sender, receiver, amount))
        conn.commit()
        print("Transaction successful!")
    else:
        print("Invalid sender or receiver.")
    conn.close()

def main():
    init_db()
    current_user = None
    
    while True:
        print(f"\n--- Cryptocurrency Wallet (User: {current_user if current_user else 'Guest'}) ---")
        print("1. Create Wallet")
        print("2. Login")
        print("3. Balance Inquiry")
        print("4. Transaction Request")
        print("5. Transaction History")
        print("6. Exit")
        choice = input("Select an option: ")
        
        if choice == '1':
            user = input("Enter username: ")
            pwd = input("Enter password: ")
            create_wallet(user, pwd)
            
        elif choice == '2':
            user = input("Enter username: ")
            pwd = input("Enter password: ")
            conn = sqlite3.connect('wallet.db')
            cursor = conn.cursor()
            # Storing and checking plaintext passwords is bad, but cryptography is excluded for this lab.
            cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
            if cursor.fetchone():
                print("Login successful!")
                current_user = user
            else:
                print("Invalid credentials.")
            conn.close()
            
        elif choice == '3':
            user = input("Enter username for balance inquiry: ")
            balance_inquiry(user) 
            
        elif choice == '4':
            if not current_user:
                print("Please login first to send funds.")
                continue
            receiver = input("Enter receiver username: ")
            amount = input("Enter amount to send: ")
            try:
                transaction_request(current_user, receiver, float(amount))
            except ValueError:
                print("Invalid amount format. Must be a number.")
                
        elif choice == '5':
            user = input("Enter username for history: ")
            transaction_history(user) 
            
        elif choice == '6':
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
