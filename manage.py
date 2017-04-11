#!env/bin/python

import os

from flask_script import Manager, Server
from flask_script.commands import ShowUrls, Clean
from appname import create_app
from appname.models import db
from appname.models.user import User

# default to dev config because no one should use this in
# production anyway
env = os.environ.get('APPNAME_ENV', 'dev')
app = create_app('appname.settings.%sConfig' % env.capitalize())

manager = Manager(app)
manager.add_command('server', Server(host='0.0.0.0'))
manager.add_command('show-urls', ShowUrls())
manager.add_command('clean', Clean())


@manager.shell
def make_shell_context():
    "Creates a python REPL"
    return dict(app=app, db=db, User=User)


@manager.command
def createdb():
    "Creates a database with all of the tables defined in your models"
    db.create_all()


if __name__ == "__main__":
    manager.run()
