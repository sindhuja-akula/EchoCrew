import time
import urllib.request
import json
import sys

# Ensure UTF-8 output encoding for console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://localhost:8000/api/v1"

def api_post(endpoint, data):
    req = urllib.request.Request(
        f"{BASE_URL}{endpoint}",
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode('utf-8'))

def api_patch(endpoint, data):
    req = urllib.request.Request(
        f"{BASE_URL}{endpoint}",
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='PATCH'
    )
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode('utf-8'))

def api_get(endpoint):
    with urllib.request.urlopen(f"{BASE_URL}{endpoint}") as res:
        return json.loads(res.read().decode('utf-8'))

def run_demo():
    print("=========================================================================")
    print("  CLEANLOOP / ECHOCREW - LIVE END-TO-END OPERATIONAL DEMONSTRATION")
    print("=========================================================================\n")

    # 1. Health check
    health = api_get("/health")
    print(f"[+] STEP 1: System Health Check -> Status: {health['status'].upper()} (DB: {health['database']['status']})")

    # 2. Citizen Report Creation
    print("\n[+] STEP 2: Citizen Submits Illegal Garbage Report")
    report_data = {
        "description": "Massive unsegregated plastic and organic pile near Indiranagar Metro Station exit",
        "latitude": 12.9784,
        "longitude": 77.6408,
        "category": "mixed",
        "volume_tier": "bulk",
        "image_url": "storage/uploads/demo_garbage_site.jpg"
    }
    report = api_post("/reports", report_data)
    print(f"   -> Created Report ID: #{report['id']}")
    print(f"   -> Location: {report['latitude']}° N, {report['longitude']}° E")
    print(f"   -> Category: {report['category'].upper()} | Volume: {report['volume_tier'].upper()}")
    print(f"   -> Status: {report['status'].upper()}")

    # 3. Spatial Deduplication Check Demo (Attempting second report within 10m)
    print("\n[+] STEP 3: Spatial Deduplication Test (Second Citizen Reports Nearby within 10m)")
    nearby_data = {
        "description": "Trash overflowing on sidewalk",
        "latitude": 12.97842,
        "longitude": 77.64082,
        "category": "mixed",
        "volume_tier": "bulk"
    }
    dup_report = api_post("/reports", nearby_data)
    print(f"   -> Created Report ID: #{dup_report['id']}")
    print(f"   -> Is Spatial Duplicate? {dup_report['is_spatial_duplicate']}")
    print(f"   -> Linked to Primary Report: #{dup_report['duplicate_of_report_id']}")

    # 4. Supervisor Work Order Dispatch
    print("\n[+] STEP 4: Dispatcher Reviews & Issues Work Order")
    wo_data = {
        "report_id": report['id'],
        "classification": "BULK_CLEANUP",
        "required_worker_count": 2
    }
    work_order = api_post("/work-orders", wo_data)
    work_unit = work_order['units'][0]
    print(f"   -> Work Order Code: {work_order['work_code']}")
    print(f"   -> Work Unit Code: {work_unit['unit_code']}")
    print(f"   -> Work Order Status: {work_order['status'].upper()}")

    # 5. Worker Registration & Assignment
    print("\n[+] STEP 5: Register & Assign Sanitation Responder")
    unique_phone = f"+9198{int(time.time() * 1000) % 100000000:08d}"
    worker = api_post("/workers", {"phone": unique_phone, "identity_ref": "EMP-BLR-4092"})
    print(f"   -> Registered Worker ID: #{worker['id']} ({worker['worker_code']})")

    assignment = api_post("/assignments", {
        "worker_id": worker['id'],
        "work_unit_id": work_unit['id']
    })
    print(f"   -> Created Assignment ID: #{assignment['id']} (Status: {assignment['status'].upper()})")

    # 6. Responder Job State Transitions
    print("\n[+] STEP 6: Worker Accepts & Starts Field Job")
    acc = api_patch(f"/assignments/{assignment['id']}/status", {"status": "accepted"})
    print(f"   -> State Transition: {acc['status'].upper()}")
    prog = api_patch(f"/assignments/{assignment['id']}/status", {"status": "in_progress"})
    print(f"   -> State Transition: {prog['status'].upper()}")

    # 7. Evidence Photo Proof Submission
    print("\n[+] STEP 7: Worker Uploads BEFORE & AFTER Cleaning Evidence Photos")
    ev_before = api_post("/evidence", {
        "work_unit_id": work_unit['id'],
        "work_assignment_id": assignment['id'],
        "evidence_type": "before",
        "image_url": "storage/uploads/demo_before.jpg"
    })
    print(f"   -> Uploaded BEFORE Photo Evidence ID: #{ev_before['id']}")

    ev_after = api_post("/evidence", {
        "work_unit_id": work_unit['id'],
        "work_assignment_id": assignment['id'],
        "evidence_type": "after",
        "image_url": "storage/uploads/demo_after.jpg"
    })
    print(f"   -> Uploaded AFTER Photo Evidence ID: #{ev_after['id']}")

    # Worker completes job
    comp_job = api_patch(f"/assignments/{assignment['id']}/status", {"status": "completed"})
    print(f"   -> Worker Job State: {comp_job['status'].upper()}")

    # 8. Supervisor Verification Approval & Payout Trigger
    print("\n[+] STEP 8: Supervisor Audits Evidence & Approves Cleanup")
    verification = api_post("/verifications", {
        "work_unit_id": work_unit['id'],
        "evidence_id": ev_after['id'],
        "status": "approved",
        "method": "supervisor",
        "notes": "Verified complete site clearance and sanitation"
    })
    print(f"   -> Verification Decision: {verification['status'].upper()} (Method: {verification['method'].upper()})")

    # Check auto-compensation record
    comps = api_get(f"/compensations?worker_id={worker['id']}")
    comp_record = comps[0]
    print(f"   -> Payout Eligibility Created: #{comp_record['id']} Amount: {comp_record['amount']} {comp_record['currency']} (Status: {comp_record['status'].upper()})")

    # 9. Waste Collection Batch Aggregation
    print("\n[+] STEP 9: Create Waste Transport Collection Batch")
    batch = api_post("/collections", {
        "total_volume_m3": 6.8
    })
    print(f"   -> Created Batch Code: {batch['batch_code']}")
    print(f"   -> Total Transport Volume: {batch['total_volume_m3']} m³")
    print(f"   -> Batch Status: {batch['status'].upper()}")

    # Transit updates
    sealed = api_patch(f"/collections/{batch['id']}/status", {"status": "sealed"})
    transit = api_patch(f"/collections/{batch['id']}/status", {"status": "in_transit"})
    delivered = api_patch(f"/collections/{batch['id']}/status", {"status": "delivered"})
    print(f"   -> Advanced Transport Lifecycle: {delivered['status'].upper()}")

    # 10. System Audit Log Inspection
    print("\n[+] STEP 10: Inspect Immutable Audit Log Trail")
    audits = api_get("/audit?limit=6")
    for a in audits:
        print(f"   - Audit #{a['id']}: [{a['action']}] on {a['entity_type']} #{a['entity_id']} -> {a['description']}")

    print("\n=========================================================================")
    print("  DEMO COMPLETED SUCCESSFULLY! All 10 operational pipeline steps passed.")
    print("=========================================================================\n")

if __name__ == "__main__":
    run_demo()
