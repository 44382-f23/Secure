import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE = 'chat_app.db'


#Initialize the database

# Database initialization function (example)
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Creating the 'messages' table with 'timestamp'
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        message TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """)
    conn.commit()
    conn.close()

def add_timestamp_column():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Alter the table to add the timestamp column
    cursor.execute("ALTER TABLE messages ADD COLUMN timestamp DATETIME DEFAULT CURRENT_TIMESTAMP;")
    conn.commit()
    conn.close()


def register_user(username,password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()

    if user:
        conn.close()
        return False   
    
    hashed_password = generate_password_hash(password)
    
    cursor.execute("INSERT INTO users (username, password) VALUES (?,?)",(username, hashed_password))

    conn.commit()
    conn.close()
    return True

def check_user_password(username, entered_password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    stored_hash = cursor.fetchone()

    if stored_hash and check_password_hash(stored_hash[0], entered_password):
        conn.close()
        return True  # Password is correct
    conn.close()
    return False     #if password is incorrect 

def get_user_password(username):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def save_message(username, message):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages(username, message) VALUES (?,?)",(username, message))
    conn.commit()
    conn.close()


def get_chat_history():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT username, message, timestamp FROM messages ORDER BY id DESC")  # Added timestamp
    chat_history = cursor.fetchall()
    conn.close()
    return chat_history

