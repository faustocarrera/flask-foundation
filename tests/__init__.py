"""
Tests
"""

from appname import create_app
from appname.database import db
from appname.models import User

class BaseTest():
    
    @classmethod
    def setup_class(cls):
        "Run for this class only"
        cls.app = create_app('appname.settings.TestConfig')
        cls.cf = cls.app.test_client()
        with cls.app.app_context():
            db.create_all()
            # add admin by default
            admin = User('admin', 'supersafepassword')
            db.session.add(admin)
            db.session.commit()
        

    @classmethod
    def teardown_class(cls):
        with cls.app.app_context():
            db.session.remove()
            db.drop_all()
