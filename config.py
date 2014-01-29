import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

# path to database
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR,
    'weather.db')

# flask app secret key, also used by flask-wtf
SECRET_KEY = 'developer key'
TESTING = False

# flask-wtf
WTF_CSRF_ENABLED = True
