# Ryan Schuenke

from flask import Flask, render_template, redirect, url_for, flash, request, session
from sql_connect import *
from dynamo_connect import *

app = Flask(__name__)
app.secret_key = 'super_secret_key_nobody_can_guess'

@app.route('/')
def index():
    """
    Sets username to none for no signed in user. redirects to login
    """
    session['username'] = None
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """"
    Display login on GET, login user on POST
    """
    # on POST, attempt login
    if request.method == 'POST':
        # grab username and password from form
        username = request.form['username']
        password = request.form['password']
        
        # check if user has matching password
        if query_login(username, password):
            # log in by setting session username and redirecting to home
            session["username"] = username
            return redirect(url_for('home'))
        else:
            # if username not in database or password does not match, go back to login
            flash("Username/Password is incorrect", "danger") 
            return redirect(url_for('login'))
    
    # display login page at "GET" request
    else:
        return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Display signup page on GET, attempt user Sign up on post
    """
    # for post methods
    if request.method == 'POST':
        # grab username and password from form
        username = request.form['username']
        password = request.form['password']
        
        # Check if username already exists
        if query_username(username):
            # redirect back to signup if username taken
            flash("username already exists", "danger")
            return redirect(url_for('signup'))
        else:
            # if username not taken, add credentials to NoSQL database and go to login
            create_success = create_user(username, password)
            if create_success:
                return redirect(url_for('login'))
            else: 
                flash("username already exists", "danger")
                return redirect(url_for('signup'))
    else: 
        return render_template('signup.html')

@app.route('/home')
def home():
    """
    Home page of web application offering to  manage account or start playing game
    """
    # displays home page if username is set (logged in)
    if session["username"] is not None:
        return render_template('home.html')
    
    # redirects to login page if not logged in
    else:
        flash('User must be logged in to view page', 'warning')
        return redirect(url_for('login'))
    
@app.route('/play', methods=['POST'])
def play():
    """
    display game page with two cities to guess which has a higher population
    """
    # if user not logged in, redirect back to login
    if session['username'] is None:
        flash('User must be logged in to view page', 'warning')
        return redirect(url_for('login'))
    
    # for GET methods, display the game page with two random cities from the choosen country
    elif request.method == 'POST':
        country = request.form['country']
        cities = execute_query("""SELECT city.Name, city.District, city.population, city.CountryCode, country.Code, country.Name 
                               FROM city JOIN country ON city.CountryCode = country.Code 
                               WHERE LOWER(country.Name) = LOWER(%(country)s) 
                               ORDER BY RAND()
                               LIMIT 2""", {"country":country})
        
        # if there are not enough cities or country was misspelled, redirect back home
        try:
            if len(cities) < 2:
                flash('Country not found or does not have more than one city.', 'warning')
                return redirect(url_for('home'))
        except Exception:
            flash('Country not found or does not have more than one city.', 'warning')
            return redirect(url_for('home'))
        
        return render_template('play.html', cities = cities)

@app.route('/score', methods=["POST"])
def score():
    """
    Display score page with check if user guessed correctly and offer chance to play again or return home
    """
    # if user not logged in, redirect back to login
    if session['username'] is None:
        flash('User must be logged in to view page', 'warning')
        return redirect(url_for('login'))
    
    # for GET methods, display the score page with their win or loss
    elif request.method == 'POST':
        
        # get choice population and remaining option's population
        choice = request.form['city choice']
        guessed_higher = int(request.form[choice])
        
        for k in request.form.keys():
            if k not in ['city choice', choice]:
                not_choice = k
        guessed_lower = int(request.form[not_choice])
        
        # compare to find if user was correct or not
        if guessed_higher >= guessed_lower:
            result = 'correct!'
            comparison = choice + " (" + request.form[choice] + ") > " + not_choice + " (" + request.form[not_choice] + ")"
        else: 
            result = 'incorrect.'
            comparison = not_choice + " (" + request.form[not_choice] + ") > "+ choice + " (" + request.form[choice] + ")"
        
        return render_template('score.html', result = result, comparison = comparison)
    

@app.route('/delete_account', methods=['GET', 'POST'])
def delete_account():
    """
    Display delete account on GET, delete account on POST
    """
    # if user not logged in, redirect back to login
    if session['username'] is None:
        flash('User must be logged in to view page', 'warning')
        return redirect(url_for('login'))
    
    # for GET methods, display the home page with their current username
    elif request.method == 'GET':
        return render_template('delete_account.html', username = session["username"])
    
    # for POST method, attempt to delete user
    elif request.method == 'POST':
        # get username from form and verify it matches the session username
        username = request.form['username']
        if username != session["username"]:
            flash("incorrect username", "warning")
            return redirect(url_for("delete_account"))
        
        # attempt to delete the username
        deleted = delete_user(username)
        if deleted:
            flash("user deleted", "success")
        else: 
            flash("user not in database", "danger")
        # go to home regardless of success or failure with None username, but change flash message
        session['username'] = None
        return redirect(url_for('login'))

@app.route('/update_account', methods=['GET', 'POST'])
def update_account():
    """
    Display update page on GET, attempt to update password on POST
    """
    # if not logged in, redirect to login page
    if session['username'] is None:
        flash('User must be logged in to view page', 'warning')
        return redirect(url_for('login'))
    
    # on GET method, render update page
    if request.method == 'GET':
        return render_template('update_account.html', username = session["username"])
    
    # on POST method, attempt to update password
    elif request.method == 'POST':
        # get username and new password
        username = session['username']
        password = request.form['password']
        
        # attempt to update password
        update_success = update_password(username, password)
        
        # on success, redirect to the home page
        if update_success:
            flash("password updated", "success")
            return redirect(url_for('home'))
        
        # on failure (username not in NoSQL database), redirect to home page and logout user
        else: 
            flash("user not in database", "danger")
            session['username'] = None
            return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)