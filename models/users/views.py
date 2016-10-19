from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from models.users.user import User
import models.users.errors as UserErrors
import models.users.decorators as user_decorators

__author__ = 'KBardool'

# view is simply the endpoint of the API related to the users object
# we will be using blueprints

user_blueprint = Blueprint('users', __name__)


# GET for data request , POST for returing data to server
@user_blueprint.route('/login', methods=['GET', 'POST'])
def login_user():
    print('   views.login_user() - request is:', request)
    if request.method == 'POST':
        # check that login is valid
        email = request.form['email']
        password = request.form['password']
        try:
            if User.is_login_valid(email, password):
                print('   login_user: Login is valid')
                session['email'] = email
                return redirect(url_for('.user_alerts'))
        except UserErrors.UserError as e:
            return e.message

    return render_template("users/login.html")


@user_blueprint.route('/register', methods=['GET', 'POST'])
def register_user():
    print('   views.register_user() - request method is:', request.method)
    if request.method == 'POST':
        # check that login is valid
        email = request.form['email']
        password = request.form['password']
        print('  email is:', email, ' password is : ',password)
        try:
            if User.register_user(email, password):
                print('   Register_user: Registration was good')
                session['email'] = email
                return redirect(url_for('.user_alerts'))
        except UserErrors.UserError as e:
            print('   User.Reigsteruser failed: ', e)
            return e.message

    # return render_template("users/login.html")
    return render_template("users/register.html")


@user_blueprint.route('/alerts')
@user_decorators.requires_login
def user_alerts():
    print('   views.user_alerts() - request is:', request)
    user = User.find_by_email(session['email'])
    alerts = user.get_alerts()
    print('   views.user_alerts() alerts found ', alerts)
    return render_template("users/alerts.html", alerts = alerts )


@user_blueprint.route('/logout')
def logout_user():
    print('   views.logout_user()- request is:', request)
    session['email'] = None
    return render_template("home.html")


@user_blueprint.route('/check_alerts/<string:user_id>')
def check_user_alerts():
    print('   views.check_user_alerts() - request is:', request)
    pass
