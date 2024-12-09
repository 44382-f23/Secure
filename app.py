from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from database import init_db, register_user, get_user_password, save_message
import re 



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
    if len(password) < 8:
        return False
    if not any(char.isdigit() for char in password):
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char.islower() for char in password):
        return False
    if not any(char in "!@#$%^&*()_+" for char in password):
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
            flash("Password must be at least 8 characters, include an uppercase letter, a digit, and a special character.")
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
    if request.method == 'POST':
        message = request.form['message']
        username = session.get('username', 'Anonymous')  # Use session or a default username
        
        # Save the message to the database
        save_message(username, message)
        
        # Update chat history in session
        chat_history = session.get('chat_history', [])
        chat_history.append((username, message))
        session['chat_history'] = chat_history

    chat_history = session.get('chat_history', [])
    return render_template('chat.html', chat_history=chat_history, username=session.get('username'))
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
