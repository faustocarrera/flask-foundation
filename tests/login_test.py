#!env/bin/python
# -*- coding: utf-8 -*-

from nose.tools import *
from . import BaseTest

class TestLogin(BaseTest):
    
    def setup(self):
        "Setup after each method"
        print('SETUP')
        
    def teardown(self):
        "Teardown after each method"
        print('TEARDOWN')
        
    def test_login(self):
        "Tests if the login form functions"
        rv = self.cf.post('/login', data=dict(
            username='admin',
            password="supersafepassword"
        ), follow_redirects=True)
        assert rv.status_code == 200
        assert 'Logged in successfully.' in str(rv.data)

    def test_login_fail(self):
        "Tests if the login form fails correctly"
        rv = self.cf.post('/login', data=dict(
            username='admin',
            password=""
        ), follow_redirects=True)
        assert rv.status_code == 200
        assert 'Invalid username or password' in str(rv.data)