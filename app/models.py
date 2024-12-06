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
import os
import datetime

# Define the path to the database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "thread.db")

class User:
    """Model for a user."""

    @staticmethod
    def get_by_username(username):
        """Retrieve a user by their username."""
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user_data = cursor.fetchone()
            if user_data:
                return User(*user_data)
            return None

    @staticmethod
    def create(username, password):
        """Create a new user with a username and password."""
        hashed_password = User.hash_password(password)
        badges = ''  # Default value for badges
        join_date = int(datetime.datetime.now().timestamp())  # Current timestamp
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO users (username, password_hash, join_date, badges) VALUES (?, ?, ?, ?)",
                    (username, hashed_password, join_date, badges)
                )
                conn.commit()
        except sqlite3.IntegrityError as e:
            print(f"IntegrityError: {e}")  # Log the error for debugging
            return False
        return True

    @staticmethod
    def verify_password(stored_password, provided_password):
        """Verify a given password against the stored hash."""
        hashed_provided_password = User.hash_password(provided_password)
        return hmac.compare_digest(stored_password, hashed_provided_password)

    @staticmethod
    def hash_password(password):
        """Hash a password using SHA256."""
        return sha256(password.encode()).hexdigest()

    @staticmethod
    def get_by_id(user_id):
        """Retrieve a user by their ID."""
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user_data = cursor.fetchone()
            if user_data:
                return User(*user_data)
            return None
        
    def set_password(self, password):
        """ hash and update """
        self.password_hash = self.hash_password(password)
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (self.password_hash, self.id))
            conn.commit()


    def __init__(self, id, username, password_hash, join_date, badges, recents=None):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.join_date = datetime.datetime.fromtimestamp(join_date) if join_date else None
        self.badges = badges.split(',') if badges else []
        self.recents = recents or []











        










