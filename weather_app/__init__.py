from flask import Flask
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config.from_object('config')

# prepare to use flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

from weather_app import views
