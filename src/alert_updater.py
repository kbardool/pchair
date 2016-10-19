from common.database import Database
from models.alerts.alert import Alert

__author__ = 'KBardool'

Database.initialize()
alerts_needing_update = Alert.find_needed_update()
print('alerts needing update',len(alerts_needing_update))


for alert in alerts_needing_update:
    print('=====> last updated:', alert.last_checked)
    alert.load_item_price()
    alert.send_email_if_price_reached()


# > use fullstack
# > db.users.insert({"_id": "1234", "email": "test@test.com", "password": "$pbkdf2-sha256$7665$WKs1ZkwJ4ZxT6t07R0iplQ$ZKfMMAMzKxH64g.3XwaFONAlVwoZf76dWdqW6uSlQtE"})
# > db.stores.insert({"_id": "a980989112d746a793448e706a6ad976", "query": {"class": "now-price", "itemprop": "price"}, "tag_name": "span", "name": "John Lewis", "url_prefix": "http://www.johnlewis.com"})
# > db.items.insert({"_id": "d5527d22c0a74a8199fbbc0aab440463", "url": "http://www.johnlewis.com/john-lewis-the-basics-dexter-low-wide-bookcase/p562355", "price": 45, "name": "Dexter" })
# > db.alerts.insert({"_id": "896045e647084cacb37a702f418be707", "price_limit": 100, "last_checked": ISODate("2016-02-09T10:35:31.542Z"), "item_id": "d5527d22c0a74a8199fbbc0aab440463", "user_email": "test@test.com"})
# > db.alerts.insert({"_id": "896045e647084cacb37a702f418be706", "price_limit": 50, "last_checked": ISODate("2016-02-08T10:35:31.542Z"), "item_id": "d5527d22c0a74a8199fbbc0aab440463", "user_email": "test@test.com"})