import os
import logging
import pytest
import yaml
import json
import requests_mock


@pytest.fixture(scope="session")
def api_config():
    """Loads API configuration from JSON file."""
    file_path = os.path.join(os.path.dirname(__file__), "..", "config", "api_config.json")
    with open(file_path, "r") as file:
        data = json.load(file)
    return data  # Returns {"base_url": "https://jsonplaceholder.typicode.com"}


# Ensure logs directory exists
LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# Configure logging
log_file_path = os.path.join(LOG_DIR, "test.log")
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


@pytest.fixture
def logger(request):
    """Returns a logger instance."""
    return logging.getLogger(request.module.__name__)


@pytest.fixture
def mock_api():
    """Mocks API responses using requests-mock."""
    with requests_mock.Mocker() as mock:
        # Mock login API response
        mock.post(
            "https://api.example.com/auth/login",
            additional_matcher=lambda request: request.json() == {"username": "test", "password": "pass"},
            json={"token": "fake_token"},
            status_code=200
        )
        # Mock user info API response
        mock.get("https://api.example.com/users/1", json={"id": 1, "name": "Test User"}, status_code=200)

        # Add a default response for incorrect credentials
        mock.post(
            "https://api.example.com/auth/login",
            json={"error": "Invalid credentials"},
            status_code=401
        )

        yield mock  # Provide the mock instance


@pytest.fixture
def user_data():
    """Loads user data from YAML file."""
    # Build absolute path to user_data.yaml
    file_path = os.path.join(os.path.dirname(__file__), "..", "config", "user_data.yaml")
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    return data


def load_user_data():
    """Loads users data from JSON file at the start."""
    file_path = os.path.join(os.path.dirname(__file__), "..", "config", "json_data.json")
    with open(file_path, "r") as file:
        data = json.load(file)
    return data["users"]  # Return list of users

# Pytest fixture (not used for parameterization)
@pytest.fixture
def user_json_data():
    """Returns JSON test data."""
    return load_user_data()

# Parameterizing the test dynamically
def pytest_generate_tests(metafunc):
    """Dynamically parameterize tests with JSON user data."""
    if "user_json_data" in metafunc.fixturenames:
        metafunc.parametrize("user_json_data", load_user_data())


@pytest.fixture
def config_data():
    return {"environment": "staging",
            "db_url": "postgres://user:pass@localhost:5432/test_db"
            }
