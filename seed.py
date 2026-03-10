from database import SessionLocal, MaliciousDomain, ApprovedVendor
import random

def seed_database():
    db = SessionLocal()
    print("🌱 Initiating massive database seed sequence...")
    
    try:
        # ==========================================
        # 1. Generate 50 Malicious Domains
        # ==========================================
        if not db.query(MaliciousDomain).first():
            print("Injecting 50 malicious domains...")
            
            prefixes = ["update", "secure", "auth", "login", "verify", "portal", "invoice", "billing", "hr", "payroll"]
            cores = ["-microsoft", "-google", "-okta", "-workday", "-salesforce", "-covenant", "-bank", "-internal", "-sso", "-vpn"]
            suffixes = [".com", ".net", ".info", ".biz", ".co", ".xyz", ".online", ".tech", ".support", ".security"]
            
            bad_guys = []
            seen_domains = set()

            while len(bad_guys) < 50:
                domain = f"{random.choice(prefixes)}{random.choice(cores)}{random.choice(suffixes)}"

                if domain not in seen_domains:
                    seen_domains.add(domain)
                    threat_level = random.choice(["Low", "Medium", "High", "Critical"])
                    bad_guys.append(MaliciousDomain(domain=domain, threat_level=threat_level))
            
            db.add_all(bad_guys)



        # ==========================================
        # 2. Generate 50 Approved Vendors (Shadow IT)
        # ==========================================
        if not db.query(ApprovedVendor).first():
            print("Injecting 50 approved enterprise vendors and IP addresses...")
            
            vendors = [
                "Microsoft Office 365", "Google Workspace", "AWS US-East", 
                "Salesforce CRM", "Workday HR", "Cloudflare CDN", 
                "GitHub Enterprise", "Slack Technologies", "Zoom Video", "Datadog"
            ]
            
            good_guys = []
            seen_ips = set()

            while len(good_guys) < 50:
                ip_address = f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"

                if ip_address not in seen_ips:
                    seen_ips.add(ip_address)
                    vendor_name = random.choice(vendors)
                    good_guys.append(ApprovedVendor(ip_address=ip_address, vendor_name=vendor_name))
            
            db.add_all(good_guys)

        # Save to Supabase
        db.commit()
        print(" Success: 100 unique mock records injected! The database is primed and ready for the AI.")
        
    except Exception as e:
        db.rollback()
        print(f" Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()