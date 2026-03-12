from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from agents import phishing_agent, log_analyst_agent
import pandas as pd
import io


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
def analyze_phishing_email(request: phishingEmail):
    """
    Ingest forwarded mail and triggers the agno multi agent triage team
    """
    try:
        # 1. Format the data for the agent
        prompt = f"Sender: {request.sender}\nSubject: {request.subject}\nBody: {request.body}"

        # 2. Trigger the agent (Synchronous call, so we dropped the 'async' from the def)
        response = phishing_agent.run(prompt)

        return {
            "status": "success",
            "message": "Email analyzed by SOC Copilot.",
            "data_received": {
                "sender": request.sender,
                "subject": request.subject
            },
            # 3. Return the actual AI verdict
            "verdict": response.content
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Phishing Agent failed: {str(e)}")


@app.post("/api/v1/analyze-logs")
async def analyze_logs(file: UploadFile = File(...)):
    """
    Ingest a massive CSV of network logs, crunches it with pandas and triggers the agno multi agent for anomalies
    """
    if not file.filename or not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=400, detail="Only CSV files are accepted.")

    try:
        # 1. Read the uploaded file bytes
        contents = await file.read()
        decoded_string = contents.decode('utf-8')

        # 2. Crunch with pandas (as promised in your docstring!)
        # We read the string into a DataFrame
        df = pd.read_csv(io.StringIO(decoded_string))

        # Convert the DataFrame into a Markdown table. LLMs *love* Markdown tables.
        log_data_for_llm = df.to_markdown(index=False)

        # 3. Trigger the log analysis agent
        response = log_analyst_agent.run(log_data_for_llm)

        return {
            "status": "success",
            "message": f"File '{file.filename}' crunched by pandas and analyzed by agents.",
            "verdict": response.content
        }

    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400, detail="Could not decode file. Ensure it is a valid UTF-8 CSV.")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Log Agent failed: {str(e)}")


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "SOC Copilot"
    }
