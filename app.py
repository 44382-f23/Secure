from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import init_db, register_user, get_user_password, save_message, get_chat_history 
import re 
import time



#Initialize the flask application
app = Flask(__name__)
app.secret_key = 'supersecretkey'

#Username should match the requirments
def validate_username(username):
    if not username or len(username) > 20 or not re.match(r'^[a-zA-Z0-9_]+$', username):
        return False
    return True
#Password must meet the length.
def validate_password(password):
    if not password or len(password) < 8:
        return False
    return True
#Route for the home page by default it redirects to the login page
@app.route('/')
def home():
    return redirect(url_for('login'))

#Defining the login with username and password.
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash("Please provide both username and password.")
            return redirect(url_for('login'))

        db_password = get_user_password(username)
        if db_password and check_password_hash(db_password, password):
            session['username'] = username
            return redirect(url_for('chat'))  # Redirect to chat page
        else:
            flash("Invalid username or password.")
            return redirect(url_for('login'))
    return render_template('login.html')  # Render login page for GET request


#Handling user registration
@app.route('/register', methods = ['GET', 'POST'])

def register():                                
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Validate username
        if not validate_username(username):
            flash("Invalid username. Must be alphanumeric and less than 20 characters.")
            return render_template('register.html')

        # Validate password
        if not validate_password(password):
            flash("Invalid password. Must be at least 8 characters long.")
            return render_template('register.html')
        
        if not username or not password:
            flash("Username and password cannot be empty.")
            return redirect(url_for('login.html'))

        #Determines to get the user registration
        if register_user(username, password):
            flash("Registration successful! Please log in.")
            return render_template('register.html')
        else:
            flash("Username already exists. Choose a different one.")
    return render_template('register.html')



#Route for the chat functioning 
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    # Initialize chat_history in session if it doesn't exist
    if 'chat_history' not in session:
        session['chat_history'] = []

    # Handle POST request (user sends a message)
    if request.method == 'POST':
        message = request.form['message']
        username = session.get('username', 'Guest')  # Get username from session or set default as 'Guest'
        
        # Append new message to chat history (with a timestamp)
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')  # Get current timestamp
        session['chat_history'].append((username, message, timestamp))
        
        # Save the session
        session.modified = True
        flash('Message sent!')  # Optionally, show a success message

    # Get chat history from session
    chat_history = session['chat_history']
    
    return render_template('chat.html', username=session.get('username', 'Guest'), chat_history=chat_history)
#A way for logging out of the user
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.clear()
    flash("You have been logged out")
    return redirect(url_for('login'))
                    

#Making sure the database is initialized before starting the server.  
init_db()        
if __name__ == '__main__':  

    app.run(debug=True)


# Recreate the database
from database import init_db
init_db()  # Make sure the users table is created
