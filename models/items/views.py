from flask import Blueprint



__author__ = 'KBardool'

# view is simply the endpoint of the API related to the users object
# we will be using blueprints

item_blueprint = Blueprint('items',__name__)

@item_blueprint.route('/item/<string:name>')
def item_page(name):
    pass

@item_blueprint.route('/load')
def load_item():
    """
    some explaination on to what the function does
    loads
    :return:
    """
    pass

