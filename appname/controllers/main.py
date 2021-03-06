"""
Package: controllers.main
"""

from flask import Blueprint
from flask import render_template
from flask import flash
from flask import request
from flask import redirect
from flask import url_for
from flask_login import login_user
from flask_login import logout_user
from flask_login import login_required
from appname.extensions import cache
from appname.forms import LoginForm
from appname.models import User

main = Blueprint('main', __name__)


@main.route('/')
@cache.cached(timeout=1000)
def home():
    "Home page"
    return render_template('index.html')


@main.route('/login', methods=['GET', 'POST'])
def login():
    "Login form"
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).one()
        login_user(user)

        flash('Logged in successfully.', 'success')
        return redirect(request.args.get('next') or url_for('.home'))

    return render_template('login.html', form=form)


@main.route('/logout')
def logout():
    "Logout"
    logout_user()
    flash('You have been logged out.', 'success')

    return redirect(url_for('.home'))


@main.route('/restricted')
@login_required
def restricted():
    "Restricted area"
    return 'You can only see this if you are logged in!', 200
