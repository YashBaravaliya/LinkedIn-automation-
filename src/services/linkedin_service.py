import requests
from datetime import datetime

class LinkedInService:
    def __init__(self, access_token):
        self.access_token = access_token
        self.api_url = "https://api.linkedin.com/v2/ugcPosts"
        
    def create_draft(self, text):
        draft_data = {
            "author": f"urn:li:person:4H457_TtZK",
            "lifecycleState": "DRAFT",
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
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

        print(headers)
        
        response = requests.post(self.api_url, headers=headers, json=draft_data)
        return response