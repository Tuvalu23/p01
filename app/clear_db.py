import sqlite3

DB_PATH = 'thread.db' 

def clear_database():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        for table in tables:
            table_name = table[0]
            cursor.execute(f"DELETE FROM {table_name};")
            cursor.execute(f"UPDATE SQLITE_SEQUENCE SET SEQ=0 WHERE NAME='{table_name}';")  # Reset autoincrement
            print(f"Cleared table: {table_name}")

        conn.commit()
        print("Database cleared successfully!")
    except sqlite3.Error as e:
        print(f"Error clearing database: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    clear_database()