from werkzeug.security import generate_password_hash
from app_student import query

def test_add_book_as_admin(client):
    # Create admin manually
    query("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
          ("admin1", generate_password_hash("pass"), "admin"))

    # Log in as admin
    client.post("/login", data={"username": "admin1", "password": "pass"})

    # Add book
    res = client.post("/add_book", data={
        "title": "Test Book",
        "author": "Someone",
        "year": "2024",
        "language": "English"
    })

    assert res.status_code in (200, 302)

    book = query("SELECT * FROM books WHERE title=?", ("Test Book",), fetchone=True)
    assert book is not None
