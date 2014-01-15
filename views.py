from config import SECRET_KEY
from flask import Flask, request, render_template, flash, redirect, url_for
from flask.ext.login import LoginManager, login_user, login_required, logout_user, session, current_user
from database import db_session
from models import *

app = Flask(__name__)
login_manager = LoginManager()
app.secret_key = SECRET_KEY
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(id):
    return db_session.query(User).get(int(id))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    page = 'login'
    if request.method == 'POST':
        user = db_session.query(User).filter_by(name=request.form['username']).first()
        if user == None or request.form['password'] != user.password:
            error = 'Invalid login information'
        else:
            session['logged_in'] = True
            login_user(user)
            flash('You were logged in')
            return redirect(url_for('user_home_page'))
    return render_template('login.html', error=error, page=page)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    error = None
    page = 'signup'
    if request.method == 'POST':
        user_check = db_session.query(User).filter_by(name=request.form['username']).first()
        if user_check != None:
            error = 'User name already taken, please choose another one'
        else:
            session['logged_in'] = True
            user = User(name=request.form['username'], password=request.form['password'], 
                    email=request.form['email'])
            db_session.add(user)
            db_session.commit()
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

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    app.debug = True
    app.run()