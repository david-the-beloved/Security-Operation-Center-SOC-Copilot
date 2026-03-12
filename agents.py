import os
from agno.agent import Agent
from agno.models.google import Gemini
from tools import check_domain_reputation, check_vendor_ip
from pydantic import BaseModel, Field
from typing import List, Optional

class SecurityVerdict(BaseModel):
    verdict: str = Field(
        description="Must be one of: CLEAN, SUSPICIOUS, MALICIOUS")
    confidence_score: float = Field(description="Confidence from 0.0 to 1.0")
    detected_threats: List[str] = Field(
        description="List of malicious domains or IPs found")
    analyst_summary: str = Field(
        description="A brief technical explanation of the finding")

phishing_agent = Agent(
    name = "Phishing Detection Agent",
    model = Gemini(id="gemini-2.5-flash"),
    tools = [check_domain_reputation],
    instructions= [
        "You are an AI SOC Analyst. Your goal is to triage potential phishing emails.",
        "1. Parse the email body and subject for any URLs or domains.",
        "2. For every unique domain found, call 'check_domain_reputation'.",
        "3. Compare findings against the 'malicious_domains' database results.",
        "4. Provide a 'Final Verdict': MALICIOUS, SUSPICIOUS, or CLEAN.",
        "5. If MALICIOUS, list the specific indicators (IOCs) found."
    ],
    markdown=True
)

log_analyst_agent = Agent(
    name = "Log Analysis Agent",
    model=Gemini(id="gemini-2.5-flash"),
    tools=[check_vendor_ip],
    instructions=[
        "You are a Senior SOC Analyst.",
        "Analyze the provided server logs and extract all IP addresses.",
        "For each IP, use 'check_vendor_ip' to see if it belongs to an approved vendor.",
        "If an IP is NOT in the approved_vendors list and shows suspicious activity (e.g., failed logins), mark as MALICIOUS.",
        "Provide a high-confidence verdict based on the database results."
    ],
    markdown=True
)   