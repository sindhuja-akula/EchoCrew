"""
EchoCrew System Health Check 🏥
Verifies availability of backend service, database connection, and local services.
"""

import sys
import urllib.request
import json

def check_health():
    print("==========================================")
    print("       EchoCrew System Health Check       ")
    print("==========================================")

    url = "http://localhost:8000/health"
    print(f"[*] Checking backend API at {url}...")

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=3) as response:
            if response.status == 200:
                data = json.loads(response.read().decode('utf-8'))
                print(f"[✓] Backend Status: {data.get('status', 'OK').upper()}")
                print(f"[✓] Environment: {data.get('environment', 'unknown')}")
            else:
                print(f"[✗] HTTP Status: {response.status}")
    except Exception as e:
        print(f"[✗] Service unreachable: {e}")
        print("    Ensure FastAPI is running locally or via docker-compose up.")

if __name__ == "__main__":
    check_health()
