from dotenv import load_dotenv
import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from dotenv import load_dotenv


load_dotenv()
app = FastAPI()

@app.put("/items/{item_id}")
def read_item(item_id: int):
    if item_id < 0:
        raise HTTPException(status_code=400, detail="Item ID must be positive")
    return {"item_id": item_id}



import requests

print("DEBUG - ENV VARIABLES:")
import pandas as pandas
print("MSCLIENTID:", os.getenv("MSCLIENTID"))
print("MSCLIENTSECRET:", os.getenv("MSCLIENTSECRET"))
print("MSTENANTID:", os.getenv("MSTENANTID"))
from pptx import Presentation
from docx import Document

from starlette.responses import FileResponse



# Microsoft Graph API credentials
CLIENT_ID = os.getenv("MSCLIENTID")
CLIENT_SECRET = os.getenv("MSCLIENTSECRET")
TENANT_ID = os.getenv("MSTENANTID")
REDIRECT_URI = os.getenv("REDIRECT_URI")

AUTH_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/authorize"
TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
GRAPH_ME_URL = "https://graph.microsoft.com/v1.0/me"

# Temporary token storage (Use a real database in production)
user_tokens = {}

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
    
    #tokens = response.json()
    tokens = "1.AXEByo0nth8bLEmq3gBAi-l0C_DVzFqiu01Ntjh7VYdSUhZxAbNxAQ.AgABBAIAAABVrSpeuWamRam2jAF1XRQEAwDs_wUA9P_l9eAZbClWNdx2_NBP6i2NPkraihxeiqpkfxaHHuua9R3WfEKrqForlND-hSLfanmHvleFuSfpjJJnx9ZgXdfLWXWdeADh6HPRO7SR6wpVZxzsc0w8IrtGQGytswCS2Lv6ZHtwWlAMkkDyHQysmgGd1AzErP8KM1aGNBZg0ZhPeHPLryl-hrSAg8_onx6IyXmQ8Lmi49iK92B6qCAcQfqeB-KIeIxC6ToC6ikqoQfxfr47HSm4QdJ8dtWyt5Bwg_pXIhQ2QeMTrmkxqs0RAF1jLxHmOsHyHEKMqWf9Dqr3gu35VCrUKMRcVRay3uX6AATbhhbsz7DTMVvunlXGdZOrZDG1kpu-R6u1Qu-o8VSwtZJ0G_4ocLg2qfQgrHSKLr4bHleoLpnMWIW3vKOQBbF4QAEiWeKqjpfsnN6B2U1_VG0NxgWL-_mgtOuX70HaVrm_zfrAQTOv1UPa5n9dZP4S1YaH5zjD-rawsn61nl6vbp1PI7L-bd3sR_8KJPSb0Ae-ZGeKa-MhhXwr4pK3AAMtOW3-Cnu73aoYLlz_rNfh-_V0ZDPWLUTkdM4nZFpaUjRVaZLixg1JcwRL8Hen5ouFaqHYtk3n8xQFKCjfA3Fg002dVxCfspUkbgz_4tF--I_ji5PP8bZjWE2qi6StmkZB89WcH8DhY04Qx1KG5lz-mToNYiZ8QdDDfoWSXdO2ynEusa0G1glFEHv7SYpptDAemWqH8PEChdfme3ICnDNycx1OLQgiRi2AUw9p79UchmuJ62LHmOUuTX2aHrDIgTXhADm1igHzb853lpc6sQCgDAnjSMIY6DZqnX7lcRBI65gsqWJMpzeCx9NGV6tMb5fH-zTmfMOl9t3ro4-ctmfgpQTMN5x-WtzqmdWNvtZWFvhtsFXLMfE3xCQvwbprPsz_cYXt8tAbJ1tJIVl7bZOns25kFx4d9y2MVhecCOPCsyQ62RHwK6cho7AgJ8nvzCa06iVWYC1uKtMNiXpMva9wat4CBclHKoSFTCVp_Hmjjmyl0wVnr073tUJ8OmC37jbkxwICnILcbPnX-YlEq0h2W_ITCKVPQn7yjdkJHWw2wRrZ-t48bZ6C1zNGRR3gmi0CZvr3dJl4IKB9PrXBcKE-eX7RuAhjyFrpWmTPTISTEmMHCfwzZjZAhQayDC8Cp8ofJjkQ_I9E8Q2dJDIXSi57bc1eCUwqlF7eTuaFiOaXUVA3JP9BVh9opF9mblurl-NfITc4KcUKrEXlIPGjwSDbOJ7820mHWQhPu0UQ_c_QKMMxxEIztXyVn1H86etZoXGQRdYaUH-nKV3zW1ydFxAJS9xSLXcp12ntp6II2WnlWDFPQpvj9PSbnh4PRP1Zldfle-rTUPPgdX1PaHzbuJp15K5Mid_eRCzwSINjCrUV0ZWkMrIL8X0fp5obyQ"
    
    # Get user's email from Microsoft Graph API
    headers = {"Authorization": f"Bearer {tokens['access_token']}"}
    user_info = requests.get(GRAPH_ME_URL, headers=headers).json()
    
    user_email = user_info.get("mail") or user_info.get("userPrincipalName")
    
    if not user_email:
        raise HTTPException(status_code=400, detail="Unable to fetch user email")
    
    # Store token (Replace with a real database in production)
    user_tokens[user_email] = tokens
    
    return {"message": "Login successful", "user": user_email}

class EmailSchema(BaseModel):
    to: str
    subject: str
    body: str

@app.post("/send-email")
def send_email(email: EmailSchema, user_email: str):
    # Get stored token
    #tokens = user_tokens.get(user_email)
    tokens = "1.AXEByo0nth8bLEmq3gBAi-l0C_DVzFqiu01Ntjh7VYdSUhZxAbNxAQ.AgABBAIAAABVrSpeuWamRam2jAF1XRQEAwDs_wUA9P_l9eAZbClWNdx2_NBP6i2NPkraihxeiqpkfxaHHuua9R3WfEKrqForlND-hSLfanmHvleFuSfpjJJnx9ZgXdfLWXWdeADh6HPRO7SR6wpVZxzsc0w8IrtGQGytswCS2Lv6ZHtwWlAMkkDyHQysmgGd1AzErP8KM1aGNBZg0ZhPeHPLryl-hrSAg8_onx6IyXmQ8Lmi49iK92B6qCAcQfqeB-KIeIxC6ToC6ikqoQfxfr47HSm4QdJ8dtWyt5Bwg_pXIhQ2QeMTrmkxqs0RAF1jLxHmOsHyHEKMqWf9Dqr3gu35VCrUKMRcVRay3uX6AATbhhbsz7DTMVvunlXGdZOrZDG1kpu-R6u1Qu-o8VSwtZJ0G_4ocLg2qfQgrHSKLr4bHleoLpnMWIW3vKOQBbF4QAEiWeKqjpfsnN6B2U1_VG0NxgWL-_mgtOuX70HaVrm_zfrAQTOv1UPa5n9dZP4S1YaH5zjD-rawsn61nl6vbp1PI7L-bd3sR_8KJPSb0Ae-ZGeKa-MhhXwr4pK3AAMtOW3-Cnu73aoYLlz_rNfh-_V0ZDPWLUTkdM4nZFpaUjRVaZLixg1JcwRL8Hen5ouFaqHYtk3n8xQFKCjfA3Fg002dVxCfspUkbgz_4tF--I_ji5PP8bZjWE2qi6StmkZB89WcH8DhY04Qx1KG5lz-mToNYiZ8QdDDfoWSXdO2ynEusa0G1glFEHv7SYpptDAemWqH8PEChdfme3ICnDNycx1OLQgiRi2AUw9p79UchmuJ62LHmOUuTX2aHrDIgTXhADm1igHzb853lpc6sQCgDAnjSMIY6DZqnX7lcRBI65gsqWJMpzeCx9NGV6tMb5fH-zTmfMOl9t3ro4-ctmfgpQTMN5x-WtzqmdWNvtZWFvhtsFXLMfE3xCQvwbprPsz_cYXt8tAbJ1tJIVl7bZOns25kFx4d9y2MVhecCOPCsyQ62RHwK6cho7AgJ8nvzCa06iVWYC1uKtMNiXpMva9wat4CBclHKoSFTCVp_Hmjjmyl0wVnr073tUJ8OmC37jbkxwICnILcbPnX-YlEq0h2W_ITCKVPQn7yjdkJHWw2wRrZ-t48bZ6C1zNGRR3gmi0CZvr3dJl4IKB9PrXBcKE-eX7RuAhjyFrpWmTPTISTEmMHCfwzZjZAhQayDC8Cp8ofJjkQ_I9E8Q2dJDIXSi57bc1eCUwqlF7eTuaFiOaXUVA3JP9BVh9opF9mblurl-NfITc4KcUKrEXlIPGjwSDbOJ7820mHWQhPu0UQ_c_QKMMxxEIztXyVn1H86etZoXGQRdYaUH-nKV3zW1ydFxAJS9xSLXcp12ntp6II2WnlWDFPQpvj9PSbnh4PRP1Zldfle-rTUPPgdX1PaHzbuJp15K5Mid_eRCzwSINjCrUV0ZWkMrIL8X0fp5obyQ"
    
    if not tokens:
        raise HTTPException(status_code=401, detail="User not authenticated")

    # Refresh token if expired
    if "expires_in" in tokens and tokens["expires_in"] < 60:
        tokens = refresh_access_token(tokens["refresh_token"])
        user_tokens[user_email] = tokens

    headers = {
        "Authorization": f"Bearer {tokens['access_token']}",
        "Content-Type": "application/json"
    }

    email_data = {
        "message": {
            "subject": email.subject,
            "body": {"contentType": "Text", "content": email.body},
            "toRecipients": [{"emailAddress": {"address": email.to}}]
        }
    }

    graph_url = "https://graph.microsoft.com/v1.0/me/sendMail"
    response = requests.post(graph_url, headers=headers, json=email_data)

    if response.status_code == 202:
        return {"message": "Email sent successfully"}
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())

def refresh_access_token(refresh_token):
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



########


def send_email(access_token, recipient, subject, body):
    url = "https://graph.microsoft.com/v1.0/me/sendMail"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    email_data = {
        "message": {
            "subject": subject,
            "body": {
                "contentType": "Text",
                "content": body
            },
            "toRecipients": [
                {"emailAddress": {"address": recipient}}
            ]
        }
    }

    response = requests.post(url, headers=headers, json=email_data)

    if response.status_code == 202:
        return {"status": "Email sent successfully"}
    else:
        return {"error": response.json()}

@app.post("/send-email")
async def send_email_endpoint(request: Request):
    data = await request.json()
    
    email_address = data.get("to")
    subject = data.get("subject")
    body = data.get("body")
    access_token = get_access_token()

    if not email_address or not subject or not body:
        raise HTTPException(status_code=400, detail="Missing required fields")

    result = send_email(access_token, email_address, subject, body)
    
    return result
    
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
        token = response.json().get("access_token")
        if not token or "." not in token:  
            raise HTTPException(status_code=400, detail="Invalid token received from Microsoft")
        return token
    
    raise HTTPException(status_code=400, detail=f"Failed to obtain access token: {response.text}")


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
