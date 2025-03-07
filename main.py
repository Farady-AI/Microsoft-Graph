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
    tokens = "1.AXEByo0nth8bLEmq3gBAi-l0C_DVzFqiu01Ntjh7VYdSUhZxAbNxAQ.AgABBAIAAABVrSpeuWamRam2jAF1XRQEAwDs_wUA9P-TQKwg3MrkeFoEBo6_kx-X8zpMRgPhFAe-OnDm5y1fjLNPxB8urp8U8t5R7cPQJbHIVqIJrn6tS1CUJfqJyB5BQyqze4S54gGnxz6i_3JJRPJfvWaTq7hS_lC5e8xzljxsBjziiuwN4bAficV7jGm2QsniC1xZsv6RY9S2DTOUKkxzABlLvXM3ZiXOvUM5i4KDycN2Ggjw-EMqLUfB1dhutq_7RId0xkA3JvlBXkpyt_sLWhxcBJx8mS3v4LXXGiGYiBJPhW8YpaSqbX2aFrjREHN4DiN8zIrcJmq7kWoKa37oz2_43mpBDo-697QI9guoIZ9oxnrnM4nnPfODH3iIO1T5XmSkA_iOUa2xWpLQ4hEIzI7Y6UK2BSKb7AjOAr6yjRwjLBVkk1zi3pX8so2TXA7eWe1J99mPR1IjY52YtySoz98SuuknoUasH0yGlkIcmz376PSF8a8IkNNJ5UreTPpPAKcSXos_5UlCUlSPNaEtbHXqrLuGQ7pIIpUf-BZboFvhwVWjxiALpWLy4s-iZM7FGLrpagCivQQdOHQfcJQ1JK_RMtCmNq0TwlvkPXk573bnHbXZTlFVxVdgnvF7wv9J2F4ZW6whYbWk5Jm_WqXxg4SUIzPn_Ci-IXGcCKzOF9Rduek-xqeSZIqux6_VcugraiifwMr1xaxUJOuIh7PansFAB7LRhtyLNC9UZIakwdBAvnRWtsbQN3G_ygdy7lqt4N4g3pl2qpv4XL0K0xMOXinN5DTm080kt3SA_5QgPP3MOkG8V93HS8iraFRrtC9STjhQ0cJ1Jw0SV_THuEeJKnQwxECDD6To_seh3oeudnyQ7694606rBdoMYXK51-_uavFiVPpO_wnYpCHfmXrdNO2St5GZEvnVui2xExeINpzj-RqCxrV1xZzjWN3dOpXXY-laxQPdlIuj_a9Squ7R2tWlUp4ti0-pUGNVfpzSYdPVrhLy73a8fMzA3G0CpRAqcBjrPf3Gr-nYk7kMvJptORQNuB2CKxstza-KOv7tz2uto9TQgvxPEsmRjz5RWa1JkHFgN4U2qVNu57z_FU_KDpX4fHlas3TpHG9Y-DskLRqK05D0d5zqQs7fgFuoRCn2tqYC13tgDV9Z2EVcr9h2fZHomQfuLGGStg_Aa4TVFtWWbI3M8Qyz7IOmRWAliyWWcH8q3-mD8bqNnIi__FtoQHy2zHv43hZpunVZKeQ93dzKviR8ZAnpXMo1OHuU2nuQNSjDT1DbRE6gsRMGUCx704mTQnqnyJWMPgw5sqYQaemZvgmQeStJJQaRop-Tj63tpzEccUeH-yEvl2B2EfrWKVqoi7BoKLYU9AC9lfpxRfGEUHy_oAkcfwfS8fHM6ZnKytrLG6ZptaceTB6yvSytwh9Cf4w5GZzKxaWTg1LKnTVe2Rvkk9EZJss"
    
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
    tokens = "1.AXEByo0nth8bLEmq3gBAi-l0C_DVzFqiu01Ntjh7VYdSUhZxAbNxAQ.AgABBAIAAABVrSpeuWamRam2jAF1XRQEAwDs_wUA9P-TQKwg3MrkeFoEBo6_kx-X8zpMRgPhFAe-OnDm5y1fjLNPxB8urp8U8t5R7cPQJbHIVqIJrn6tS1CUJfqJyB5BQyqze4S54gGnxz6i_3JJRPJfvWaTq7hS_lC5e8xzljxsBjziiuwN4bAficV7jGm2QsniC1xZsv6RY9S2DTOUKkxzABlLvXM3ZiXOvUM5i4KDycN2Ggjw-EMqLUfB1dhutq_7RId0xkA3JvlBXkpyt_sLWhxcBJx8mS3v4LXXGiGYiBJPhW8YpaSqbX2aFrjREHN4DiN8zIrcJmq7kWoKa37oz2_43mpBDo-697QI9guoIZ9oxnrnM4nnPfODH3iIO1T5XmSkA_iOUa2xWpLQ4hEIzI7Y6UK2BSKb7AjOAr6yjRwjLBVkk1zi3pX8so2TXA7eWe1J99mPR1IjY52YtySoz98SuuknoUasH0yGlkIcmz376PSF8a8IkNNJ5UreTPpPAKcSXos_5UlCUlSPNaEtbHXqrLuGQ7pIIpUf-BZboFvhwVWjxiALpWLy4s-iZM7FGLrpagCivQQdOHQfcJQ1JK_RMtCmNq0TwlvkPXk573bnHbXZTlFVxVdgnvF7wv9J2F4ZW6whYbWk5Jm_WqXxg4SUIzPn_Ci-IXGcCKzOF9Rduek-xqeSZIqux6_VcugraiifwMr1xaxUJOuIh7PansFAB7LRhtyLNC9UZIakwdBAvnRWtsbQN3G_ygdy7lqt4N4g3pl2qpv4XL0K0xMOXinN5DTm080kt3SA_5QgPP3MOkG8V93HS8iraFRrtC9STjhQ0cJ1Jw0SV_THuEeJKnQwxECDD6To_seh3oeudnyQ7694606rBdoMYXK51-_uavFiVPpO_wnYpCHfmXrdNO2St5GZEvnVui2xExeINpzj-RqCxrV1xZzjWN3dOpXXY-laxQPdlIuj_a9Squ7R2tWlUp4ti0-pUGNVfpzSYdPVrhLy73a8fMzA3G0CpRAqcBjrPf3Gr-nYk7kMvJptORQNuB2CKxstza-KOv7tz2uto9TQgvxPEsmRjz5RWa1JkHFgN4U2qVNu57z_FU_KDpX4fHlas3TpHG9Y-DskLRqK05D0d5zqQs7fgFuoRCn2tqYC13tgDV9Z2EVcr9h2fZHomQfuLGGStg_Aa4TVFtWWbI3M8Qyz7IOmRWAliyWWcH8q3-mD8bqNnIi__FtoQHy2zHv43hZpunVZKeQ93dzKviR8ZAnpXMo1OHuU2nuQNSjDT1DbRE6gsRMGUCx704mTQnqnyJWMPgw5sqYQaemZvgmQeStJJQaRop-Tj63tpzEccUeH-yEvl2B2EfrWKVqoi7BoKLYU9AC9lfpxRfGEUHy_oAkcfwfS8fHM6ZnKytrLG6ZptaceTB6yvSytwh9Cf4w5GZzKxaWTg1LKnTVe2Rvkk9EZJss"


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
