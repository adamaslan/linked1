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
        'scope': 'w_member_social r_liteprofile'
    }
    auth_url = f"{AUTH_URL}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    print(f"Authorize here: {auth_url}")
    auth_code = input("Enter the authorization code from the redirect URL (copy and paste after 'code='): ")
    print(f"Authorization code: {auth_code}")
    return auth_code

def get_access_token(auth_code):
    """Exchanges authorization code for an access token and saves it."""
    print("get_access_token() called")
    print(f"Authorization code received: {auth_code}")
    data = {
        'grant_type': 'authorization_code',
        'code': auth_code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    response = requests.post(TOKEN_URL, data=data)
    try:
        response.raise_for_status()
        token_data = response.json()
        print(f"Token data: {token_data}")
        with open(TOKEN_FILE, 'w') as f:
            f.write(token_data['access_token'])
        return token_data['access_token']
    except requests.exceptions.HTTPError as e:
        print(f"HTTPError: {e}")
        return None

def authenticate():
    """Full authentication flow to obtain and save access token."""
    print("Initiating LinkedIn authentication...")
    auth_code = get_auth_code()
    access_token = get_access_token(auth_code)
    print("Successfully authenticated. Access token stored in", TOKEN_FILE)
    print(f"Access token: {access_token}")
    # Add r_liteprofile scope to the access token
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get("https://api.linkedin.com/v2/me", headers=headers)
    try:
        response.raise_for_status()
        data = response.json()
        print(f"LinkedIn URN: {data['id']}")
    except requests.exceptions.HTTPError as e:
        print(f"Error retrieving LinkedIn URN: {e}")

if __name__ == '__main__':
    authenticate()
