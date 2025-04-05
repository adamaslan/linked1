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
        return f.read().strip()

def create_linkedin_post(post_text, author_urn='urn:li:person:YOUR_MEMBER_ID'):
    """Creates a LinkedIn post with the specified text."""
    access_token = load_access_token()
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'X-Restli-Protocol-Version': '2.0.0'
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
    
    response = requests.post(POST_URL, headers=headers, json=post_payload)
    response.raise_for_status()
    return response.json()

if __name__ == '__main__':
    # Example usage (Uncomment sections as needed):
    
    # 1. Run authentication flow (once)
    authenticate()
    
    # 2. Create a post
    post_content = "Hello LinkedIn! Sharing insights via API integration. #developer"
    try:
        post_result = create_linkedin_post(post_content)
        print("Post successfully created:", post_result)
    except Exception as e:
        print(f"Error creating post: {str(e)}")
