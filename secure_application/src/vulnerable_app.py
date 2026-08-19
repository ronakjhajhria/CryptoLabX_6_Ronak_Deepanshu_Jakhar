import os
import sqlite3
import hashlib

# 1. Hardcoded Credentials
DB_USERNAME = "admin"
DB_PASSWORD = "super_secret_password_123"

def connect_db():
    # Connect to a dummy sqlite database
    conn = sqlite3.connect('test_app.db')
    return conn

def hash_password(password):
    # 2. Weak Cryptography (MD5)
    # MD5 is considered cryptographically broken and vulnerable to collision attacks
    hasher = hashlib.md5()
    hasher.update(password.encode('utf-8'))
    return hasher.hexdigest()

def get_user_data(username):
    conn = connect_db()
    cursor = conn.cursor()
    
    # 3. SQL Injection Vulnerability
    # Using string formatting directly into the SQL query is highly insecure
    query = f"SELECT * FROM users WHERE username = '{username}'"
    
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except sqlite3.Error as e:
        return str(e)
    finally:
        conn.close()

def ping_host(hostname):
    # 4. Command Injection Vulnerability
    # Passing user input directly to a system shell command is extremely dangerous
    command = f"ping -c 1 {hostname}"
    print(f"Executing: {command}")
    
    # Using os.system with untrusted input
    os.system(command)

if __name__ == "__main__":
    print("Running Vulnerable Application...")
    print("Database Credentials:", DB_USERNAME, DB_PASSWORD)
    
    hashed_pwd = hash_password("my_password")
    print(f"Hashed password: {hashed_pwd}")
    
    # Simulating malicious user input
    malicious_user = "admin' OR '1'='1"
    print(f"Fetching data for: {malicious_user}")
    print(get_user_data(malicious_user))
    
    # Simulating command injection
    malicious_host = "127.0.0.1; whoami"
    ping_host(malicious_host)
