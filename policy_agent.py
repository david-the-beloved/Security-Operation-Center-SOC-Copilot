from agno.agent import Agent
from agno.models.google import Gemini
from agno.knowledge.pdf import PDFKnowledgeBase
from agno.vectordb.lancedb import LanceDb
from agno.embedder.sentence_transformer import SentenceTransformerEmbedder
import os
from dotenv import load_dotenv

load_dotenv()

# 1. THE FREE LOCAL EMBEDDER
# This converts words into math directly on your laptop CPU, saving API tokens.
local_embedder = SentenceTransformerEmbedder(model="all-MiniLM-L6-v2")

# 2. THE PDF KNOWLEDGE BASE
knowledge_base = PDFKnowledgeBase(
    path="corporate_policy.pdf",
    vector_db=LanceDb(
        table_name="pdf_policy",
        uri="./lancedb_store",
        embedder=local_embedder
    )
)

print("🧠 Shredding PDF and loading into local vector memory...")
knowledge_base.load(recreate=True)

# 3. THE RAG AGENT
policy_agent = Agent(
    model=Gemini(id="gemini-1.5-flash"),
    knowledge=knowledge_base,
    search_knowledge=True,  # Gives the Agent the ability to search the PDF
    system_prompt=(
        "You are a strict Security Policy Enforcer. "
        "When asked a question, you must use your `search_knowledge` tool to look up the rule in the PDF document. "
        "Quote the rule if necessary, but keep your answers professional."
    ),
    show_tool_calls=True,
    markdown=True
)

if __name__ == "__main__":
    print("\n TEST TRIGGERED: Employee spotted routing data to a personal Notion account...")
    policy_agent.print_response(
        "According to our policy document, what is the rule regarding personal Notion accounts?")
