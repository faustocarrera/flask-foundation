#!env/bin/python
#-*- coding: utf-8 -*-

from nose.tools import *
from appname import create_app


class TestUrl():

    def setup(self):
        "Run for this class only"
        app = create_app('appname.settings.TestConfig')
        self.app = app.test_client()

    def test_home(self):
        "Tests if the home page loads"
        rv = self.app.get('/')
        assert rv.status_code == 200
