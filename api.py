import os
import datetime
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import firebase_admin
from firebase_admin import credentials, firestore
from google import genai
import pandas as pd
from fastapi.responses import FileResponse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# 1. Initialize Firebase Admin SDK
# Ensure 'serviceAccountKey.json' is in the same directory
try:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
except Exception as e:
    print(f"Firebase Init Error: {e}")
    db = None

# 2. Initialize Gemini AI Client
# Set your GEMINI_API_KEY environment variable
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

app = FastAPI()

# 3. Enable CORS for SharePoint integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, restrict this to your SharePoint domain
    allow_methods=["*"],
    allow_headers=["*"],
)

class PRRequest(BaseModel):
    requestor: str
    area: str
    problem: str
    current_situation: str
    next_step: str

class RefineRequest(BaseModel):
    field_name: str
    content: str

@app.post("/refine-field")
async def refine_field(req: RefineRequest):
    prompt = f"""
    You are an Engineering Documentation Specialist. 
    Convert this rough note into a professional, structured engineering statement for the field: '{req.field_name}'.
    Rough Note: {req.content}
    
    Rules:
    - Keep it concise but technical.
    - If no specific ID is provided, use a placeholder like '[Equipment ID]'.
    - Output ONLY the refined text.
    """
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )
        return {"refined_text": response.text.strip()}
    except Exception as e:
        return {"refined_text": req.content} # Fallback to original on error

@app.post("/submit-pr")
async def submit_pr(pr: PRRequest):
    if not db:
        raise HTTPException(status_code=500, detail="Database connection failed")

    # 4. AI Evaluation Logic (High-Efficiency Engineering Rubric)
    prompt = f"""
    You are a Senior Equipment Engineering Manager. Grade this Purchase Requisition (PR) against strict standards.
    
    ### THE STANDARDS FOR APPROVAL:
    1. SPECIFICITY: Problem must mention Equipment IDs, error codes, or quantifiable frequency (e.g., '3x per week').
    2. TROUBLESHOOTING: Current situation must state what was already attempted or the specific impact (e.g., 'Risk of 4hrs downtime').
    3. ALIGNMENT: The 'Next Step' must be a direct technical solution to the 'Problem Statement'.
    4. NO FILLER: Reject one-word answers or vague 'need for work' justifications.

    ### USER DATA:
    - Requestor: {pr.requestor}
    - Area/Dept: {pr.area}
    - Problem Statement: {pr.problem}
    - Current Situation: {pr.current_situation}
    - Next Step: {pr.next_step}

    ### YOUR TASK:
    - If it fails ANY standard, status is "Rejected".
    - Provide a "feedback" summary.
    - List "coaching_tips" for how to reach the Gold Standard.

    RESPONSE FORMAT (JSON):
    {{
        "status": "Approved" or "Rejected",
        "feedback": "Concise summary.",
        "coaching_tips": ["Specific tip 1", "Specific tip 2"]
    }}
    """
    
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config={
                'response_mime_type': 'application/json',
            }
        )
        ai_decision = response.parsed
    except Exception as e:
        ai_decision = {
            "status": "Error", 
            "feedback": f"AI Error: {str(e)}",
            "coaching_tips": ["Check server logs", "Verify API Key"]
        }

    # 5. Log to Firebase Firestore
    pr_data = pr.model_dump()
    pr_data.update({
        "status": ai_decision.get("status"),
        "feedback": ai_decision.get("feedback"),
        "coaching_tips": ai_decision.get("coaching_tips"),
        "timestamp": datetime.datetime.utcnow()
    })
    
    db.collection("purchase_requisitions").add(pr_data)

    return ai_decision

@app.get("/export-report")
async def export_report():
    if not db:
        raise HTTPException(status_code=500, detail="Database connection failed")

    # 6. Fetch data from Firestore and Export to Excel
    docs = db.collection("purchase_requisitions").stream()
    data = [doc.to_dict() for doc in docs]
    
    if not data:
        return {"message": "No data found to export"}

    df = pd.DataFrame(data)
    report_file = "pr_report.xlsx"
    df.to_excel(report_file, index=False)

    return FileResponse(report_file, filename=report_file)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
