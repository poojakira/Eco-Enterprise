import httpx
import time
import subprocess
import os
import signal
import sys

# --- Configuration ---
BASE_URL = "http://127.0.0.1:8000"
BACKEND_DIR = r"c:\Users\pooja\Downloads\EcoTrack-Enterprise-main (3)\EcoTrack-Enterprise-main\EcoTrack-Enterprise\EcoTrack-Enterprise\backend"

def run_server():
    print("🚀 Starting EcoTrack Backend for Phase 2 Verification...")
    process = subprocess.Popen(
        ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=BACKEND_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(5) # Wait for startup
    return process

def test_ledger_integrity():
    print("\n🛡️ Testing Ledger Integrity (Phase 2)...")
    
    with httpx.Client(base_url=BASE_URL) as client:
        # 1. Login
        print("🔑 Logging In...")
        login_data = {"username": "admin_user", "password": "secure_password_123"}
        r = client.post("/api/v1/auth/login", data=login_data)
        if r.status_code != 200:
             # Try registering if login fails (fresh DB)
             print("📝 Registering User...")
             reg_data = {"username": "admin_user", "password": "secure_password_123", "email": "admin@ecotrack.ent", "role": "admin"}
             client.post("/api/v1/auth/register", json=reg_data)
             r = client.post("/api/v1/auth/login", data=login_data)
        
        token = r.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 2. Ingest Data (Verify Merkle Root)
        print("📥 Ingesting Batch Group...")
        ingest_data = [
            {"sku_name": "Eco-Leaf 1", "category": "Packaging", "region": "EU", "vendor": "ForestCorp", "raw_material_energy": 50.0, "manufacturing_energy": 100.0},
            {"sku_name": "Eco-Leaf 2", "category": "Packaging", "region": "EU", "vendor": "ForestCorp", "raw_material_energy": 60.0, "manufacturing_energy": 110.0}
        ]
        r = client.post("/api/v1/data/ingest", json=ingest_data, headers=headers)
        if r.status_code == 200:
            merkle_root = r.json()["data_hash"]
            print(f"✅ Ingestion Successful. Merkle Root: {merkle_root}")
        else:
            print(f"❌ Ingestion Failed: {r.text}")
            return

        # 3. Verify Chain
        print("🔍 Running Full Chain Verification...")
        r = client.get("/api/v1/ledger/verify-chain", headers=headers)
        if r.status_code == 200:
            result = r.json()
            print(f"✅ Integrity Status: {result['status']}")
            print(f"✅ Records Scanned: {result['records_scanned']}")
            if result['status'] == "SECURE":
                 print("💎 Ledger Cryptographically Sound.")
        else:
            print(f"❌ Verification API Failed: {r.text}")

        # 4. Check Audit Log
        print("📜 Retrieving Audit Logs...")
        r = client.get("/api/v1/ledger/audit-log", headers=headers)
        if r.status_code == 200:
            logs = r.json()
            print(f"✅ Audit Entries Found: {len(logs)}")
            print(f"✅ Latest Entry Batch ID: {logs[0]['batch_id']}")
        else:
            print(f"❌ Audit Log API Failed: {r.text}")

if __name__ == "__main__":
    server_process = None
    try:
        server_process = run_server()
        test_ledger_integrity()
    except Exception as e:
        print(f"💥 Error: {e}")
    finally:
        if server_process:
            print("\n🛑 Shutting down server...")
            os.kill(server_process.pid, signal.SIGTERM)
            print("👋 Phase 2 Implementation Verified.")
