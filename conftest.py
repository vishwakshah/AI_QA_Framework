import pytest
# Import Pytest because we are creating a Pytest fixture.

from api_clients.user_api import User_API
# Import our API client class so the fixture can create a User_API object.


@pytest.fixture
def api():
    # This fixture creates a User_API object for any test that requests "api".

    return User_API()
    # Return the object to the test.