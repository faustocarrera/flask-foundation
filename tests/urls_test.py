#!env/bin/python
# -*- coding: utf-8 -*-

from nose.tools import *
from . import BaseTest

class TestUrls(BaseTest):
    
    def setup(self):
        "Setup after each method"
        print('SETUP')
        
    def teardown(self):
        "Teardown after each method"
        print('TEARDOWN')
        
    def test_home(self):
        "Tests if the home page loads"
        rv = self.cf.get('/')
        assert rv.status_code == 200

    def test_login(self):
        "Tests if the login page loads"
        rv = self.cf.get('/login')
        assert rv.status_code == 200

    def test_logout(self):
        "Tests if the logout page loads"
        rv = self.cf.get('/logout')
        assert rv.status_code == 302

    def test_restricted_logged_out(self):
        "Tests restricted page"
        rv = self.cf.get('/restricted', follow_redirects=False)
        assert rv.status_code == 200

    def test_restricted_logged_in(self):
        "Tests restricted page"
        self.cf.post('/login', data=dict(
            username='admin',
            password="supersafepassword"
        ), follow_redirects=True)
        rv = self.cf.get('/restricted')
        assert rv.status_code == 200

