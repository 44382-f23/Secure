from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from database import init_db, register_user, get_user_password, save_message, get_chat_history

#Initialize the flask application
app = Flask(__name__)
app.secret_key = 'supersecretkey'

#Route for the home page by default it redirects to the login page
@app.route('/')
def home():
    return redirect(url_for('login'))

#Defining the login with username and password.
@app.route('/login', methods=['GET','POST'])
def login():                                    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db_password = get_user_password(username)   #Gives the hashed password from the database

        #Checks the credentials 
        if db_password and check_password_hash(db_password, password):
            session['username'] = username
            return redirect(url_for('chat'))
        else:
            flash("Login failed.Please cleck your credentials")
            session['username'] = username
            return redirect(url_for('login'))
        return render_template('login.html')
@app.route('/register', methods = ['GET', 'POST'])

#Handling user registration
def register():                                
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

        #Determines to get the user registration
        if register_user(username, password):
            flash("Registration successful! Please log in.")
            return redirect(url_for('login'))
        else:
            flash("Username already exists.")
    return render_template('register.html')