from flask import Flask, render_template, redirect, url_for, flash, request, session
from sql_connect import *

app = Flask(__name__)
app.secret_key = 'super_secret_key_nobody_can_guess'

@app.route('/')
def index():
    session['user_id'] = None
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if session["user_id"] is not None:
        return render_template('home.html')
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        query = f"SELECT * FROM users WHERE username=%(username)s AND password=%(password)s"
        args = {'username': username, 'password': password}
        result = execute_query(query, args)
        if result:
            session["user_id"] = result[0][0]
            return redirect(url_for('home'))
        else:
            flash("Invalid username or password", 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if username already exists
        query = f"SELECT * FROM users WHERE username=%(username)s"
        args = {'username': username}
        result = execute_query(query, args)
        if result:
            flash("Username already exists", 'error')
            return redirect(url_for('signup'))
        
        # Insert new user into the database
        query = f"INSERT INTO users (username, password) VALUES (%(username)s, %(password)s)"
        args = {'username': username, 'password': password}
        execute_query(query, args)
        flash("User created successfully", 'success')
        return redirect(url_for('login'))
    return render_template('signup.html')




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)