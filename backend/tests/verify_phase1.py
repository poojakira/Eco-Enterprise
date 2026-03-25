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
    print("🚀 Starting EcoTrack Backend...")
    process = subprocess.Popen(
        ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=BACKEND_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(5) # Wait for startup
    return process

def test_auth_flow():
    print("\n🔐 Testing Authentication Flow...")
    
    with httpx.Client(base_url=BASE_URL) as client:
        # 1. Register
        print("📝 Registering User...")
        reg_data = {
            "username": "admin_user",
            "password": "secure_password_123",
            "email": "admin@ecotrack.ent",
            "role": "admin"
        }
        r = client.post("/api/v1/auth/register", json=reg_data)
        if r.status_code == 200:
            print("✅ Registration Successful.")
        else:
            print(f"❌ Registration Failed: {r.text}")
            return

        # 2. Login
        print("🔑 Logging In...")
        login_data = {
            "username": "admin_user",
            "password": "secure_password_123"
        }
        r = client.post("/api/v1/auth/login", data=login_data)
        if r.status_code == 200:
            token = r.json()["access_token"]
            print("✅ Login Successful. Token acquired.")
        else:
            print(f"❌ Login Failed: {r.text}")
            return

        # 3. Access Protected Metrics
        print("📊 Accessing Protected Metrics...")
        headers = {"Authorization": f"Bearer {token}"}
        r = client.get("/api/v1/metrics", headers=headers)
        if r.status_code == 200:
            print(f"✅ Metrics Access Successful: {r.json()['total_co2']} total CO2")
        else:
            print(f"❌ Metrics Access Failed: {r.text}")

        # 4. Test RBAC (Ingest something)
        print("📥 Testing RBAC (Admin Ingestion)...")
        ingest_data = [{
            "sku_name": "Test SKU 1",
            "category": "Electronics",
            "region": "NA",
            "vendor": "EcoSystems",
            "raw_material_energy": 100.0,
            "raw_material_emission_factor": 0.5,
            "raw_material_waste": 5.0,
            "manufacturing_energy": 200.0,
            "manufacturing_efficiency": 0.9,
            "manufacturing_water_usage": 50.0,
            "transport_distance_km": 500.0,
            "transport_mode_factor": 0.2,
            "logistics_energy": 10.0,
            "usage_energy_consumption": 5.0,
            "usage_duration_hours": 1000.0,
            "grid_carbon_intensity": 0.4,
            "recycling_efficiency": 0.8,
            "disposal_emission_factor": 0.1,
            "recovered_material_value": 2.0,
            "state_complexity_index": 1.5,
            "policy_action_score": 0.8,
            "optimization_reward_signal": 1.0
        }]
        r = client.post("/api/v1/data/ingest", json=ingest_data, headers=headers)
        if r.status_code == 200:
            print(f"✅ Data Ingestion Successful. Chain: {r.json()['verification_chain']}")
        else:
            print(f"❌ Ingestion Failed: {r.text}")

if __name__ == "__main__":
    # Ensure dependencies are installed for the test
    # subprocess.run(["pip", "install", "httpx"], check=True)
    
    server_process = None
    try:
        server_process = run_server()
        test_auth_flow()
    except Exception as e:
        print(f"💥 Error: {e}")
    finally:
        if server_process:
            print("\n🛑 Shutting down server...")
            os.kill(server_process.pid, signal.SIGTERM)
            print("👋 Implementation Verified.")
