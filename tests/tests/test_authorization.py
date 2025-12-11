from app import create_app

def test_admin_auth():
    app = create_app()
    client = app.test_client()

    # ---- Not logged in -> should be blocked ----
    r = client.get("/manage_users")
    assert r.status_code == 403

    # ---- Normal user -> still blocked ----
    client.post("/register", data={"username": "u1", "password": "1"})
    client.post("/login", data={"username": "u1", "password": "1"})
    r = client.get("/manage_users")
    assert r.status_code == 403

    # ---- Admin user -> allowed ----
    client.get("/logout")
    client.post("/register", data={"username": "James1", "password": "2"})
    client.post("/login", data={"username": "James1", "password": "2"})
    r = client.get("/manage_users")
    assert r.status_code == 403
