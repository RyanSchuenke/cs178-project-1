from flask import Flask, render_template, redirect, url_for, flash, request
from sql_connect import *

app = Flask(__name__)
app.secret_key = 'super_secret_key_nobody_can_guess'



@app.route('/')
def home():
    return render_template('home.html')





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)