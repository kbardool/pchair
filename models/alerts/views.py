from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from models.alerts.alert import Alert
from models.items.item import Item
import models.users.decorators as user_decorators


__author__ = 'KBardool'

# view is simply the endpoint of the API related to the users object
# we will be using blueprints

alert_blueprint = Blueprint('alerts', __name__)

@alert_blueprint.route('/')
def index():
    return "this is the Alerts index"


@alert_blueprint.route('/new', methods=['GET','POST'])
@user_decorators.requires_login
def create_alert():
    if request.method == 'POST':
        print('   alerts.create_alert(): POST method!')
        name = request.form['name']
        url  = request.form['url']
        price_limit = float(request.form['price_limit'])
        print('  name:',name,'   url:', url, '  price:',price_limit)
        print('   create item')
        item = Item(name, url)
        item.save_to_db()
        print('   create alert session[email] is', session['email'])
        alert = Alert(session['email'], price_limit, item._id)
        alert.load_item_price()   # this method saving to database

        print('   alerts.views.create_alert(): alert created')

    return render_template("alerts/create_alert.html")


@alert_blueprint.route('/edit/<string:alert_id>', methods=['GET', 'POST'])
@user_decorators.requires_login
def edit_alert(alert_id):
    alert = Alert.find_by_id(alert_id)
    print('   alerts.views.edit_alert() alert is ', alert)

    if request.method == 'POST':
        alert.price_limit = float(request.form['price_limit'])
        alert.save_to_db()
        print('   alerts.views.create_alert(): alert modified')
        return redirect(url_for('users.user_alerts', alert=alert))

    return render_template("alerts/edit_alert.html", alert=alert)


@alert_blueprint.route('/<string:alert_id>')
@user_decorators.requires_login
def get_alert_page(alert_id):
    alert = Alert.find_by_id(alert_id)
    return render_template('alerts/alert.html', alert = alert)


@alert_blueprint.route('/check_price/<string:alert_id>')
@user_decorators.requires_login
def check_alert_price(alert_id):
    alert = Alert.find_by_id(alert_id).load_item_price()
    return redirect(url_for('.get_alert_page', alert_id = alert_id))
    ##  return render_template('alerts/alert.html', alert = alert)


@alert_blueprint.route('/deactivate/<string:alert_id>')
@user_decorators.requires_login
def deactivate_alert(alert_id):
    print('   alerts.deactivate_alert()')
    alert = Alert.find_by_id(alert_id).deactivate()
    # return redirect(url_for('.get_alert_page', alert_id = alert_id))
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/activate/<string:alert_id>')
@user_decorators.requires_login
def activate_alert(alert_id):
    print('   alerts.activate_alert()')
    alert = Alert.find_by_id(alert_id).activate()
    # return redirect(url_for('.get_alert_page', alert_id = alert_id))
    return redirect(url_for('users.user_alerts'))


@alert_blueprint.route('/delete/<string:alert_id>')
@user_decorators.requires_login
def delete_alert(alert_id):
    print('   alert views.delete_alert()')
    alert = Alert.find_by_id(alert_id).delete()
    # return redirect(url_for('.get_alert_page', alert_id = alert_id))
    return redirect(url_for('users.user_alerts'))