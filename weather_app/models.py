from weather_app import db
from flask.ext.login import UserMixin
from foursquare import Foursquare

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
    fs_access_token = db.Column(db.Text)
    checkins = db.relationship('Checkin', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User: %s>' % (self.name)

    def has_valid_fs_access_token(self):
        return (self.fs_access_token is not None and
            self.fs_access_token != '')

    def last_fs_checkin(self):
        # use the access token to get user's data
        foursquare_client = Foursquare(access_token=self.fs_access_token)
        return foursquare_client.users.checkins(params={'limit':1})


class Checkin(db.Model):
    __tablename__ = 'checkins'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    fs_id = db.Column(db.Text)
    fs_created_at = db.Column(db.Integer)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return "<Checked in: %s>" (self.name)
