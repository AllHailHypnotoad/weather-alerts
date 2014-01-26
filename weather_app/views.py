from flask import (Flask, request, render_template, flash, redirect,
    url_for, session)
from flask.ext.login import (login_user, logout_user, current_user,
    login_required)

from weather_app import app, db, login_manager
from models import User

@login_manager.user_loader
def load_user(id):
    """
    Retrieves a user from a user's id.
    Note: flask-login implements user id as unicode string. Need to
    convert to integer before sending it to the database.
    """
    return User.query.get(int(id))

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    page = 'login'
    if request.method == 'POST':
        user = User.query.filter_by(name=request.form['username']).first()
        if user == None or request.form['password'] != user.password:
            error = 'Invalid login information'
        else:
            session['logged_in'] = True
            login_user(user)
            flash('You were logged in.')
            return redirect(url_for('user_home_page'))
    return render_template('login.html', error=error, page=page)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = None
    page = 'signup'
    if request.method == 'POST':
        user_check = User.query.filter_by(name=request.form['username']).first()
        if user_check != None:
            error = 'User name already taken, please choose another one'
        else:
            session['logged_in'] = True
            user = User(name=request.form['username'],
                password=request.form['password'], email=request.form['email'])
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Thanks for signing up, you are now logged in')
            return redirect(url_for('user_home_page'))
    return render_template('signup.html', error=error, page=page)


@app.route("/", methods=["GET", "POST"])
@login_required
def user_home_page():
    message1 = "Welcome back, " + current_user.name
    message2 = "Here is your home page"
    return render_template("user_home_page.html", message1=message1, message2=message2)

@app.route("/logout")
@login_required
def logout():
    session.pop('logged_in', None)
    logout_user()
    return redirect(url_for('login'))
