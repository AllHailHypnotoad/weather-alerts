from flask import (request, render_template, flash, redirect, g, url_for, session)
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

@app.before_request
def before_request():
    """
    Place the flask-login current_user into g.user to allow access to
    the user object from templates.
    """
    g.user = current_user

@app.route("/")
@app.route("/index")
@login_required
def index():
    return render_template("user_home_page.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    # user already logged in
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))

    # no user
    error = None
    page = 'login'
    if request.method == 'POST':
        user = User.query.filter_by(name=request.form['username']).first()
        if user == None or request.form['password'] != user.password:
            error = 'Invalid login information'
        else:
            login_user(user)
            flash('You were logged in.')
            return redirect(url_for('index'))
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
            return redirect(url_for('index'))
    return render_template('signup.html', error=error, page=page)

@app.route("/logout")
@login_required
def logout():
    session.pop('logged_in', None)
    logout_user()
    return redirect(url_for('index'))

@app.route('/forecast')
@login_required
def forecast():
    # get hold of current user

    # check if user has token

    # if user has token then get the last check-in from foursquare

    pass
