import os
import requests
import jwt
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID')
CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET')
REDIRECT_URI = os.getenv('LINKEDIN_REDIRECT_URI', 'http://localhost:8000/callback')
JWKS_URI = 'https://www.linkedin.com/oauth/openid/jwks'

SCOPES = ['openid', 'profile', 'email']

def get_authorization_url():
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': ' '.join(SCOPES),
        'state': os.urandom(16).hex()
    }
    return f"https://www.linkedin.com/oauth/v2/authorization?{'&'.join([f'{k}={v}' for k, v in params.items()])}"

def exchange_code(code):
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET
    }
    
    response = requests.post('https://www.linkedin.com/oauth/v2/accessToken', data=data)
    response.raise_for_status()
    return response.json()

def validate_id_token(id_token):
    jwks_client = jwt.PyJWKClient(JWKS_URI)
    signing_key = jwks_client.get_signing_key_from_jwt(id_token)
    
    return jwt.decode(
        id_token,
        key=signing_key.key,
        algorithms=["RS256"],
        audience=CLIENT_ID,
        issuer="https://www.linkedin.com"
    )

def get_user_info(access_token):
    headers = {'Authorization': f'Bearer {access_token}'}
    response = requests.get('https://api.linkedin.com/v2/userinfo', headers=headers)
    response.raise_for_status()
    return response.json()

def authenticate():
    auth_url = get_authorization_url()
    print(f"Authorize here: {auth_url}")
    code = input("Enter authorization code: ").strip()
    
    token_response = exchange_code(code)
    id_token = token_response['id_token']
    access_token = token_response['access_token']
    
    # Validate ID token
    claims = validate_id_token(id_token)
    print("\nID Token Claims:")
    print(f"User ID: {claims['sub']}")
    print(f"Name: {claims.get('name', 'N/A')}")
    print(f"Email: {claims.get('email', 'N/A')}")
    
    # Get additional user info
    user_info = get_user_info(access_token)
    print("\nUser Info from API:")
    print(f"Given Name: {user_info.get('given_name')}")
    print(f"Family Name: {user_info.get('family_name')}")
    print(f"Locale: {user_info.get('locale')}")
    print(f"Email Verified: {user_info.get('email_verified', False)}")
    
    return {
        'access_token': access_token,
        'id_token': id_token,
        'claims': claims,
        'user_info': user_info
    }

if __name__ == '__main__':
    authenticate()