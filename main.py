from fastapi import FastAPI, HTTPException
import logging
import os
import msal
import requests
from datetime import datetime, timedelta
from pydantic import BaseModel

# Load environment variables
CLIENT_ID = os.getenv("MSCLIENTID")
CLIENT_SECRET = os.getenv("MSCLIENTSECRET")
TENANT_ID = os.getenv("MSTENANTID")
REDIRECT_URI = os.getenv("REDIRECT_URI")  # Must match Azure settings

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/Mail.Send", "https://graph.microsoft.com/User.Read"]
  # Removed 'offline_access' to avoid ValueError

app = FastAPI()

user_tokens = {}  # Dictionary to store user tokens (Use a database in production)

@app.get("/auth/login")
def login():
    msal_app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
    auth_url = msal_app.get_authorization_request_url(SCOPE, redirect_uri=REDIRECT_URI)
    return {"auth_url": auth_url}

@app.get("/auth/callback")
def auth_callback(code: str):
    msal_app = msal.ConfidentialClientApplication(CLIENT_ID, CLIENT_SECRET, authority=AUTHORITY)
    
    # Exchange the auth code for a token
    result = msal_app.acquire_token_by_authorization_code(code, scopes=SCOPE, redirect_uri=REDIRECT_URI)

    if "access_token" not in result:
        raise HTTPException(status_code=400, detail=f"Authentication failed: {result.get('error_description')}")

    expiration_time = datetime.utcnow() + timedelta(seconds=result["expires_in"])
    result["expires_at"] = expiration_time.timestamp()

    # Get user's email
    headers = {"Authorization": f"Bearer {result['access_token']}"}
    user_info = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers).json()
    
    user_email = user_info.get("mail") or user_info.get("userPrincipalName")
    
    if not user_email:
        raise HTTPException(status_code=400, detail="Unable to fetch user email")

    # Store the tokens per user
    user_tokens[user_email] = result
    print(f"Stored Token for {user_email}: {result}")  # Debugging

    return {"message": "Login successful", "user": user_email}

class EmailSchema(BaseModel):
    to: str
    subject: str
    prompt: str

@app.post("/send-email")
def send_email(email: EmailSchema, user_email: str):
    tokens = user_tokens.get(user_email)
    
    if not tokens:
        raise HTTPException(status_code=401, detail=f"User {user_email} not authenticated. Please login first.")

    # Refresh token if expired
    if datetime.utcnow().timestamp() > tokens["expires_at"]:
        msal_app = msal.ConfidentialClientApplication(CLIENT_ID, CLIENT_SECRET, authority=AUTHORITY)
        refresh_result = msal_app.acquire_token_by_refresh_token(tokens["refresh_token"], scopes=SCOPE)

        if "access_token" not in refresh_result:
            raise HTTPException(status_code=401, detail="Token expired, and refresh failed. Please re-authenticate.")
        
        tokens = refresh_result
        tokens["expires_at"] = datetime.utcnow().timestamp() + tokens["expires_in"]
        user_tokens[user_email] = tokens

    # Generate email content using OpenAI
    ai_generated_body = generate_email_content(email.prompt)

    headers = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "Content-Type": "application/json"
    }

    email_data = {
        "message": {
            "subject": email.subject,
            "body": {"contentType": "Text", "content": ai_generated_body},
            "toRecipients": [{"emailAddress": {"address": email.to}}]
        }
    }

    graph_url = "https://graph.microsoft.com/v1.0/me/sendMail"
    response = requests.post(graph_url, headers=headers, json=email_data)

    if response.status_code == 202:
        return {"message": "Email sent successfully", "generated_content": ai_generated_body}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())
