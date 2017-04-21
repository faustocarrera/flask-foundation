#!env/bin/python
# -*- coding: utf-8 -*-

import pytest
from .. import test_app
from appname import create_app
from appname.database import db
from appname.models import User

@pytest.mark.incremental
class TestUser():
        
    def test_save(self, test_app):
        "Test Saving the user model to the database"
        app = create_app('appname.settings.TestConfig')
        with app.app_context():
            testuser = User('testuser', 'supersafepassword')
            db.session.add(testuser)
            db.session.commit()
            user = User.query.filter_by(username='testuser').first()
            assert user is not None
            
    def test_update(self):
        "Test update user"
        app = create_app('appname.settings.TestConfig')
        with app.app_context():
            user = User.query.filter_by(username='testuser').first()
            user.set_password('anothersafepassword')
            db.session.commit()
            testuser = User.query.filter_by(username='testuser').first()
            assert testuser is not None
            assert testuser.check_password('anothersafepassword')
            
    def test_delete(self):
        "Test delete user"
        app = create_app('appname.settings.TestConfig')
        with app.app_context():
            user = User.query.filter_by(username='testuser').first()
            db.session.delete(user)
            db.session.commit()
            testuser = User.query.filter_by(username='testuser').first()
            assert testuser is None
    
    def test_password(self, test_app):
        "Test password hashing and checking"
        app = create_app('appname.settings.TestConfig')
        with app.app_context():
            testuser = User('testuser', 'supersafepassword')
            assert testuser.username == 'testuser'
            assert testuser.check_password('supersafepassword')
