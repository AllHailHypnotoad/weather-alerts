#!/usr/bin/env python

from config import SQLALCHEMY_DATABASE_URI
from weather_app import db

db.create_all()
