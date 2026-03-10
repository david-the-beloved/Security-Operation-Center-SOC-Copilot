import os
from agno.agent import Agent
from agno.models.google import Gemini
from tools import check_domain_reputation 

phishing_agent = Agent(
    name = "Phishing Detection Agent",
    model = Gemini(id="gemini-2.0-flash"),
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
