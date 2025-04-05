import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN_FILE = 'linkedin_token.txt'

def get_access_token():
    with open(TOKEN_FILE, 'r') as f:
        return f.read().strip()

# def get_user_urn():
#     headers = {
#         'Authorization': f'Bearer {get_access_token()}',
#         'X-Restli-Protocol-Version': '2.0.0'
#     }
#     response = requests.get('https://api.linkedin.com/v2/me', headers=headers)
#     response.raise_for_status()
#     return response.json()['id']

def create_post(text):
    headers = {
        'Authorization': f'Bearer {get_access_token()}',
        'X-Restli-Protocol-Version': '2.0.0',
        'Content-Type': 'application/json'
    }
    
    payload = {
        "author": "zxy-posting",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": text
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }
    
    response = requests.post(
        'https://api.linkedin.com/v2/ugcPosts',
        headers=headers,
        json=payload
    )
    return response.json()

if __name__ == '__main__':
    post_text = "Sharing insights from our latest project! #ProfessionalGrowth"
    try:
        result = create_post(post_text)
        print("Post created successfully:", result)
    except Exception as e:
        print(f"Post failed: {str(e)}")