from fastapi import FastAPI,  UploadFile, File, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="Hybrid SOC Copilot API",
    description="Automated Security Operations Center for Phishing Triage and Shadow IT Hunting.",
    version="1.0.0"
)


class phishingEmail(BaseModel):
    sender: str
    subject: str
    body: str


@app.post("/api/v1/analyze-email")
async def analyze_phishing_email(request: phishingEmail):
    """
    Ingest forwarded mail and triggers the agno multi agent triage team
    """

    return {
        "status": "success",
        "message": "Email recieved by the SOC Copilot and is being analyzed.",
        "data recieved": {
            "sender": request.sender,
            "subject": request.subject,
            "body": request.body
        },
        "next_steps": "Agents booting up to anlayze text"

    }


@app.post("/api/v1/analyze-logs")
async def analyze_logs(file: UploadFile = File(...)):
    """
    Ingest a massive CSV of network logs, crunches it with pandas and triggers the agno multi agent for anomalies
    """

    if not file.filename or not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=400, detail="Only CSV files are accepted.")

    # Here you would add logic to process the CSV file and trigger the agents

    return {
        "status": "success",
        "message": f"File '{file.filename}' received and is being analyzed.",
        "next_steps": "pandas is warming up to crunch data"
    }

@app.get("/health")
async def health_check():

    return {
        "status": "healthy",
        "service": "SOC Copilot"
    }
