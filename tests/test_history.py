from app import create_app

def test_history_page():
    app = create_app()
    client = app.test_client()

    # Register + login
    client.post("/register", data={"username": "histUser", "password": "123"})
    client.post("/login", data={"username": "histUser", "password": "123"})

    # Access history page
    r = client.get("/history")
    assert r.status_code == 200
