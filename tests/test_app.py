from app_student import app

def test_home_page_requires_login(client):
    response = client.get("/")
    assert response.status_code in (302, 401, 403)
