import logging
import requests
from jsonschema import validate
from schemas.schemas import UserSchema, USER_SCHEMA

import requests


def test_validate_user_response_json(mock_api):
    response = requests.get("https://api.example.com/users/1")
    assert response.status_code == 200

    # Validate response JSON against JSON schema
    validate(instance=response.json(), schema=USER_SCHEMA)


def test_validate_user_response_schemas(mock_api):
    """Validates API response structure using pydantic."""
    response = requests.get("https://api.example.com/users/1")
    assert response.status_code == 200

    # Validate response JSON against UserSchema
    user = UserSchema(**response.json())  # Converts the response into a UserSchema object; Raises error if structure is incorrect
    assert user.id == 1
    assert user.name == "Test User"


def test_mocked_login(mock_api):
    """Tests the mocked login API response."""
    response = requests.post("https://api.example.com/auth/login", json={"username": "test", "password": "pass"})
    assert response.status_code == 200
    assert "token" in response.json()
    assert response.json()["token"] == "fake_token"


def test_mocked_login_fail(mock_api):
    """Tests the mocked login API response."""
    response = requests.post("https://api.example.com/auth/login", json={"username": "test", "password": "pas"})
    assert response.status_code == 401
    assert response.json()["error"] == "Invalid credentials"


def test_mocked_user_info(mock_api):
    """Tests the mocked user info API response."""
    response = requests.get("https://api.example.com/users/1")
    assert response.status_code == 200
    assert response.json()['id'] == 1
    assert response.json()['name'] == "Test User"


def test_user_data(user_data):
    assert user_data["username"] == "test_user"
    assert user_data["password"] == "secure123"


def test_config(config_data):
    assert config_data["environment"] == "staging"


def test_api_url(user_json_data):
    assert "username" in user_json_data
    assert "user" in user_json_data["username"]
    assert "password" in user_json_data
    assert "@" in user_json_data["email"]


def test_invalid_username(user_data):
    """Test with an empty username."""
    assert user_data["username"] != "", "Username should not be empty"


def test_logging_example(logger, caplog):
    """Test that logs messages and verifies log output."""
    with caplog.at_level(logging.INFO):
        logger.info("Starting test execution.")
        assert 2 + 2 == 4
        assert "Starting test execution." in caplog.text  # Verify log

