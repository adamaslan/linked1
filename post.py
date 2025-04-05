import os
import requests
from dotenv import load_dotenv
from auth import authenticate

load_dotenv()

# Configuration
POST_URL = 'https://api.linkedin.com/v2/ugcPosts'
TOKEN_FILE = 'linkedin_token.txt'

# -------------------------- Posting Section --------------------------
def load_access_token():
    """Loads the stored access token from file."""
    if not os.path.exists(TOKEN_FILE):
        raise FileNotFoundError(
            "No access token found. Authenticate first using the authenticate() function."
        )
    with open(TOKEN_FILE, 'r') as f:
        access_token = f.read().strip()
        print(f"Access token loaded from file: {access_token}")
        return access_token

def create_linkedin_post(post_text, author_urn='urn:li:person:YOUR_MEMBER_ID'):
    """Creates a LinkedIn post with the specified text."""
    access_token = load_access_token()
    headers = {
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0',
        'Authorization': f'Bearer {access_token}'
    }
    
    post_payload = {
        "author": author_urn,
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": post_text
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    
    try:
        response = requests.post(POST_URL, headers=headers, json=post_payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        print(f"Error creating post: {e}")
        print(f"Response content: {response.content}")
        return None

if __name__ == '__main__':
    # Example usage (Uncomment sections as needed):
    
    # 2. Create a post
    post_content = "Hello LinkedIn! We are ZXY GALLERY"
    try:
        post_result = create_linkedin_post(post_content)
        print("Post successfully created:", post_result)
    except Exception as e:
        print(f"Error creating post: {str(e)}")
