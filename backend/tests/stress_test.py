import httpx # type: ignore
import time
import asyncio
import statistics
import subprocess
import os
import signal
import sys

BASE_URL = "http://127.0.0.1:8000"
BACKEND_DIR = r"c:\Users\pooja\Downloads\EcoTrack-Enterprise-main (3)\EcoTrack-Enterprise-main\EcoTrack-Enterprise\EcoTrack-Enterprise\backend"

async def stress_test_ingestion():
    print("🏙️  Starting Industrial Stress Test (Phase 7)...")
    
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=30.0) as client:
        # 1. Login
        login_data = {"username": "admin_user", "password": "secure_password_123"}
        r = await client.post("/api/v1/auth/login", json=login_data)
        token = r.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # 2. Burst Ingestion (1000 records in 10 batches)
        print("🌪️ Sending 1000 High-Complexity Telemetry Records...")
        latencies = []
        batch_ids = []
        
        for i in range(10):
            batch = [
                {
                    "sku_name": f"STRESS-UNIT-{i}-{j}",
                    "category": "Industrial Systems",
                    "region": "Global",
                    "vendor": "StressCorp",
                    "raw_material_energy": 100.0 + i + j,
                    "manufacturing_energy": 200.0 + i + j
                }
                for j in range(100)
            ]
            start = time.time()
            res = await client.post("/api/v1/data/ingest", json=batch, headers=headers)
            latencies.append(time.time() - start)
            if res.status_code == 202:
                batch_ids.append(res.json()["batch_id"])
            else:
                print(f"❌ Batch {i} Failed: {res.text}")

        # 3. Concurrent AI Inference
        print("🧠 Running 50 Concurrent AI Inference Projections...")
        inf_start = time.time()
        tasks = []
        for _ in range(50):
            payload = {"manufacturing_energy": 120.0, "manufacturing_efficiency": 0.85, "raw_material_energy": 60.0, "transport_distance_km": 500.0}
            tasks.append(client.post("/api/v1/predict", json=payload, headers=headers))
        
        inf_responses = await asyncio.gather(*tasks)
        inf_duration = time.time() - inf_start

        # 4. Results Summary
        print("\n📈 [bold underline]Performance Report[/bold underline]")
        print(f"Ingestion Throughput: 1000 records / {sum(latencies):.2f}s")
        print(f"Avg API Response Time (202): {statistics.mean(latencies)*1000:.2f}ms")
        print(f"Total AI Inference Time (50 reqs): {inf_duration:.2f}s")
        
        # 5. Final Cryptographic Audit
        print("\n🛡️  Executing Post-Stress Ledger Audit...")
        time.sleep(5) # Wait for worker to finish
        verify = await client.get("/api/v1/ledger/verify-chain", headers=headers)
        if verify.status_code == 200:
             audit = verify.json()
             print(f"✅ Cryptographic Result: {audit['status']}")
             print(f"💎 Merkle Root Validated for {audit['records_scanned']} records.")
        else:
             print(f"❌ Audit Failed: {verify.text}")

if __name__ == "__main__":
    print("🚀 Running EcoTrack Client-Side Stress Test...")
    try:
        asyncio.run(stress_test_ingestion())
    except Exception as e:
        print(f"💥 Stress Test Failed: {e}")
    finally:
        print("🏁 Final Validation Cycle Complete.")
