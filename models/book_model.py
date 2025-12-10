from database import query
from config import Config
DB = Config.DATABASE

def add_book(title, author, year, language):
    return query(DB, "INSERT INTO books (title, author, year, language) VALUES (?, ?, ?, ?)", (title, author, year, language))

def get_all_books():
    return query(DB, "SELECT * FROM books", fetchall=True)

def search_books(q):
    like = f"%{q}%"
    return query(DB, "SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR language LIKE ? OR year LIKE ?", (like, like, like, like), fetchall=True)

def get_book(book_id):
    return query(DB, "SELECT * FROM books WHERE id=?", (book_id,), fetchone=True)

def update_book(book_id, title, author, year, language, available):
    return query(DB, "UPDATE books SET title=?, author=?, year=?, language=?, available=? WHERE id=?", (title, author, year, language, available, book_id))

def delete_book(book_id):
    return query(DB, "DELETE FROM books WHERE id=?", (book_id,))
