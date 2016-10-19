from src.app import app

__author__ = 'KBardool'

app.run(debug=app.config['DEBUG'], port=5000)