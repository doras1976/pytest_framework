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
    return data


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
        def match_login_request(request):
            """Custom matcher to check if request JSON contains required fields."""
            try:
                json_data = request.json()
                return (
                    isinstance(json_data, dict) and
                    json_data.get("username") == "test" and
                    json_data.get("password") == "pass"
                )
            except:
                return False

        # Mock login API response (handling port 443 explicitly)
        for login_url in [
            "https://api.example.com/auth/login",
            "https://api.example.com:443/auth/login"  # Include port 443 variation
        ]:
            mock.post(
                login_url,
                additional_matcher=match_login_request,
                json={"token": "fake_token"},
                status_code=200
            )

        # Mock user info API response
        mock.get("https://api.example.com/users/1", json={"id": 1, "name": "Test User"}, status_code=200)

        # Default response for incorrect credentials
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


# Load user test data at module level (before test execution)
def load_user_test_data():
    """Loads test data from JSON file before pytest runs."""
    file_path = os.path.join(os.path.dirname(__file__), "..", "config", "user_test_data.json")
    with open(file_path, "r") as file:
        return json.load(file)


# Pytest fixture (not used for parameterization)
@pytest.fixture
def user_json_data():
    """Returns JSON test data."""
    return load_user_data()


@pytest.fixture(scope="session")
def user_test_data():
    """Provides test data for tests."""
    return load_user_test_data()


# Parameterizing the test dynamically
def pytest_generate_tests(metafunc):
    """Dynamically injects test cases into parameterized tests."""
    if "user_test_data" in metafunc.fixturenames:
        metafunc.parametrize("user_test_data", load_user_test_data())
    if "user_json_data" in metafunc.fixturenames:
        metafunc.parametrize("user_json_data", load_user_data())


@pytest.fixture
def config_data():
    return {"environment": "staging",
            "db_url": "postgres://user:pass@localhost:5432/test_db"
            }
