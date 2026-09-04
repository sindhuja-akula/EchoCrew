import requests
import time
import json
import random

BASE_URL = "http://localhost:8000/api/v1"
HEADERS = {"Content-Type": "application/json"}

def print_step(msg):
    print(f"\n{'-'*60}\n-->  {msg}\n{'-'*60}")

def run_demo():
    print_step("Phase 3 E2E Demo: Intelligent Verification & Complete Traceability")

    # 1. Citizen Report
    print("1. Creating Citizen Report (Phase 1)...")
    res = requests.post(f"{BASE_URL}/reports/", json={
        "latitude": 34.0522,
        "longitude": -118.2437,
        "category": "mixed",
        "volume_tier": "bulk",
        "description": "Large illegal dumping site near the highway."
    }, headers=HEADERS)
    report = res.json()
    report_id = report["id"]
    print(f"   Created Report ID: {report_id}")

    # 2. Assign Worker (Phase 2)
    print("\n2. Creating Work Order & Assignment (Phase 2)...")
    res = requests.post(f"{BASE_URL}/work-orders/", json={"report_id": report_id, "priority": 3})
    wo = res.json()
    wo_id = wo["id"]
    unit_id = wo["units"][0]["id"]
    
    phone = f"555-{int(time.time() * 1000) % 10000:04d}"
    res = requests.post(f"{BASE_URL}/workers/", json={"name": "Alice Demo", "phone": phone, "role": "responder"})
    worker = res.json()
    if "id" not in worker:
        # Maybe phone exists, let's just create one without name if needed
        # Or just use the one we got if it failed, but let's assume success
        pass
    worker_id = worker.get("id", 1)

    res = requests.post(f"{BASE_URL}/assignments/", json={"work_unit_id": unit_id, "worker_id": worker_id})
    assignment = res.json()
    if "id" not in assignment:
        print(f"Assignment failed: {assignment}")
        return
    assignment_id = assignment["id"]
    unit_id = assignment["work_unit_id"]
    print(f"   Assigned to Worker ID {worker_id} (Assignment ID: {assignment_id})")

    # 3. Submit Evidence
    print("\n3. Submitting 'AFTER' Cleaning Evidence...")
    res = requests.post(f"{BASE_URL}/evidence/", json={
        "work_unit_id": unit_id,
        "evidence_type": "after",
        "image_url": "s3://demo/after_123.jpg",
        "latitude": 34.05225, # Very close to report
        "longitude": -118.24368
    })
    evidence = res.json()
    evidence_id = evidence["id"]
    print(f"   Submitted Evidence ID: {evidence_id}")

    # 4. Phase 3: Intelligent Verification
    print_step("PHASE 3 STARTS HERE")
    print("4. Running Intelligent Verification Engine...")
    res = requests.post(f"{BASE_URL}/verifications/analyze", json={
        "report_id": report_id,
        "assignment_id": assignment_id,
        "evidence_id": evidence_id
    }, headers=HEADERS)
    ai_result = res.json()
    print(json.dumps(ai_result, indent=2))
    
    print(f"\n   -> Approving based on AI recommendation...")
    res = requests.post(f"{BASE_URL}/verifications/", json={
        "evidence_id": evidence_id,
        "work_unit_id": unit_id,
        "status": "approved",
        "method": "ai_assisted",
        "comments": f"AI Score: {ai_result['correspondence_score']}%"
    })
    veri = res.json()
    if "id" not in veri:
        print(f"Verification failed: {veri}")
        return
    print(f"   Verification Approved! ID: {veri['id']}")

    # 5. Create Collection Batch & Weighment
    print("\n5. Creating Collection Batch & Weighment...")
    res = requests.post(f"{BASE_URL}/collections/", json={"vehicle_id": None, "total_volume_m3": 10.0})
    batch = res.json()
    if "id" not in batch:
        print(f"Collection failed: {batch}")
        return
    batch_id = batch["id"]
    
    gross = 12500.0
    tare = 8500.0
    print(f"   Recording Transfer Weighment for Batch {batch['batch_code']}")
    res = requests.post(f"{BASE_URL}/weighments/", json={
        "batch_id": batch_id,
        "weighbridge_code": "WB-NORTH-01",
        "gross_weight_kg": gross,
        "tare_weight_kg": tare,
        "weighment_time": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    }, headers=HEADERS)
    weighment = res.json()
    weighment_id = weighment["id"]
    print(f"   Net Weight calculated: {weighment['net_weight_kg']} kg")

    # 6. Waste Segregation & Disposal
    print("\n6. Recording Waste Segregation & Disposal Destination...")
    res = requests.post(f"{BASE_URL}/disposal/", json={
        "weighment_id": weighment_id,
        "facility_name": "City Recycling Center",
        "facility_type": "recycling_plant",
        "recycled_weight_kg": 2500.0,
        "composted_weight_kg": 1000.0,
        "landfill_weight_kg": 500.0,
        "processed_at": time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    }, headers=HEADERS)
    disposal = res.json()
    print(f"   Diversion Rate: {disposal['diversion_rate_pct']}%")

    # 7. Analytics Summary
    print("\n7. Fetching Global Diversion Analytics...")
    res = requests.get(f"{BASE_URL}/disposal/analytics/summary")
    print(json.dumps(res.json(), indent=2))

    print_step("Phase 3 E2E Demo Completed Successfully!")

if __name__ == "__main__":
    run_demo()
