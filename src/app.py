from flask import Flask
from flask import render_template

from common.database import Database

__author__ = 'KBardool'

app = Flask(__name__)

app.config.from_object('src.config.py')

app.secret_key = '12345'





@app.before_first_request
def init_db():
    Database.initialize()

@app.route('/')
def home():
    return render_template("home.html")


# register blueprints

from models.users.views  import user_blueprint
from models.stores.views import store_blueprint
from models.alerts.views import alert_blueprint

#every thing in the users blueprint will be prefixed by /users
app.register_blueprint(user_blueprint, url_prefix = '/users')
app.register_blueprint(store_blueprint, url_prefix = '/stores')
app.register_blueprint(alert_blueprint, url_prefix = '/alerts')