from werkzeug.security import generate_password_hash
from app_student import query

def test_borrow_and_return(client):
    # Create user
    query("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
          ("user1", generate_password_hash("pw"), "user"))

    # Create book
    query("INSERT INTO books (title, author, year, language, available) VALUES (?, ?, ?, ?, ?)",
          ("Borrowable", "Auth", "2020", "EN", 1))

    # Login
    client.post("/login", data={"username": "user1", "password": "pw"})

    # Get book ID
    book = query("SELECT * FROM books WHERE title=?", ("Borrowable",), fetchone=True)

    # Borrow
    client.get(f"/borrow/{book['id']}")

    updated = query("SELECT * FROM books WHERE id=?", (book["id"],), fetchone=True)
    assert updated["available"] == 0

    # Return
    client.get(f"/return/{book['id']}")

    updated = query("SELECT * FROM books WHERE id=?", (book["id"],), fetchone=True)
    assert updated["available"] == 1
