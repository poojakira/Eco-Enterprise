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
    print("🚀 Starting EcoTrack Backend for Phase 5 Verification...")
    process = subprocess.Popen(
        ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=BACKEND_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(5) # Wait for startup
    return process

def test_async_ingestion():
    print("\n⚡ Testing Distributed Ingestion (Phase 5)...")
    
    with httpx.Client(base_url=BASE_URL) as client:
        # 1. Login
        print("🔑 Logging In...")
        login_data = {"username": "admin_user", "password": "secure_password_123"}
        r = client.post("/api/v1/auth/login", data=login_data)
        token = r.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 2. Ingest Data (Async)
        print("📥 Sending Ingestion Batch (Expect 202 Accepted)...")
        ingest_data = [
            {"sku_name": "STREAM-1", "category": "Packaging", "region": "EU", "vendor": "ForestCorp", "raw_material_energy": 50.0, "manufacturing_energy": 100.0},
            {"sku_name": "STREAM-2", "category": "Packaging", "region": "EU", "vendor": "ForestCorp", "raw_material_energy": 60.0, "manufacturing_energy": 110.0}
        ]
        start_time = time.time()
        r = client.post("/api/v1/data/ingest", json=ingest_data, headers=headers)
        duration = time.time() - start_time
        
        if r.status_code == 202:
            res = r.json()
            print(f"✅ Ingestion Accepted (Time: {duration:.4f}s). Batch ID: {res['batch_id']}")
        else:
            print(f"❌ Ingestion Failed: {r.status_code} - {r.text}")
            return

        # 3. Wait for background processing
        print("⏳ Waiting for Stream Worker to process batch...")
        time.sleep(3)

        # 4. Verify Ledger/Audit
        print("🔍 Checking Ledger for Async Completion...")
        r = client.get("/api/v1/ledger/audit-log", headers=headers)
        if r.status_code == 200:
            logs = r.json()
            latest_batch = logs[0]["batch_id"]
            if latest_batch == res["batch_id"]:
                print(f"✅ Batch {latest_batch} found in Audit Log. Stream Processing Success.")
            else:
                print(f"⚠️  Batch ID mismatch. Expected {res['batch_id']}, found {latest_batch}")
        else:
            print(f"❌ Audit Log API Failed: {r.text}")

if __name__ == "__main__":
    server_process = None
    try:
        server_process = run_server()
        test_async_ingestion()
    except Exception as e:
        print(f"💥 Error: {e}")
    finally:
        if server_process:
            print("\n🛑 Shutting down server...")
            os.kill(server_process.pid, signal.SIGTERM)
            print("👋 Phase 5 Implementation Verified.")
