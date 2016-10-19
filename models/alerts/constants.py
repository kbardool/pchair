import os

__author__ = 'KBardool'

URL = os.environ.get('MAILGUN_URL')
    # "https://api.mailgun.net/v3/sandbox0494fd345970485dbcc98b1aa757bd19.mailgun.org/messages"
APIKEY = os.environ.get('MAILGUN_API_KEY')
    # "key-f7dd3239713abc6c481f005d12290bff"
FROM = os.environ.get('MAILGUN_FROM')
    # "postmaster@sandbox0494fd345970485dbcc98b1aa757bd19.mailgun.org"
TO = os.environ.get('MAILGUN_TO')
    # "Kevin Bardool <kbardool@outlook.com>"
SUBJECT = "Hello Kevin Bardool"