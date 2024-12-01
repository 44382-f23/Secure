import sqlite3
from werkzeug.security import generate_password_hash

DATABASE = 'chat_app.db'


#Initialize the database
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(''' CREATE TABLE IF NOT EXISTS users(id INTERGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL, password TEXT NOT NULL)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, message TEXT NOT NULL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def register_user(username,password):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    if cursor.fetchone():
        conn.close()
        return False   
    
    hashed_password = generate_password_hash(password)
    cursor.execute("INSERT INTO users (username, password) VALUES (?,?),(usernmae, hashed_password)")

    conn.commit()
    conn.close()
    return True

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