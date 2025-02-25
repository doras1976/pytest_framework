import random
import requests
import pytest


def test_create_user_from_json(api_config, user_test_data):
    """Test creating users with data from JSON."""
    url = f"{api_config['base_url']}/users"
    headers = {
        "Authorization": f"Bearer {api_config['access_token']}",
        "Content-Type": "application/json"
    }
    email = f"testuser{random.randint(1000, 9999)}@example.com"
    payload = {
        "name": user_test_data['name'],
        "gender": user_test_data['gender'],
        "email": email,
        "status": user_test_data['status']
    }
    response = requests.post(url, json=payload, headers=headers)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == user_test_data['name']
    assert data["email"] == email
    assert data["status"] == user_test_data['status']


def test_get_users(api_config):
    """Test fetching users with authentication."""
    url = f"{api_config['base_url']}/users"
    headers = {
        "Authorization": f"Bearer {api_config['access_token']}"
    }
    response = requests.get(url, headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_update_delete_user(api_config):
    """Test creating, updating and deleting a new user with authentication - gorest.co.in"""
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

    user_id = data['id']
    # update user
    update_payload = {
        "name": "John Doe Updated",
        "email": email,
        "status": "inactive"
    }
    update_response = requests.put(f"{api_config['base_url']}/users/{user_id}", json=update_payload, headers=headers)

    # Validate response
    assert update_response.status_code == 200  # Ensure update was successful
    updated_data = update_response.json()
    assert updated_data["id"] == user_id
    assert updated_data["name"] == "John Doe Updated"
    assert updated_data["status"] == "inactive"

    # Delete the user
    delete_response = requests.delete(f"{api_config['base_url']}/users/{user_id}", headers=headers)

    # Validate deletion was successful
    assert delete_response.status_code == 204  # Expecting No Content (204)

    # Try to GET the deleted user (should return 404)
    get_response = requests.get(f"{api_config['base_url']}/users/{user_id}", headers=headers)
    assert get_response.status_code == 404  # Expecting Not Found (404)