from passlib.hash import pbkdf2_sha512

import re, requests

__author__ = 'KBardool'


class Utils(object):
    @staticmethod
    def hash_password(password):
        """
        Hashes a  password using pbkdf2_sha512

        :param password: sha512 password from the login /register form
        :return: A sha512 --> pbkdf2_sha512 enrypted password
        """
        print('   utils.hash_password password:',password)
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checks password sent by user matches password on database
        The database password is encrypted more than the user's password at this stage
        :param password: sha512-hashed password
        :param hashed_password: pbkdf2_sha512 encrypted password
        :return: True is passwords match, false otherwise
        """
        print('   utils.checked_hashed_password \n   password:',password, '\n   hashed password:',hashed_password)
        try:
            p = pbkdf2_sha512.verify(password, hashed_password)
        except:
            print("   xan error was encountered ")
            p = False
        return p


    @staticmethod
    def email_is_valid(email):
        email_matcher = re.compile('^[\w.-]+@([\w-]+\.)+[\w]+$')

        return True if email_matcher.match(email) else False

    @classmethod
    def send_email(cls, url, apikey, from_addr, to_addr, subject, body):
        print('   utils.send_email ')
        resp =  requests.post(
            url,
            auth=("api", apikey),
            data={"from"   : from_addr,
                  "to"     : to_addr,
                  "subject": subject,
                  "text"   : body})
        print('   send_email: rc:',resp)