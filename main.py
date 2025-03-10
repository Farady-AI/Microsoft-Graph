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
from fastapi.middleware.cors import CORSMiddleware
from pptx.util import Inches

# Setup logging
logging.basicConfig(level=logging.INFO)

# Define simplified request model
class DocumentRequest(BaseModel):
    document_type: str
    title: str
    content: str
    output_format: str = "docx"  # "docx" or "pptx"

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

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/generate-text")
async def generate_text(request: TextRequest):
    """
    Enhanced endpoint that handles both free-form text generation and structured document content.
    When structured_output is True, expects a DocumentRequest object with specific formatting instructions.
    """
    try:
        logging.info(f"Received request: {request}")
        
        # If this is a structured document request, add specific system instructions
        if request.structured_output and request.document_request:
            system_prompt = f"""You are an AI assistant specialized in generating educational content for K-12 PE, Health, and Driver's Ed.
            You are generating content for a {request.document_request.document_type}.
            Format the output according to the provided structure and maintain professional educational standards."""
            
            # Convert the document request to a format suitable for GPT
            formatted_prompt = f"""
            Title: {request.document_request.title}
            Document Type: {request.document_request.document_type}
            
            Please provide content for each section while maintaining educational best practices and standards.
            
            Original prompt: {request.prompt}
            """
        else:
            system_prompt = "You are an AI assistant that generates text based on prompts."
            formatted_prompt = request.prompt

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": formatted_prompt}
            ]
        )
        
        generated_content = response["choices"][0]["message"]["content"].strip()
        
        # If this is a structured request, process the content for document generation
        if request.structured_output and request.document_request:
            # Process the generated content based on document type
            if request.document_request.output_format == "docx":
                doc = Document()
                doc.add_heading(request.document_request.title, 0)
                
                # Add content sections
                for section in request.document_request.sections:
                    doc.add_heading(section.section_type, level=1)
                    doc.add_paragraph(section.content)
                    
                # Save with metadata
                filename = f"{request.document_request.document_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
                doc.save(filename)
                
                return FileResponse(filename)
            
            # Add similar handling for pptx and xlsx formats
            
        logging.info("Content generation successful")
        return {"generated_text": generated_content}
        
    except Exception as e:
        logging.error(f"Error in generate-text: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/test")
async def test_endpoint():
    """Simple endpoint to verify API is accessible"""
    return {"status": "ok", "message": "API is running and accessible"}

@app.post("/generate-document")
async def generate_document(request: DocumentRequest):
    """
    Simplified document generation endpoint.
    Accepts content and generates a document in the requested format.
    """
    try:
        logging.info(f"Generating {request.output_format} document: {request.title}")
        
        if request.output_format == "docx":
            doc = Document()
            doc.add_heading(request.title, 0)
            doc.add_paragraph(request.content)
            
            filename = f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx"
            doc.save(filename)
            return FileResponse(filename)
            
        elif request.output_format == "pptx":
            prs = Presentation()
            slide = prs.slides.add_slide(prs.slide_layouts[5])
            title = slide.shapes.title
            title.text = request.title
            
            # Add content to the slide
            left = top = width = height = Inches(1)
            txBox = slide.shapes.add_textbox(left, top, width, height)
            tf = txBox.text_frame
            tf.text = request.content
            
            filename = f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pptx"
            prs.save(filename)
            return FileResponse(filename)
            
        else:
            raise HTTPException(status_code=400, detail=f"Unsupported format: {request.output_format}")
            
    except Exception as e:
        logging.error(f"Error generating document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

