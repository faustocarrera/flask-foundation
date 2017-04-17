#!env/bin/python

import os

from flask_script import Manager, Server
from flask_script.commands import ShowUrls, Clean
from flask_migrate import Migrate, MigrateCommand
from appname import create_app
from appname.database import db
from appname.models.user import User

# default to dev config because no one should use this in
# production anyway
env = os.environ.get('APPNAME_ENV', 'dev')
app = create_app('appname.settings.%sConfig' % env.capitalize())
migrate = Migrate(app, db)


manager = Manager(app)
manager.add_command('server', Server(host='0.0.0.0'))
manager.add_command('show-urls', ShowUrls())
manager.add_command('clean', Clean())
manager.add_command('db', MigrateCommand)


@manager.shell
def make_shell_context():
    "Creates a python REPL"
    return dict(app=app, db=db, User=User)


if __name__ == "__main__":
    manager.run()
