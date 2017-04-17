"""
Package: models.user
"""

from flask_login import UserMixin
from flask_login import AnonymousUserMixin
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from appname.database import db


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        "Hash password"
        self.password = generate_password_hash(password)

    def check_password(self, value):
        "Check password"
        return check_password_hash(self.password, value)

    @property
    def is_authenticated(self):
        "Check if user is authenticated"
        if isinstance(self, AnonymousUserMixin):
            return False
        else:
            return True

    def is_active(self):
        "Check if user is active"
        return True

    def is_anonymous(self):
        "Check if the user is not logged"
        if isinstance(self, AnonymousUserMixin):
            return True
        else:
            return False

    def get_id(self):
        "Get user id"
        return self.id

    def __repr__(self):
        return '<User %r>' % self.username
