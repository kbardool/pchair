import uuid
from common.database import Database
import models.stores.errors as StoreErrors


__author__ = 'KBardool'

class Store(object):

    def __init__(self, name, url_prefix, tag_name, query, _id=None):
        self.name       = name
        self.url_prefix = url_prefix
        self.tag_name   = tag_name
        self.query      = query
        self._id = uuid.uuid4().hex if _id is None else _id
        print('    Store constructor complete')
        return

    def __repr__(self):
        return "<The Store is {} >".format(self.name)


    def json(self):
        return {
            "_id":          self._id,
            "name":         self.name,
            "url_prefix":   self.url_prefix,
            "tag_name":     self.tag_name,
            "query":        self.query
        }


    def save_to_db(self):
        Database.update("stores",{"_id": self._id}, self.json())

    @classmethod
    def get_by_id(cls, store_id):
        print('   store/get_by_id()', store_id)
        store_data = Database.find_one("stores", {"_id": store_id})
        return cls(**store_data)

    @classmethod
    def get_by_name(cls, store_name):
        store_data = Database.find_one("stores", {"name": store_name})
        return cls(**store_data)

    @classmethod
    def get_by_url_prefix(cls, url_prefix ):
        print('   stores.get_by_url_prefix()', url_prefix)
        store_data = Database.find_one("stores", {"url_prefix": {"$regex":'^{}'.format(url_prefix)}})
        print('   ------------------------')
        return cls(**store_data)

    @classmethod
    def find_by_url(cls, url):
        print('   Store.find_by_url: ',url)
        for i in range(1, len(url)+1):
            print('   Searching:', url[:i])
            try:
                store = cls.get_by_url_prefix(url[:i])
                print('   store.find_by_url(): ', store)
                return store
            except:
                raise StoreErrors.StoreNotFoundException("The URL Prefix used to find the store didn't not have any matches!")


    def delete(self):
        print('   store.delete()')
        Database.delete("stores", {"_id": self._id})
        print('   Store Deleted')


    @classmethod
    def all(cls):
        p = Database.find("stores", {})
        return [ cls(**elem) for elem in p]
