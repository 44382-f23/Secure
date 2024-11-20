from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from database import init_db, register_user, get_user_password, save_message, get_chat_history

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if register_user(username, password):
            flash("Registration successful! Please log in.")
            return redirect(url_for('login'))
        else:
            flash("Username already exists.")
    return render_template('register.html')

@app.route('/chat', methods= ['GET', 'POST'])