from fastapi import FastAPI, HTTPException
import logging
import os
import msal
import requests
from datetime import datetime, timedelta
from pydantic import BaseModel
from pptx import Presentation
from docx import Document
import pandas as pd
from starlette.responses import FileResponse
import uvicorn
import gunicorn
import openai
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO)

# Define request model for text generation
class TextRequest(BaseModel):
    prompt: str

# Load environment variables
load_dotenv()
CLIENT_ID = os.getenv("MSCLIENTID")
CLIENT_SECRET = os.getenv("MSCLIENTSECRET")
TENANT_ID = os.getenv("MSTENANTID")
REDIRECT_URI = os.getenv("REDIRECT_URI")  # Must match Azure settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # OpenAI API Key

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
SCOPE = ["https://graph.microsoft.com/Mail.Send", "https://graph.microsoft.com/User.Read"]

app = FastAPI()


user_tokens = {}  # Dictionary to store user tokens (Use a database in production)

openai.api_key = OPENAI_API_KEY  # Set OpenAI API Key

@app.get("/auth/login")
def login():
    msal_app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY)
    auth_url = msal_app.get_authorization_request_url(
        SCOPE,
        redirect_uri=REDIRECT_URI,
        with_account=None
    )
    return {"auth_url": auth_url}

@app.get("/auth/callback")
def auth_callback(code: str):
    logging.info("Auth callback triggered")
    msal_app = msal.ConfidentialClientApplication(CLIENT_ID, CLIENT_SECRET, authority=AUTHORITY)
    result = msal_app.acquire_token_by_authorization_code(
        code, 
        scopes=SCOPE,
        redirect_uri=REDIRECT_URI
    )
    if "access_token" not in result:
        logging.error("Authentication failed, no access token received.")
        raise HTTPException(status_code=400, detail=f"Authentication failed: {result.get('error_description')}")
    
    expiration_time = datetime.utcnow() + timedelta(seconds=result["expires_in"])
    result["expires_at"] = expiration_time.timestamp()
    headers = {"Authorization": f"Bearer {result['access_token']}"}
    user_info = requests.get("https://graph.microsoft.com/v1.0/me", headers=headers).json()
    user_email = user_info.get("mail") or user_info.get("userPrincipalName")
    if not user_email:
        logging.error("Unable to fetch user email")
        raise HTTPException(status_code=400, detail="Unable to fetch user email")
    user_tokens[user_email] = result
    logging.info(f"Stored Token for {user_email}: {result}")
    return {"message": "Login successful", "user": user_email}

@app.get("/generate-ppt")
def generate_ppt():
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    title = slide.shapes.title
    title.text = "Generated PowerPoint Slide"
    prs.save("generated_ppt.pptx")
    return FileResponse("generated_ppt.pptx")

@app.get("/generate-doc")
def generate_doc():
    doc = Document()
    doc.add_paragraph("Generated Word Document")
    doc.save("generated_doc.docx")
    return FileResponse("generated_doc.docx")

@app.get("/generate-excel")
def generate_excel():
    df = pd.DataFrame({"Column1": ["Data1", "Data2"], "Column2": ["MoreData1", "MoreData2"]})
    df.to_excel("generated_excel.xlsx", index=False)
    return FileResponse("generated_excel.xlsx")

class TextRequest(BaseModel):
    prompt: str

@app.post("/generate-text")
def generate_text(request: TextRequest):
    """Uses OpenAI's ChatGPT to generate text from a given prompt."""
    try:
        logging.info(f"Received request: {request.prompt}")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI assistant that generates text based on prompts."},
                {"role": "user", "content": request.prompt}
            ]
        )
        logging.info("OpenAI response successful")
        return {"generated_text": response["choices"][0]["message"]["content"].strip()}
    except Exception as e:
        logging.error(f"Error in generate-text: {str(e)}")
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

