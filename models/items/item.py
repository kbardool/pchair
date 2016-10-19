import re
import uuid

import requests
from bs4 import BeautifulSoup

from common.database import Database
from models.stores.store import Store

__author__ = 'KBardool'

class Item(object):

    def __init__(self, name, url, price = None , _id=None):
        self.name     = name
        self.url      = url
        # self.store  = store
        store         = Store.find_by_url(url)
        self.tag_name = store.tag_name
        self.query    = store.query
        self.price    = price
        # self.price  = self.load_price(tag_name, query)
        self._id      = uuid.uuid4().hex if _id is None else _id
        print('   Item constructor complete')
        return


    def __repr__(self):
        return "<Item {} with URL {}>".format(self.name, self.price)


    def load_price(self):
        # eg. query= {"itemprop": "price", "class": "now-price"}
        # eg. tag_name = "span"
        request = requests.get(self.url)
        content = request.content
        soup    = BeautifulSoup(content,"html.parser")
        element = soup.find(self.tag_name, self.query)
        string_price = element.text.strip()

        pattern = re.compile('(\d+.\d+)')
        match = pattern.search(string_price)

        self.price = float(match.group())
        return self.price


    def json(self):
        return {
            "_id"   :   self._id,
            "name"  :   self.name,
            "url"   :   self.url,
            "price" :   self.price,
            # "store":  self.store
        }


    def save_to_db(self):
        Database.update("items", {"_id": self._id}, self.json())

    @classmethod
    def get_by_id(cls, _id):
        item_data = Database.find_one("items", {"_id": _id})
        return cls(**item_data)