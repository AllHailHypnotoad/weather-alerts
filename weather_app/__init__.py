from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from ConfigParser import SafeConfigParser

app = Flask(__name__)
app.config.from_object('config')

# create flask-sqlalchemy database object
db = SQLAlchemy(app)

# use flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# stuff credentials in app config
parser = SafeConfigParser()
found = parser.read('foursquare.ini')
app.config['FS_CLIENT_ID'] = parser.get('foursquare', 'fs_client_id')
app.config['FS_CLIENT_SECRET']= parser.get('foursquare', 'fs_client_secret')
app.config['FS_REDIRECT_URI']= parser.get('foursquare', 'fs_redirect_uri')
app.config['FS_TOKEN_URL'] = parser.get('foursquare', 'fs_token_url')

from weather_app import views, models
