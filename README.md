# FastAPI + OpenAI + Microsoft Graph API

This is a FastAPI application that integrates **OpenAI** for text generation and **Microsoft Graph API** for authentication and email/pptx/docx/pandas functionality. These APIs are specifically designed to power a Custom GPT that serves K-12 Physical Education, Health, and Driver's Education teachers in Elizabeth Public Schools (EPS), New Jersey.

## 🎯 Purpose
This API suite enables a specialized Custom GPT to assist educators by:
- Generating structured lesson plans aligned with New Jersey state standards
- Creating assessments following Bloom's Taxonomy
- Producing materials that align with Danielson's Framework for Teaching
- Managing and distributing educational content through Microsoft Office integration

---

## 🚀 Features
✅ **Authentication:** Uses **Microsoft Graph API** for secure user authentication  
✅ **OpenAI Integration:** Supports intelligent text generation with **GPT-4** for lesson planning and content creation  
✅ **Document Generation:** Creates **PowerPoint presentations, Word documents (including EPS Lesson Plan templates), and Excel files** dynamically  
✅ **Email Integration:** Facilitates direct sharing of educational materials through Microsoft Graph API  
✅ **FERPA Compliance:** Ensures secure handling of educational data  
✅ **REST API:** Built with **FastAPI** and deployed on **Render**

## 🎓 Key Capabilities
1. **Lesson Planning & Assessment Generation**
   - Creates structured lesson plans using EPS templates
   - Generates differentiated content for ELL, Special Education, 504, and Gifted students
   - Produces assessments aligned with state standards

2. **Document Management**
   - Automated creation of educational materials
   - Secure storage in OneDrive
   - Easy retrieval and sharing capabilities

3. **Educational Enhancement**
   - AI-powered activity suggestions
   - Differentiation strategy recommendations
   - Higher-order thinking questions based on Bloom's Taxonomy

---

## 📂 Project Structure
📦 project-root/ 
├── 📄 main.py # FastAPI application 
├── 📄 requirements.txt # Dependencies for pip install 
├── 📄 gunicorn.conf.py # Gunicorn configuration 
├── 📄 render.yaml # Render deployment configuration 
├── 📄 .env # Environment variables (DO NOT COMMIT) 
├── 📄 README.md # Documentation 
└── 📂 Other files...

---

## 🔧 Installation & Setup

### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO.git
cd YOUR_REPO

