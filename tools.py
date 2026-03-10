from database import SessionLocal, ApprovedVendor, MaliciousDomain


def check_domain_reputation(domain: str) -> str:
    """
    Checks the corporate database to see if a domain is known to be malicious.
    The AI Agent will use this tool when it extracts a link from an email.
    """

    print(f"Agent is checking domain {domain}...")
    db = SessionLocal()

    try:
        record = db.query(MaliciousDomain).filter(MaliciousDomain.domain == domain).first()

        if record:
            return f"Critical Match: The domain {domain} is a known {record.threat_level} threat"
        
        return f"SAFE: The domain '{domain}' does not appear in our threat intelligence database."
    finally:
        db.close()


def check_vendor_ip(ip_address: str) -> str:
    """
    Checks the corporate database to see if an IP belongs to an approved vendor.
    The AI Agent will use this tool to investigate weird network traffic.
    """

    print(f"Agent is checking IP adress: {ip_address}...")
    db = SessionLocal()

    try:
        record = db.query(ApprovedVendor).filter(ApprovedVendor.ip_address == ip_address).first()

        if record:
            return f"APPROVED: IP '{ip_address}' belongs to authorized vendor '{record.vendor_name}'."
        
        return f"VIOLATION: IP '{ip_address}' is NOT approved. This is unauthorized Shadow IT traffic."
    
    finally:
        db.close()