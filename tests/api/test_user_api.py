import pytest
# Import Pytest because we use Pytest features
# such as @pytest.mark.parametrize.


from jsonschema import validate
# Import the validate function from jsonschema.
# It compares our API response against the schema we define.


from validators.response_validator import (
    validate_status_code,
    validate_response_not_empty
)
# Import both reusable validation functions.


def test_get_users(api):
    # "api" is provided automatically by the Pytest fixture.

    response = api.get_users()
    # Call the GET /users API.
    # The API response is stored in the "response" variable.

    validate_status_code(response, 200)
    # Send the actual API response and expected status code
    # to our reusable validator.

    validate_response_not_empty(response)
    # Use the reusable validator to check that the response is not empty.

    users = response.json()
    # Convert the API response into Python data.
    # "users" is our own variable containing the actual API response.


    expected_names = [
        "Leanne Graham",
        "Ervin Howell",
        "Clementine Bauch",
        "Patricia Lebsack",
        "Chelsey Dietrich"
    ]
    # Expected names for the first five users.


    for i in range(5):
        # Loop through the first five users.

        assert users[i]["name"] != ""
        # Check that each user's name is not empty.

        assert users[i]["name"] == expected_names[i]
        # Check that the actual name matches the expected name.


    schema = {
        "type": "array",
        # The API response should be an array/list of users.

        "items": {
            "type": "object",
            # Each item inside the array should be an object/dictionary.

            "properties": {
                "id": {"type": "integer"},
                # The user's ID should be an integer.

                "name": {"type": "string"},
                # The user's name should be a string.

                "username": {"type": "string"},
                # The username should be a string.

                "email": {"type": "string"}
                # The email should be a string.
            },

            "required": [
                "id",
                "name",
                "username",
                "email"
            ]
            # Every user object must contain these four fields.
        }
    }


    validate(
        instance=users,
        # "instance" is the parameter name defined by the jsonschema library.
        # "users" is our own variable containing the actual API response.

        schema=schema
        # "schema" is the parameter expected by validate().
        # Our variable "schema" contains the expected structure
        # and data types of the API response.
    )
    # validate() compares the actual API response with our schema.
    # If the response structure or data types are wrong,
    # JSON Schema validation will fail.


def test_create_user(api):
    # "api" is provided by the Pytest fixture.

    payload = {
        "id": 11,
        "name": "vish",
        "username": "vishhsiv"
    }

    headers = {
        "Content-Type": "application/json"
    }

    Post_response = api.create_user(payload, headers)
    # Use the "api" object provided by the fixture.
    # We no longer create User_API() manually here.

    assert Post_response.status_code == 201
    # Verify that the API created the user successfully.


def test_get_users_with_token(api):

    token = "abc123"
    # In a real project, this would come from a login/authentication API.
    # We are using a sample token here only to learn the structure.

    response = api.get_users_with_token(token)

    assert response.status_code == 200
    # Verify that the API returned a successful response.


def test_get_access_token(api):

    token_url = "https://funapi.dev/api/auth/v1/oauth/token"
    # OAuth 2.0 token endpoint.

    client_id = "demo-client"
    # Demo client ID provided by Fun API documentation for OAuth practice.
    # This is a public demo credential, not our own real client ID.

    client_secret = "demo-secret"
    # Demo client secret provided by Fun API documentation for OAuth practice.
    # In a real project, secrets should NOT be hardcoded in test code.

    response = api.get_access_token(
        token_url,
        client_id,
        client_secret
    )

    print(response.status_code)
    print(response.text)

    assert response.status_code == 200
    # Token request should succeed.

    token = response.json()["access_token"]
    # Extract the access token from the JSON response.

    assert token != ""
    # Make sure an access token was actually returned.


@pytest.mark.parametrize(
    "user_id",
    [
        99999,
        88888,
        77777
    ]
)
# Parametrization allows us to use multiple test data values
# with ONE test function.
#
# "user_id" is the parameter name.
# 99999, 88888 and 77777 are the test data.
#
# Pytest will run the same test function three times:
# test_invalid_user(99999)
# test_invalid_user(88888)
# test_invalid_user(77777)


def test_invalid_user(api, user_id):
    # "api" comes from the Pytest fixture.
    # "user_id" comes from @pytest.mark.parametrize.

    response = api.get_user(user_id)
    # Call get_user() using the current user_id.

    assert response.status_code == 404
    # 404 means "Not Found".
    # We expect the API to return 404 for each invalid user ID.