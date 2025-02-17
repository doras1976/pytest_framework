import random
import requests


def test_get_users(api_config):
    """Test fetching users with authentication."""
    url = f"{api_config['base_url']}/users"
    headers = {
        "Authorization": f"Bearer {api_config['access_token']}"
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_user(api_config):
    """Test creating a new user with authentication - gorest.co.in"""
    url = f"{api_config['base_url']}/users"
    headers = {
        "Authorization": f"Bearer {api_config['access_token']}",
        "Content-Type": "application/json"
    }
    email = f"testuser{random.randint(1000, 9999)}@example.com"
    payload = {
        "name": "John Doe",
        "gender": "male",
        "email": email,
        "status": "active"
    }
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["email"] == email
