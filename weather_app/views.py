from flask import (request, render_template, flash, redirect, g, url_for, session)
from flask.ext.login import (login_user, logout_user, current_user,
    login_required)
from forms import EditAlertForm

from foursquare import Foursquare

from weather_app import app, db, login_manager
from .models import User, Checkin


def format_phone(phn):
    """
    This function attempts to format the phone variable. Currently accepts
    inputs with dashes and spaces.  It removes those values and then checks
    to make sure all remaing values are valid integers.  If the country
    code was ommitted (currently only for the US), it is added, 
    additionally a + is added to the front of the string to comply with 
    Twilio's API.  If the format appears to be invalid, None is returned,
    and an error can be raised to the user.
    """
    phn = str(phn).translate(None, "- +")
    for digit in phn:
        if not digit.isdigit():
            return None
    if phn[0] != 1:
        phn = "+1" + phn
    else:
        phn = "+" + phn
    if len(phn) == 12:
        return phn
    else:
        return None


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
        phone = format_phone(request.form['phone'])
        if user_check != None:
            error = 'User name already taken, please choose another one'
        elif phone == None:
            error = 'Invalid Phone Number'
        else:
            user = User(name=request.form['username'], phone=phone,
                password=request.form['password'], email=request.form['email'], 
                hrs=3, pop=25)
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

@app.route("/prompt_fs_authorize")
@login_required
def prompt_fs_authorize():
    # get secret and urls
    fs_client_id = app.config['FS_CLIENT_ID']
    fs_client_secret = app.config['FS_CLIENT_SECRET']
    fs_redirect_uri = app.config['FS_REDIRECT_URI']

    # get fs redirect link
    foursquare_client = Foursquare(client_id=fs_client_id,
        client_secret=fs_client_secret, redirect_uri=fs_redirect_uri)
    fs_authorize_url = foursquare_client.oauth.auth_url()
    return render_template('fs_authorize.html',
        fs_link=fs_authorize_url)

@app.route('/forecast')
@login_required
def forecast():
    # get hold of current user
    user = current_user

    if user is None:
        # unable to obtain current user,
        # perhaps user entered url directly
        return redirect(url_for('login'))

    # valid user, valid access token?
    if not user.has_valid_fs_access_token():
        return redirect(url_for('prompt_fs_authorize'))

    # valid access token
    last_checkin, new_chk = user.get_last_checkin()
    if last_checkin is not None:
        return "hello, you last checked in at %s, lat = %f, lng = %f" % (last_checkin.name, last_checkin.lat, last_checkin.lng)
    else:
        return "oops! we weren't able to get a check in from foursquare. perhaps you haven't checked in yet?"

@app.route('/callback', methods=['GET', ])
def callback():
    # get the current user
    user = current_user

    # parse out code from call back
    code = request.args.get('code')
    session['code'] = code

    # exchange code for access token, get secret and urls
    fs_client_id = app.config['FS_CLIENT_ID']
    fs_client_secret = app.config['FS_CLIENT_SECRET']
    fs_redirect_uri = app.config['FS_REDIRECT_URI']

    foursquare_client = Foursquare(client_id=fs_client_id,
        client_secret=fs_client_secret, redirect_uri=fs_redirect_uri)
    access_token = foursquare_client.oauth.get_token(code)

    # save the access token
    if access_token and access_token != '':
        user.fs_access_token = access_token
        db.session.commit()

    return redirect(url_for('forecast'))


@app.route('/editalert', methods=['GET', 'POST'])
@login_required
def editalert():
    form = EditAlertForm()
    user = current_user
    if form.validate_on_submit():
        user.hrs = form.hrs.data
        user.pop = form.pop.data
        db.session.add(user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('index'))
    elif request.method != "POST":
        form.hrs.data = user.hrs
        form.pop.data = user.pop
    return render_template('editalert.html', form=form)



