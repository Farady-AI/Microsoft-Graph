from dotenv import load_dotenv
import os
import requests
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from pptx import Presentation
from docx import Document
import pandas as pd
from starlette.responses import FileResponse
import openai  # OpenAI API Integration

# Load environment variables
load_dotenv()

app = FastAPI()

# Microsoft Graph API credentials
CLIENT_ID = os.getenv("MSCLIENTID")
CLIENT_SECRET = os.getenv("MSCLIENTSECRET")
TENANT_ID = os.getenv("MSTENANTID")
REDIRECT_URI = os.getenv("REDIRECT_URI")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # OpenAI API Key

AUTH_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize"
TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
GRAPH_ME_URL = "https://graph.microsoft.com/v1.0/me"

user_tokens = {}  # Temporary token storage (Use a real database in production)

openai.api_key = OPENAI_API_KEY  # Set OpenAI API Key

@app.get("/auth/login")
def login():
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": "User.Read Mail.Send offline_access",
        "response_mode": "query"
    }
    auth_url = f"{AUTH_URL}?{'&'.join([f'{k}={v}' for k, v in params.items()])}"
    return RedirectResponse(auth_url)


@app.get("/auth/callback")
def auth_callback(code: str):
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "scope": "User.Read Mail.Send offline_access"
    }
    
    response = requests.post(TOKEN_URL, data=data)
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to get access token")
    
    tokens = response.json()
    
    # Get user's email from Microsoft Graph API
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    user_info = requests.get(GRAPH_ME_URL, headers=headers).json()
    
    user_email = user_info.get("mail") or user_info.get("userPrincipalName")
    
    if not user_email:
        raise HTTPException(status_code=400, detail="Unable to fetch user email")
    
    user_tokens[user_email] = tokens  # Store token
    
    return {"message": "Login successful", "user": user_email}


class EmailSchema(BaseModel):
    to: str
    subject: str
    prompt: str  # Instead of body, use a prompt for AI-generated content

@app.post("/send-email")
def send_email(email: EmailSchema, user_email: str):
    # Get stored token
    tokens = user_tokens.get(user_email)
    
    if not tokens:
        raise HTTPException(status_code=401, detail="User not authenticated")

    # Refresh token if expired
    if "expires_in" in tokens and tokens["expires_in"] < 60:
        tokens = refresh_access_token(tokens["refresh_token"])
        user_tokens[user_email] = tokens

    # Generate AI-powered email content using OpenAI
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


def generate_email_content(prompt: str) -> str:
    """Uses OpenAI's ChatGPT to generate email content from a given prompt."""
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI assistant that generates professional email content."},
            {"role": "user", "content": f"Generate a professional email based on this prompt: {prompt}"}
        ]
    )
    return response.choices[0].message.content.strip()


def refresh_access_token(refresh_token):
    """Refreshes the Microsoft Graph API access token."""
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "scope": "User.Read Mail.Send offline_access"
    }

    response = requests.post(TOKEN_URL, data=data)
    
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to refresh access token")
    
    return response.json()


# File generation endpoints remain unchanged...

