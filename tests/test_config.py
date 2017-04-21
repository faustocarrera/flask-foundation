#!env/bin/python
#-*- coding: utf-8 -*-

import pytest
from appname import create_app


class TestConfig():
        
    def test_dev_config(self):
        "Check if dev config loads correctly"
        app = create_app('appname.settings.DevConfig')
        assert app.config['DEBUG'] == True
        assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///database/dev.db'
        assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] == False
        assert app.config['CACHE_TYPE'] == 'null'

    def test_test_config(self):
        "Check if test config loads correctly"
        app = create_app('appname.settings.TestConfig')
        assert app.config['DEBUG'] == True
        assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] == False
        assert app.config['SQLALCHEMY_ECHO'] == True
        assert app.config['CACHE_TYPE'] == 'null'
        
    def test_prod_config(self):
        "Check if production config loads correctly"
        app = create_app('appname.settings.ProdConfig')
        assert app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] == False
        assert app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite:///database/prod.db'
        assert app.config['CACHE_TYPE'] == 'simple'
