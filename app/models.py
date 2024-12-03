'''
Team Bareustoph: Ben Rudinski, Tiffany Yang, Endrit Idrizi, Tim Ng
SoftDev
P01: ArRESTed Development - Global Bites
2024-11-27
Time Spent: 1.2
'''

# imports
import sqlite3
from hashlib import sha256
import hmac
import datetime

class User:
    """model for the user  """
    @staticmethod
    def get_by_username(username):
        """ retrieve user by their usrname """
        with sqlite3.connect("thread.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user_data = cursor.fetchone()
            if user_data:
                return User(*user_data)
            return None

    @staticmethod
    def create(username, password):
        """ create a user with two variables :)"""
        hashed_password = User.hash_password(password)
        badges = ' ' # default value for badges
        join_date = int(datetime.datetime.now().timestamp()) # make current time join date
        try:
            with sqlite3.connect("thread.db") as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (username, password_hash, join_date, badges) VALUES (?, ?, ?, ?)", (username, hashed_password, join_date, badges))
                conn.commit()
        except sqlite3.IntegrityError:
            return False
        return True

    @staticmethod
    def verify_password(stored_password, provided_password):
        """ check given password against stored one """
        hashed_provided_password = User.hash_password(provided_password)
        return hmac.compare_digest(stored_password, hashed_provided_password)
    
    @staticmethod
    def hash_password(password):
        return sha256(password.encode()).hexdigest()

    @staticmethod
    def get_by_id(user_id):
        """ get user by their id """
        with sqlite3.connect("thread.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                return User(*user_data)
            return None

    def __init__(self, id, username, password_hash, join_date, badges, recents=None):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.join_date = join_date
        self.badges = badges
        self.recents = recents











        










