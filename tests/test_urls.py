#!env/bin/python
# -*- coding: utf-8 -*-

import pytest
from . import test_app

class TestUrls():
        
    def test_home(self, test_app):
        "Tests if the home page loads"
        rv = test_app.get('/')
        assert rv.status_code == 200

    def test_login(self, test_app):
        "Tests if the login page loads"
        rv = test_app.get('/login')
        assert rv.status_code == 200

    def test_logout(self, test_app):
        "Tests if the logout page loads"
        rv = test_app.get('/logout')
        assert rv.status_code == 302

    def test_restricted_logged_out(self, test_app):
        "Tests restricted page"
        rv = test_app.get('/restricted', follow_redirects=False)
        assert rv.status_code == 302

    def test_restricted_logged_in(self, test_app):
        "Tests restricted page"
        test_app.post('/login', data=dict(
            username='admin',
            password="supersafepassword"
        ), follow_redirects=True)
        rv = test_app.get('/restricted')
        assert rv.status_code == 200
