from database import query
from config import Config
DB = Config.DATABASE

def borrow_book(username, book_id):
    query(DB, "UPDATE books SET available=0 WHERE id=?", (book_id,))
    return query(DB, "INSERT INTO borrow (username, book_id, status) VALUES (?, ?, ?)", (username, book_id, "borrowed"))

def return_book(username, book_id):
    query(DB, "UPDATE books SET available=1 WHERE id=?", (book_id,))
    return query(DB, "INSERT INTO borrow (username, book_id, status) VALUES (?, ?, ?)", (username, book_id, "returned"))

def get_history_for_user(username):
    return query(DB, """
        SELECT borrow.*, books.title
        FROM borrow JOIN books ON borrow.book_id = books.id
        WHERE borrow.username=?
        ORDER BY borrow.id DESC
    """, (username,), fetchall=True)
