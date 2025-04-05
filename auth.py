import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Configuration
CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID')
CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET')
REDIRECT_URI = "https://www.linkedin.com/developers/tools/oauth/redirect"
TOKEN_FILE = 'linkedin_token.txt'

# LinkedIn API endpoints
AUTH_URL = 'https://www.linkedin.com/oauth/v2/authorization'
TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'

def get_auth_code():
    """Generates authorization URL and retrieves the auth code from the user."""
    print("get_auth_code() called")
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': 'w_member_social'
    }
    auth_url = f"{AUTH_URL}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    print(f"Authorize here: {auth_url}")
    auth_code = input("Enter the authorization code from the redirect URL: ")
    print(f"Authorization code: {auth_code}")
    return auth_code

def get_access_token(auth_code):
    """Exchanges authorization code for an access token and saves it."""
    print("get_access_token() called")
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, data=data)
    response.raise_for_status()
    token_data = response.json()
    print(f"Token data: {token_data}")
    with open(TOKEN_FILE, 'w') as f:
        f.write(token_data['access_token'])
    return token_data['access_token']

if __name__ == '__main__':
    get_auth_code()
