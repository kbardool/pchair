import uuid
import datetime
from common.utils import Utils
from common.database import Database
from models.items.item import Item
import models.alerts.constants as AlertConstants

__author__ = 'KBardool'


class Alert(object):


    def __init__(self, user_email, price_limit, item_id, active=True, _id=None, last_checked=None):
        print('    Alert constructor')
        self.user_email     = user_email
        self.price_limit    = float(price_limit)
        self.item_id        = item_id
        self.item           = Item.get_by_id(item_id)
        self.active         = active
        self.last_checked   = datetime.datetime.utcnow() if last_checked is None else last_checked
        self._id            = uuid.uuid4().hex if _id is None else _id

        print('    Alert constructor complete')


    def __repr__(self):
        return "<Alert for: {} on item id: {} item name: {}  with price limit: {}>" \
            .format(self.user_email, self.item_id, self.item.name, self.price_limit)


    @classmethod
    def find_needed_update(cls, minute_since_update=1):
        last_updated_limit = datetime.datetime.utcnow() - datetime.timedelta(minutes=minute_since_update)
        print('   alert.find_needed_update(): last_updated_limit =', last_updated_limit)
        alerts = Database.find("alerts", {"last_checked": {"$lte": last_updated_limit}, "active": True})
        return [cls(**elem) for elem in alerts]

    def json(self):
        return {
            "_id"           : self._id,
            "price_limit"   : self.price_limit,
            "last_checked"  : self.last_checked,
            "user_email"    : self.user_email,
            "item_id"       : self.item._id,
            "active"        : self.active
        }

    def save_to_db(self):
        Database.update("alerts", {"_id": self._id}, self.json())
        return

    def load_item_price(self):
        self.item.load_price()
        self.last_checked = datetime.datetime.utcnow()
        self.save_to_db()
        self.item.save_to_db()
        return self.item.price

    def send_email_if_price_reached(self):
        print('   criteria:  <', self.item.name,'>  Alert price:', self.price_limit, ' Current price:', self.item.price)
        if self.item.price <= self.price_limit:
            print('   An alert has been triggered')
            self.send()

    def send(self):
        Body = "We've found a deal! ({}). To navigate to the alert visit {}".format(
            self.item.url,
            "http://endpoint.com/alerts/{}".format(self._id))
        print('   send: ', AlertConstants.APIKEY)
        Utils.send_email(AlertConstants.URL,
                         AlertConstants.APIKEY,
                         AlertConstants.FROM,
                         "kbardool@outlook.com",
                         "Price Limit reached for {}".format(self.item.name),
                         Body)

    @classmethod
    def find_by_user_email(cls, user_email):
        print('   alert.find_by_user_email()', user_email)
        d1 = Database.find("alerts", {"user_email": user_email})
        return [cls(**elem) for elem in d1]

    @classmethod
    def find_by_id(cls, alert_id):
        print('   alert.find_by_id()', alert_id)
        d1 = Database.find_one("alerts", {"_id": alert_id})
        return cls(**d1)

    def deactivate(self):
        self.active = False
        self.save_to_db()

    def activate(self):
        self.active = True
        self.save_to_db()

    def delete(self):
        print('   alert.delete()')
        Database.delete("alerts", {"_id": self._id})
        print('   Alert Deleted')
