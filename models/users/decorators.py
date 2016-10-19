from functools import wraps

from flask import request
from flask import session
from flask import url_for
from werkzeug.utils import redirect
from src.app import app

__author__ = 'KBardool'


def requires_login(func):
    print(func)
    @wraps(func)
    def decorator_function(*args, **kwargs):
        print('   @requires_login decorator func')
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        print('   @requires_login: User was logged in, so proceed')
        return func(*args, **kwargs)    # call func with all it's args

    return decorator_function


def requires_admin_permissions(func):
    print(func)
    @wraps(func)
    def decorator_function(*args, **kwargs):
        if 'email' not in session.keys() or session['email'] is None:
            return redirect(url_for('users.login_user', next=request.path))
        if session['email'] not in app.config['ADMINS']:
            return redirect(url_for('users.login_user'))
        return func(*args, **kwargs)    # call func with all it's args

    return decorator_function




def requires_kevin(func):
    print(' inside requires login -- only run once per function')
    print(func)
    @wraps(func)
    def decorations(*args, **kwargs):
        print('inside decorator - runs each time ',func,' is called')
        return func(*args, **kwargs)    # call func with all it's args

    print('  after decorator function defintion')
    return decorations




@requires_kevin
def my_function1():
    print("hello world")
    return "Bye world"

@requires_kevin
def my_function2():
    print("my function 2 - hellow world")
    return "my function 2 - Bye world"


print('\n call my function 1')
p= my_function1()
print(p)

print('\n call my function 2')
p= my_function2()
print(p)
