import uuid

from common.database import Database
import models.users.errors as UserErrors
from common.utils import Utils
from models.alerts.alert import Alert

__author__ = 'KBardool'


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {} >".format(self.email)

    @staticmethod
    def is_login_valid(email, password):
        """
        This method verifies that an email/password combo is valid
        checks that the email exits and the password associated is correct
        :param email:  The user's email  address
        :param password: The users sha512 hashed password
        :return: True is user is valid, otherwise false
        """
        print('   User.is_login_valid')
        user_data = Database.find_one('users', {"email": email})
        if user_data is None:
            raise UserErrors.UserNotExistsError("Your user does not exist.")

        if not Utils.check_hashed_password(password, user_data['password']):
            # incorrect password
            raise UserErrors.IncorrectPasswordError(" Your Password was wrong.")

        return True

    @staticmethod
    def register_user(email, password):
        """

        :param email:
        :param password:
        :return:
        """
        print('   User.register_user')
        user_data = Database.find_one('users', {"email": email})
        if user_data is not None:
            raise UserErrors.UserAlreadyRegistered("The email you used to register already exists.")

        if not Utils.email_is_valid(email):
            # invalid email format
            raise UserErrors.InvalidEmailError("Your email id is not formatted correctly")

        #all checks passed , create new user and save to DB
        print('   Create new user')
        User(email, Utils.hash_password(password)).save_to_db()

        return True


    def json(self):
        return {
            "email": self.email,
            "password": self.password,
            "_id": self._id
        }


    def save_to_db(self):
        Database.insert("users", self.json())

    @classmethod
    def find_by_email(cls,email):
        d1 = Database.find_one("users",{"email":email})
        return cls(**d1)

    def get_alerts(self):
        print('   user.get_alerts()')
        alerts = Alert.find_by_user_email(self.email)
        print('   user.get_alerts() :', alerts)
        return alerts