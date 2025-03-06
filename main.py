from dotenv import load_dotenv
import os
from FastAPI import HTTPException


import requests

print("DEBUG - ENV VARIABLES:")
import pandas as pandas
print("MSCLIENTID:", os.getenv("MSCLIENTID"))
print("MSCLIENTSECRET:", os.getenv("MSCLIENTSECRET"))
print("MSTENANTID:", os.getenv("MSTENANTID"))
from pptx import Presentation
from docx import Document

from starlette.responses import FileResponse

app = load_dotenv()

# Microsoft Graph API credentials
CLIENT_ID = os.getenv("MSCLIENTID")
CLIENT_SECRET = os.getenv("MSCLIENTSECRET")
TENANT_ID = os.getenv("MSTENANTID")
ACCESS_TOKEN = None  # This should be obtained via OAuth flow


def get_access_token():
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials",
        "scope": "https://graph.microsoft.com/.default"
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        return response.json().get("access_token")
    raise HTTPException(status_code=400, detail="Failed to obtain access token")


def create_ppt(content: list, file_name: str = "generated_presentation.pptx"):
    prs = Presentation()
    for slide_content in content:
        slide_layout = prs.slide_layouts[5]
        slide = prs.slides.add_slide(slide_layout)
        if slide.shapes.title:
            slide.shapes.title.text = slide_content.get("title", "Untitled")
        if len(slide.placeholders) > 1:
            slide.placeholders[1].text = slide_content.get("body", "")
    prs.save(file_name)
    return file_name


def create_doc(content: list, file_name: str = "generated_document.docx"):
    doc = Document()
    for section in content:
        doc.add_heading(section.get("title", "Untitled"), level=1)
        doc.add_paragraph(section.get("body", ""))
    doc.save(file_name)
    return file_name


def create_excel(content: list, file_name: str = "generated_spreadsheet.xlsx"):
    df = pd.DataFrame(content)
    df.to_excel(file_name, index=False)
    return file_name


@app.post("/generate-file")
async def generate_file(request: Request):
    global ACCESS_TOKEN
    data = await request.json()
    file_type = data.get("file_type", "ppt")
    content = data.get("content", [])
    
    if file_type == "ppt":
        file_name = create_ppt(content)
    elif file_type == "doc":
        file_name = create_doc(content)
    elif file_type == "excel":
        file_name = create_excel(content)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    if ACCESS_TOKEN is None:
        ACCESS_TOKEN = get_access_token()
    
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/octet-stream"
    }
    
    with open(file_name, "rb") as file:
        upload_url = f"https://graph.microsoft.com/v1.0/me/drive/root:/{file_name}:/content"
        response = requests.put(upload_url, headers=headers, data=file)
        
        if response.status_code in [200, 201]:
            return {"message": "File uploaded successfully", "file_url": response.json().get("webUrl", "")}
        else:
            raise HTTPException(status_code=400, detail=f"Failed to upload file: {response.text}")


@app.get("/download-file")
async def download_file(file_type: str = "ppt"):
    file_map = {
        "ppt": "generated_presentation.pptx",
        "doc": "generated_document.docx",
        "excel": "generated_spreadsheet.xlsx"
    }
    file_name = file_map.get(file_type, "generated_presentation.pptx")
    if not os.path.exists(file_name):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_name, media_type="application/octet-stream", filename=file_name)
