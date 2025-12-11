from app import create_app

def test_books():
    app = create_app()
    client = app.test_client()

    # ---- Normal user cannot add books ----
    client.post("/register", data={"username": "u2", "password": "x"})
    client.post("/login", data={"username": "u2", "password": "x"})
    r = client.post("/add_book", data={
        "title": "Blocked",
        "author": "Nope",
        "year": "2020",
        "language": "EN"
    })
    assert r.status_code == 403  # blocked

