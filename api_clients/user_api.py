import requests
# Import requests so Python can send HTTP requests.

from config.config import BASE_URL
# Import the common API base URL from our configuration file.

class User_API:
    # This class will contain our User API methods.

    def get_users(self):
        # This method will call the API and get the users.

        response = requests.get(
            f"{BASE_URL}/users"
        )
        # requests.get() sends a GET request to the URL.
        # The API response is stored in the "response" variable.

        return response
        # Return the response so our test can check it.


    def create_user(self, payload, headers):
        response = requests.post(f"{BASE_URL}/users", json=payload, headers=headers)
        return response

    def get_users_with_token(self, token):
        # "token" is received from the test.

        headers = {
            "Authorization": f"Bearer {token}"
        }
        # We create the Authorization header.
        # f"Bearer {token}" puts the actual token after "Bearer".

        response = requests.get(
            f"{BASE_URL}/users",
            headers=headers
        )
        # Send the token in the request header.

        return response
        # Return the API response to the test.

    def get_access_token(self, token_url, client_id, client_secret):
        # Send client credentials to the OAuth 2.0 token endpoint.

        data = {
            "grantType": "client_credentials",
            "clientId": client_id,
            "clientSecret": client_secret
        }
        # OAuth 2.0 Client Credentials flow uses this grant type.

        response = requests.post(
            token_url,
            json=data,
            auth=(client_id, client_secret)
        )
        # Send client_id and client_secret to the authorization server.
        # The authorization server should return an access token.

        return response
        # Return the token response so the test can validate it.

    def test_get_invalid_user():

        api = User_API()
        # Create the API client object so we can call our GET method.

        response = api.get_users()
        # Call the existing GET API method.
        # NOTE: Our current method gets /users, so this test is not yet
        # testing an invalid user ID.

    def get_user(self, user_id):
    # This method gets ONE specific user using the user ID.

        response = requests.get(
        f"{BASE_URL}/users/{user_id}"
        )
        # Example: user_id = 1 → /users/1
        # Example: user_id = 99999 → /users/99999

        return response
        # Return the response so the test can validate it.