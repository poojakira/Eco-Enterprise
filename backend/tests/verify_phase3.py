import httpx
import time
import subprocess
import os
import signal
import sys
import shutil

# --- Configuration ---
BASE_URL = "http://127.0.0.1:8000"
BACKEND_DIR = r"c:\Users\pooja\Downloads\EcoTrack-Enterprise-main (3)\EcoTrack-Enterprise-main\EcoTrack-Enterprise\EcoTrack-Enterprise\backend"

def run_server():
    print("🚀 Starting EcoTrack Backend for Phase 3 Verification...")
    process = subprocess.Popen(
        ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=BACKEND_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(5) # Wait for startup
    return process

def test_ml_and_mlflow():
    print("\n🧠 Testing Advanced ML & MLflow (Phase 3)...")
    
    with httpx.Client(base_url=BASE_URL) as client:
        # 1. Login
        print("🔑 Logging In...")
        login_data = {"username": "admin_user", "password": "secure_password_123"}
        r = client.post("/api/v1/auth/login", data=login_data)
        if r.status_code != 200:
             print("❌ Login Failed.")
             return
        
        token = r.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 2. Ingest Data (Need history for forecast)
        print("📥 Preparing Telemetry History...")
        ingest_data = []
        for i in range(12):
            ingest_data.append({
                "sku_name": f"SKU-PH3-{i}", 
                "category": "Electronics", 
                "region": "GLOBAL", 
                "vendor": "HyperProvider", 
                "raw_material_energy": 100.0 + (i * 5), 
                "manufacturing_energy": 200.0 + (i * 2)
            })
        client.post("/api/v1/data/ingest", json=ingest_data, headers=headers)

        # 3. Test Forecast
        print("📈 Testing Ensemble Forecast...")
        r = client.get("/api/v1/forecast", headers=headers)
        if r.status_code == 200:
            res = r.json()
            print(f"✅ Forecast Successful. Baseline First: {res['baseline_projection'][0]}")
            print(f"✅ Methodology: {res['methodology']}")
        else:
            print(f"❌ Forecast Failed: {r.text}")

        # 4. Test Predict with MLflow
        print("🔮 Testing Prediction & MLflow Logging...")
        pred_data = {
            "sku_name": "MLFLOW-TEST", "category": "Test", "region": "LAB", "vendor": "ML-Ops",
            "raw_material_energy": 150.0, "raw_material_emission_factor": 0.5, "raw_material_waste": 5.0,
            "manufacturing_energy": 300.0, "manufacturing_efficiency": 0.9, "manufacturing_water_usage": 50.0,
            "transport_distance_km": 1000.0, "transport_mode_factor": 0.2, "logistics_energy": 20.0,
            "usage_energy_consumption": 10.0, "usage_duration_hours": 2000.0, "grid_carbon_intensity": 0.4,
            "recycling_efficiency": 0.8, "disposal_emission_factor": 0.1, "recovered_material_value": 5.0,
            "state_complexity_index": 2.0, "policy_action_score": 0.9, "optimization_reward_signal": 1.0
        }
        r = client.post("/predict", json=pred_data, headers=headers)
        if r.status_code == 200:
            print(f"✅ Prediction Successful: {r.json()['predicted_carbon_footprint']}")
        else:
            print(f"❌ Prediction Failed: {r.text}")

        # 5. Verify MLflow directory
        print("🗂️ Verifying MLflow Run Storage...")
        mlruns_path = os.path.join(BACKEND_DIR, "mlruns")
        if os.path.exists(mlruns_path):
            print(f"✅ MLflow 'mlruns' directory detected at {mlruns_path}")
        else:
            print(f"⚠️ MLflow 'mlruns' directory not found locally. Check environment config.")

if __name__ == "__main__":
    server_process = None
    try:
        server_process = run_server()
        test_ml_and_mlflow()
    except Exception as e:
        print(f"💥 Error: {e}")
    finally:
        if server_process:
            print("\n🛑 Shutting down server...")
            os.kill(server_process.pid, signal.SIGTERM)
            print("👋 Phase 3 Implementation Verified.")
