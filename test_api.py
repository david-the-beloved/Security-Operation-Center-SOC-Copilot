import requests
import io

# The base URL of your local FastAPI server
BASE_URL = "http://localhost:8000/api/v1"


def test_phishing_endpoint():
    print("--- Testing Pipeline A: Phishing Triage ---")

    # 1. Create a mock email payload containing a suspicious link
    email_payload = {
        "sender": "admin@paypa1-security-update.com",
        "subject": "URGENT: Your account has been suspended",
        "body": "Dear user, please click here to verify your identity: http://malicious-login-portal.com/login. If you do not verify within 24 hours, your account will be deleted."
    }

    try:
        # Send the JSON payload to the analyze-email endpoint
        response = requests.post(
            f"{BASE_URL}/analyze-email", json=email_payload)
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)

        print("Status Code:", response.status_code)
        print("Response JSON:")
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Pipeline A Test Failed: {e}")


def test_log_analysis_endpoint():
    print("\n--- Testing Pipeline B: Log Analysis ---")

    # 1. Create a mock CSV string simulating server access logs
    mock_csv_data = """timestamp,ip_address,action,status
2026-03-10T14:00:00Z,192.168.1.50,login,success
2026-03-10T14:05:00Z,203.0.113.42,database_query,success
2026-03-10T14:10:00Z,198.51.100.99,login,failed
2026-03-10T14:11:00Z,198.51.100.99,login,failed
2026-03-10T14:12:00Z,198.51.100.99,login,failed
"""

    # 2. Convert the string into a file-like object so requests can upload it
    file_tuple = {
        "file": ("mock_logs.csv", io.StringIO(mock_csv_data), "text/csv")}

    try:
        # Send the file to the analyze-logs endpoint
        response = requests.post(f"{BASE_URL}/analyze-logs", files=file_tuple)
        response.raise_for_status()

        print("Status Code:", response.status_code)
        print("Response JSON:")
        print(response.json())
    except requests.exceptions.RequestException as e:
        print(f"Pipeline B Test Failed: {e}")


if __name__ == "__main__":
    print("Starting SOC Copilot API Tests...\n")
    test_phishing_endpoint()
    test_log_analysis_endpoint()
    print("\nTests completed.")
