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
                recents INTERGER NULL
            )
        ''')
        conn.execute('''
            CREATE TABLE IF NOT EXISTS threads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
    conn.close()

if __name__ == "__main__":
    setup_database()



# Users
# user_id (primary key)
# username
# password_hash
# join_date
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
