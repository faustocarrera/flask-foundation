"""
Tests
"""

import pytest
from appname import create_app
from appname.database import db
from appname.models import User

@pytest.fixture(scope='module')
def test_app():
    print('create test app')
    app = create_app('appname.settings.TestConfig')
    with app.app_context():
        db.create_all()
        # add admin by default
        admin = User('admin', 'supersafepassword')
        db.session.add(admin)
        db.session.commit()
    yield app.test_client()
    print('teardown test app')
    with app.app_context():
        db.session.remove()
        db.drop_all()
