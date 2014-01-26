from weather_app import db
from flask.ext.login import UserMixin

# db is a SQLALchemy object provided by flask-sqlalchemy that provides:
# - all the functions and classes from sqlalchemy and slalchemy.orm
# - a preconfigured scoped session called *session*
# - the *metadata*, the *engine*
# - a *Model* base class that is a configured declarative base
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True, index=True)
    password = db.Column(db.String(120))

    def __repr__(self):
        return '<User: %r>' % (self.name)
