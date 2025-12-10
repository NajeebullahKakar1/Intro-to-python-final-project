"""database.py - sqlite helpers"""
"""
This file handles all the database work for the library project.
I wanted to keep things simple, so all the SQL queries go through here.

Functions here help the rest of the app by:
- opening a connection to the SQLite database
- running queries
- creating the tables the first time the app runs

Having the database stuff in one place makes the rest of the project cleaner.
"""


import sqlite3

def get_conn(path):
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn

def query(db_path, sql, params=(), fetchone=False, fetchall=False):
    conn = get_conn(db_path)
    cur = conn.cursor()
    cur.execute(sql, params)
    conn.commit()
    if fetchone:
        row = cur.fetchone()
        conn.close()
        return row
    if fetchall:
        rows = cur.fetchall()
        conn.close()
        return rows
    conn.close()
    return None

"""
The init_db() function sets up the database tables when the app starts.
It creates three tables:

1. users  → stores usernames, passwords, and roles (admin or normal user)
2. books  → stores all book details (title, author, year, etc.)
3. borrow → keeps track of which user borrowed which book

If the tables already exist, it doesn’t recreate them. This just makes
sure the project has all the required tables.
"""



def init_db(db_path):
    conn = get_conn(db_path)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT DEFAULT 'user'
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            author TEXT,
            year TEXT,
            language TEXT,
            available INTEGER DEFAULT 1
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS borrow (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            book_id INTEGER,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()
