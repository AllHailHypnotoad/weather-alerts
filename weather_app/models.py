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
    phone = db.Column(db.String(12))
    password = db.Column(db.String(120))
    fs_access_token = db.Column(db.Text)
    checkins = db.relationship('Checkin', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User: %s>' % (self.name)

    def has_valid_fs_access_token(self):
        return (self.fs_access_token is not None and
            self.fs_access_token != '')

    def get_last_checkin(self):
        # use the access token to get user's data
        foursquare_client = Foursquare(access_token=self.fs_access_token)
        fs_checkin = foursquare_client.users.checkins(params={'limit':1})

        if (fs_checkin['checkins']['count'] == 0):
            # foursquare did not send the user's last checkin
            # possible that the user have not ever checked in
            last_stored_checkin = self.checkins.order_by('-id').first()

            if last_stored_checkin is None:
                # don't have a last checkin stored for this user
                return None
            else:
                return last_stored_checkin

        # got a checkin from foursquare
        # is this a newer checkin than what we have in the database?
        fs_id = fs_checkin['checkins']['items'][0]['id']
        fs_created = fs_checkin['checkins']['items'][0]['createdAt']

        # get user's last checkin stored in the database
        last_stored_checkin = self.checkins.order_by('-id').first()

        # if checkin table is empty or the stored fs_checkin id doesn't match
        # the checkin fs_id received from fs, then add the checkin received
        # from foursquare to the list of checkins for this user
        if (last_stored_checkin is None or
            last_stored_checkin.fs_created != fs_created):

            name = fs_checkin['checkins']['items'][0]['venue']['name']
            fs_created_tz_offset = fs_checkin['checkins']['items'][0]['timeZoneOffset']
            location = fs_checkin['checkins']['items'][0]['venue']['location']
            lat = location['lat']
            lng = location['lng']

            checkin = Checkin(name=name, fs_id=fs_id, fs_created=fs_created,
                fs_created_tz_offset=fs_created_tz_offset, lat=lat, lng=lng, user=self)
            db.session.add(checkin)
            db.session.commit()
            return checkin
        else:
            # foursquare does not keep state of the checkins it sends
            # we have seen this checkin before
            return last_stored_checkin


class Checkin(db.Model):
    __tablename__ = 'checkins'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    fs_id = db.Column(db.Text)
    fs_created = db.Column(db.Integer)
    fs_created_tz_offset = db.Column(db.Integer)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return "<Checked in: %s, lat: %f, lng: %f>" % (self.name,
            self.lat, self.lng)
