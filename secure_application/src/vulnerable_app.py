import sqlite3

DB = "wallet.db"

ADMIN_PASSWORD = "admin123"

current_user = None


def init_db():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS wallets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            balance REAL NOT NULL DEFAULT 0
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender INTEGER NOT NULL,
            receiver INTEGER NOT NULL,
            amount REAL NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def register():
    print("\n===== USER REGISTRATION =====")

    username = input("Enter new username: ")
    password = input("Enter new password: ")

    if username == "" or password == "":
        print("Username and password cannot be empty.")
        return

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users(username, password) VALUES (?, ?)",
            (username, password)
        )

        user_id = cur.lastrowid

        cur.execute(
            "INSERT INTO wallets(user_id, balance) VALUES (?, ?)",
            (user_id, 0)
        )

        conn.commit()

        print("Registration successful.")
        print("Your User ID is:", user_id)
        print("Wallet created with balance: 0")

    except sqlite3.IntegrityError:
        print("Username already exists.")

    finally:
        conn.close()


def login():
    global current_user

    username = input("Enter username: ")
    password = input("Enter password: ")

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "SELECT id, username FROM users "
        "WHERE username = ? AND password = ?",
        (username, password)
    )

    user = cur.fetchone()
    conn.close()

    if user:
        current_user = user[0]
        print("Login successful.")
        print("Welcome", user[1])
        print("User ID:", user[0])
    else:
        print("Invalid username or password.")


def create_wallet():
    if current_user is None:
        print("Please login first.")
        return

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM wallets WHERE user_id = ?",
        (current_user,)
    )

    wallet = cur.fetchone()

    if wallet:
        print("Wallet already exists.")
    else:
        cur.execute(
            "INSERT INTO wallets(user_id, balance) VALUES (?, ?)",
            (current_user, 0)
        )

        conn.commit()
        print("Wallet created successfully.")

    conn.close()


def balance():
    if current_user is None:
        print("Please login first.")
        return

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "SELECT balance FROM wallets WHERE user_id = ?",
        (current_user,)
    )

    wallet = cur.fetchone()
    conn.close()

    if wallet:
        print("Current balance:", wallet[0])
    else:
        print("Wallet not found.")


def deposit():
    if current_user is None:
        print("Please login first.")
        return

    amount = input("Enter deposit amount: ")

    try:
        amount = float(amount)
    except ValueError:
        print("Invalid amount.")
        return

    if amount <= 0:
        print("Amount must be positive.")
        return

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "UPDATE wallets SET balance = balance + ? WHERE user_id = ?",
        (amount, current_user)
    )

    conn.commit()
    conn.close()

    print("Deposit successful.")
    print("Deposited:", amount)


def transaction():
    if current_user is None:
        print("Please login first.")
        return

    receiver = input("Enter receiver user ID: ")
    amount = input("Enter amount: ")

    try:
        receiver = int(receiver)
        amount = float(amount)
    except ValueError:
        print("Invalid transaction input.")
        return

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "SELECT balance FROM wallets WHERE user_id = ?",
        (current_user,)
    )

    wallet = cur.fetchone()

    if wallet is None:
        print("Wallet not found.")
        conn.close()
        return

    balance_amount = wallet[0]

    if amount <= balance_amount:
        cur.execute(
            "UPDATE wallets SET balance = balance - ? WHERE user_id = ?",
            (amount, current_user)
        )

        cur.execute(
            "UPDATE wallets SET balance = balance + ? WHERE user_id = ?",
            (amount, receiver)
        )

        cur.execute(
            "INSERT INTO transactions(sender, receiver, amount) "
            "VALUES (?, ?, ?)",
            (current_user, receiver, amount)
        )

        conn.commit()

        print("Transaction completed successfully.")
    else:
        print("Insufficient balance.")

    conn.close()


def transaction_history():
    if current_user is None:
        print("Please login first.")
        return

    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    user_id = input("Enter user ID: ")

    try:
        user_id = int(user_id)
    except ValueError:
        print("Invalid user ID.")
        conn.close()
        return

    cur.execute(
        "SELECT sender, receiver, amount "
        "FROM transactions "
        "WHERE sender = ? OR receiver = ?",
        (user_id, user_id)
    )

    rows = cur.fetchall()
    conn.close()

    if not rows:
        print("No transactions found.")
        return

    print("\n===== TRANSACTION HISTORY =====")

    for row in rows:
        print(
            "Sender:", row[0],
            "Receiver:", row[1],
            "Amount:", row[2]
        )


def main():
    init_db()

    while True:
        print("\n================================")
        print("      CRYPTOCURRENCY WALLET")
        print("================================")

        print("1. Register")
        print("2. Login")
        print("3. Create Wallet")
        print("4. Balance Inquiry")
        print("5. Deposit")
        print("6. Transaction Request")
        print("7. Transaction History")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            register()
        elif choice == "2":
            login()
        elif choice == "3":
            create_wallet()
        elif choice == "4":
            balance()
        elif choice == "5":
            deposit()
        elif choice == "6":
            transaction()
        elif choice == "7":
            transaction_history()
        elif choice == "8":
            print("Exiting application...")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()