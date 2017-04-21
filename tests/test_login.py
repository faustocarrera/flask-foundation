#!env/bin/python
# -*- coding: utf-8 -*-

import pytest
from . import test_app

class TestLogin():
        
    def test_login(self, test_app):
        "Tests if the login form functions"
        rv = test_app.post('/login', data=dict(
            username='admin',
            password="supersafepassword"
        ), follow_redirects=True)
        assert rv.status_code == 200
        assert 'Logged in successfully.' in str(rv.data)

    def test_login_fail(self, test_app):
        "Tests if the login form fails correctly"
        rv = test_app.post('/login', data=dict(
            username='admin',
            password=""
        ), follow_redirects=True)
        assert rv.status_code == 200
        assert 'Invalid username or password' in str(rv.data)
