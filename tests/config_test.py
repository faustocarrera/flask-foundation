#!env/bin/python
#-*- coding: utf-8 -*-

from nose.tools import *
from appname import create_app


class TestConfig():

    @classmethod
    def setup_class(cls):
        "Run for this class only"
        print('SETUP CLASS')

    @classmethod
    def teardown_class(cls):
        print('TEARDOWN CLASS')

    def setup(self):
        "Setup after each method"
        print('SETUP')
        
    def teardown(self):
        "Teardown after each method"
        print('TEARDOWN')
        
    def test_dev_config(self):
        "Check if dev config loads correctly"
        app = create_app('appname.settings.DevConfig')
        assert_equal(app.config['DEBUG'], True)
        assert_equal(app.config['SQLALCHEMY_DATABASE_URI'], 'sqlite:///../database.db')
        assert_equal(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'], False)
        assert_equal(app.config['CACHE_TYPE'], 'null')

    def test_test_config(self):
        "Check if test config loads correctly"
        app = create_app('appname.settings.TestConfig')
        assert_equal(app.config['DEBUG'], True)
        assert_equal(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'], False)
        assert_equal(app.config['SQLALCHEMY_ECHO'], True)
        assert_equal(app.config['CACHE_TYPE'], 'null')
        
    def test_prod_config(self):
        "Check if production config loads correctly"
        app = create_app('appname.settings.ProdConfig')
        assert_equal(app.config['SQLALCHEMY_TRACK_MODIFICATIONS'], False)
        assert_equal(app.config['SQLALCHEMY_DATABASE_URI'], 'sqlite:///../database.db')
        assert_equal(app.config['CACHE_TYPE'], 'simple')
