import os
from azure.identity import InteractiveBrowserCredential
from azure.keyvault.secrets import SecretClient
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

KV_URI = os.getenv("AZURE_KEYVAULT_URL")

if not KV_URI:
    raise ValueError("AZURE_KEYVAULT_URL environment variable is not set")

print("Authenticating with Azure")

credential = InteractiveBrowserCredential()
client = SecretClient(vault_url=KV_URI, credential=credential)

print("Fetching Supabase URL secretly from the key vault...")

supabase_secret = client.get_secret("SUPABASE-DB-URI")

DATABASE_URL = supabase_secret.value

if not DATABASE_URL:
    raise ValueError("SUPABASE-DB-URI secret is not set or empty")

# Supabase gives a 'postgresql://' or 'postgres://' URL. SQLAlchemy requires 'postgresql://'
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class MaliciousDomain(Base):
    __tablename__ = "malicious_domains"
    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String, unique=True, index=True)
    threat_level = Column(String)


class ApprovedVendor(Base):
    __tablename__ = "approved_vendors"
    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, unique=True, index=True)
    vendor_name = Column(String)


Base.metadata.create_all(bind=engine)
print("Database connection established and tables verified in Supabase!")
