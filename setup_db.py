'''
Team Bareustoph: Ben Rudinski, Tiffany Yang, Endrit Idrizi, Tim Ng
SoftDev
P01: ArRESTed Development - Global Bites
2024-11-27
Time Spent: 0.5
'''


import sqlite3

def setup_database():
    conn = sqlite3.connect('thread.db')
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                join_date INTEGER NULL,
                badges TEXT NOT NULL

            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Comments (
                comment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                recipe_id INTEGER NOT NULL,
                text TEXT NOT NULL,
                comment_time INTEGER NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Recipes (
                recipe_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                ingredients TEXT NOT NULL,
                instructions TEXT NOT NULL,
                cuisine TEXT NULL,
                image_url TEXT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS Badges (
                badge_id INTEGER NULL,
                badge_name TEXT NOT NULL,
                description TEXT NOT NULL,
                icon_url TEXT NOT NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS RecentHistory(
                history_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                recipe_id INTEGER NOT NULL,
                interaction_type TEXT NOT NULL,
                comment_time INTEGER NULL
            )
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
