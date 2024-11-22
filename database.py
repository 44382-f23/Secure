import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def init_db():
    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()
    cursor.execute(''' CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, message TEXT)''')
    conn.commit()
    conn.close()

def register_user(username,password):
    hashed_password = generate_password_hash(password)
    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?,?)",(username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError :
        return False
    finally:
        conn.close()

def get_user_password(username):
    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

def save_message(username, message):
    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO messages(username, message) VALUES (?,?)",(username, message))
    conn.commit()

def get_chat_history():
    conn = sqlite3.connect('chat_app.db')
    cursor = conn.cursor()
    cursor.execute("SELECT username, message FROM messages ORDER BY id")
    chat_history = cursor.fetchall()
    conn.close()
    return chat_history