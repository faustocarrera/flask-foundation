#!env/bin/python
# -*- coding: utf-8 -*-

from nose.tools import *
from . import BaseTest
from appname.database import db
from appname.models import User

class TestUser(BaseTest):
    
    def setup(self):
        "Setup after each method"
        print('SETUP')
        
    def teardown(self):
        "Teardown after each method"
        print('TEARDOWN')
        
    def test_user_save(self):
        "Test Saving the user model to the database"
        with self.app.app_context():
            testuser = User('testuser', 'supersafepassword')
            db.session.add(testuser)
            db.session.commit()
            user = User.query.filter_by(username='testuser').first()
            assert user is not None

    def test_user_password(self):
        "Test password hashing and checking"
        with self.app.app_context():
            testuser = User('testuser', 'supersafepassword')
            assert testuser.username == 'testuser'
            assert testuser.check_password('supersafepassword')
