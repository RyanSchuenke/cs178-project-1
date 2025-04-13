from flask import Flask, render_template, redirect, url_for, flash, request, session
from sql_connect import *
from dynamo_connect import *

app = Flask(__name__)
app.secret_key = 'super_secret_key_nobody_can_guess'

@app.route('/')
def index():
    session['username'] = None
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if session["username"] is not None:
        countries = execute_query("SELECT * FROM country ORDER BY Population DESC LIMIT 10", {})
        return render_template('home.html', countries = countries)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if query_login(username, password):
            session["username"] = username
            return redirect(url_for('home'))
        else:
            flash("Username/Password is incorrect", "danger") 
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if username already exists
        if query_username(username):
            flash("username already exists", "danger")
            return redirect(url_for('signup'))
        else:
            create_user(username, password)
            return redirect(url_for('login'))
    else: 
        return render_template('signup.html')
    
@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    if session['username'] is None:
        flash('', 'danger')
        redirect(url_for('login'))
    if request.method == 'GET':
        return render_template('delete_account.html', username = session["username"])
    elif request.method == 'POST':
        username = request.form['username']
        if username != session["username"]:
            flash("incorrect username", "warning")
            return redirect(url_for("delete_account"))
            
        deleted = delete_user(username)
        if deleted:
            flash("user deleted", "success")
        else: 
            flash("user not in database", "danger")
        session['username'] = None
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)