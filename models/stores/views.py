from flask import Blueprint
from flask import json
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from models.stores.store import Store
import models.users.decorators as user_decorators

__author__ = 'KBardool'

# view is simply the endpoint of the API related to the users object
# we will be using blueprints

store_blueprint = Blueprint('stores',__name__)


@store_blueprint.route('/')
def index():
    stores = Store.all()
    return render_template('/stores/store_list.html', stores = stores)


@store_blueprint.route('/stores/<string:store_id>')
def store_page(store_id):
    print('   stores.store_page()')
    store = Store.get_by_id(store_id)
    print('   stores.store_page() ',Store)
    return render_template('/stores/store.html', store = store)


@store_blueprint.route('/edit/<string:store_id>', methods=['GET','POST'])
@user_decorators.requires_admin_permissions
def edit_store(store_id):
    print('   stores.edit_store()', store_id)

    store = Store.get_by_id(store_id)
    if request.method == 'POST':
        store.name        = request.form['name']
        store.url_prefix  = request.form['url_prefix']
        store.tag_name    = request.form['tag_name']
        store.query       = json.loads(request.form['query'])
        # print('   name:',name,' url_pref:',url_prefix,' query:',query)
        store.save_to_db()
        return redirect(url_for('.index'))

    return render_template('stores/edit_store.html', store = store)


@store_blueprint.route('/del/<string:store_id>')
@user_decorators.requires_admin_permissions
def delete_store(store_id):
    print('   stores.delete_store()',store_id)
    Store.get_by_id(store_id).delete()
    return redirect(url_for('.index'))


@store_blueprint.route('/new', methods=['GET','POST'])
@user_decorators.requires_admin_permissions
def create_store():
    print('   stores.create_store()')
    if request.method == 'POST':
        name = request.form['name']
        url_prefix = request.form['url_prefix']
        tag_name = request.form['tag_name']
        query = json.loads(request.form['query'])
        # print('   name:',name,' url_pref:',url_prefix,' query:',query)
        Store(name, url_prefix, tag_name, query ).save_to_db()
        return redirect(url_for('.index'))

    return render_template('stores/new_store.html')
