from flask import (request, render_template, flash, redirect, g, url_for, session)
from flask.ext.login import (login_user, logout_user, current_user,
    login_required)
from flask.json import jsonify
from ConfigParser import SafeConfigParser

from foursquare import Foursquare

from weather_app import app, db, login_manager
from .models import User

client_id = 'AYYIMF3RMVYQWYL0KSU1PES5QT4AKLXZUAUJTVISFCN1IABX'
client_secret = '1G2NM12W44SNVTJ0RCKJ1WNOB0CVENAIQUZX0ZEXRPKQL1DO'
redirect_uri = 'http://localhost:5000/callback'
token_url = 'https://foursquare.com/oauth2/access_token'

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
    logout_user()
    return redirect(url_for('index'))

@app.route('/forecast')
@login_required
def forecast():
    # get hold of current user
    user = current_user

    if user:
        if user.fs_access_token is not None and user.fs_access_token != '':
            # use the access token to get user's data

            foursquare_client = Foursquare(access_token=user.fs_access_token)
            user = foursquare_client.users()
            return jsonify(user)
        else:
            # get secret and urls
            #parser = SafeConfigParser()
            #parser.read('foursquare.ini')
            #client_id = parser.get('foursquare', 'client_id')
            #client_secret = parser.get('foursquare', 'client_secret')
            #redirect_uri = parser.get('foursquare', 'redirect_uri')

            # redirect user to foursquare authenticate page
            foursquare_client = Foursquare(client_id=client_id,
                client_secret=client_secret, redirect_uri=redirect_uri)
            authorization_url = foursquare_client.oauth.auth_url()
            return redirect(authorization_url)
    else:
        # no user (shouldn't happen)
        return redirect(url_for('login'))

@app.route('/callback', methods=['GET', ])
def callback():
    # get the current user
    user = current_user

    # parse out code from call back
    code = request.args.get('code')
    session['code'] = code

    # exchange code for access token
    foursquare_client = Foursquare(client_id=client_id,
        client_secret=client_secret, redirect_uri=redirect_uri)
    access_token = foursquare_client.oauth.get_token(code)

    # save the access token
    if access_token and access_token != '':
        user.fs_access_token = access_token
        db.session.commit()

    return redirect(url_for('forecast'))

