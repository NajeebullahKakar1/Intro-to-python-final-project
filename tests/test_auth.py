def test_register_and_login(client):
    # Register user
    register = client.post("/register", data={
        "username": "testuser",
        "password": "1234"
    }, follow_redirects=True)
    assert register.status_code == 200

    # Login with same user
    login = client.post("/login", data={
        "username": "testuser",
        "password": "1234"
    }, follow_redirects=True)
    assert login.status_code == 200
    assert b"Welcome" in login.data
