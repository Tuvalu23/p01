'''
Team Bareustoph: Ben Rudinski, Tiffany Yang, Endrit Idrizi, Tim Ng
SoftDev
P01: ArRESTed Development - Global Bites
2024-11-27
Time Spent: 0.5
'''

import sqlite3
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, 'thread.db')

def setup_database():
    conn = sqlite3.connect(DB_PATH)
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                join_date INTEGER,
                badges TEXT NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Comments (
                comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                recipe_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                comment_time INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id)
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Recipes (
                recipe_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                ingredients TEXT,
                instructions TEXT,
                cuisine TEXT,
                image_url TEXT
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Badges (
                badge_id INTEGER PRIMARY KEY AUTOINCREMENT,
                badge_name TEXT NOT NULL,
                description TEXT NOT NULL,
                icon_url TEXT NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS RecentHistory (
                history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                recipe_id INTEGER NOT NULL,
                interaction_type TEXT NOT NULL,
                comment_time INTEGER,
                FOREIGN KEY (user_id) REFERENCES users(id),
                FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id)
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS RecipeVotes (
            recipe_id INTEGER PRIMARY KEY,
            upvotes INTEGER DEFAULT 0,
            downvotes INTEGER DEFAULT 0,
            FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id)
        )
    ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS UserRecipeVotes (
            user_id INTEGER,
            recipe_id INTEGER,
            vote INTEGER,
            PRIMARY KEY (user_id, recipe_id),
            FOREIGN KEY (user_id) REFERENCES Users(id),
            FOREIGN KEY (recipe_id) REFERENCES Recipes(recipe_id)
        );

    ''')
    conn.close()

if __name__ == "__main__":
    setup_database()


# Users -done
# user_id (primary key)
# username
# password_hash
# join_date (unix time stamp?)
# badges

# Comments
# comment_id (primary key)
# user_id (foreign key) recipe_id (foreign
# key)
# text
# timestamp

# Recipes
# recipe_id (primary
# key)
# title
# ingredients
# instructions
# cuisine
# image_url

# Badges
# badge_id (primary key) badge_name
# description icon_url
