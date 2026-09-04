# 07 - API Contract Specifications 📜

All API endpoints reside under `/api/v1`.

## Endpoint Matrix

| Method | Path | Description | Status |
|---|---|---|---|
| `GET` | `/api/v1/health` | Service health & PostGIS DB readiness check | **VERIFIED** |
| `POST` | `/api/v1/reports` | Submit new incident report (20m spatial dedup check) | **VERIFIED** |
| `POST` | `/api/v1/reports/upload-photo` | Upload report photo to storage | **VERIFIED** |
| `GET` | `/api/v1/reports` | List incident reports with category/status filters | **VERIFIED** |
| `GET` | `/api/v1/reports/{report_id}` | Retrieve incident report details | **VERIFIED** |
| `POST` | `/api/v1/workers` | Register new cleanup worker profile | **VERIFIED** |
| `GET` | `/api/v1/workers` | List workers with status & verification filters | **VERIFIED** |
| `GET` | `/api/v1/workers/{worker_id}` | Retrieve worker detail | **VERIFIED** |
| `PATCH` | `/api/v1/workers/{worker_id}/status` | Update worker availability status | **VERIFIED** |
| `POST` | `/api/v1/vehicles` | Register transport fleet vehicle | **VERIFIED** |
| `GET` | `/api/v1/vehicles` | List fleet vehicles | **VERIFIED** |
| `GET` | `/api/v1/vehicles/{vehicle_id}` | Retrieve vehicle detail | **VERIFIED** |
| `POST` | `/api/v1/work-orders` | Dispatch cleanup work order for approved report | **VERIFIED** |
| `GET` | `/api/v1/work-orders` | List dispatched work orders | **VERIFIED** |
| `GET` | `/api/v1/work-orders/{work_order_id}` | Retrieve work order with sub-units | **VERIFIED** |
| `POST` | `/api/v1/assignments` | Assign worker to a work unit | **VERIFIED** |
| `GET` | `/api/v1/assignments` | List worker assignments | **VERIFIED** |
| `PATCH` | `/api/v1/assignments/{assignment_id}/status` | Update assignment status (accepted/in_progress/completed) | **VERIFIED** |
| `POST` | `/api/v1/evidence` | Worker submits photo proof evidence | **VERIFIED** |
| `GET` | `/api/v1/evidence` | List evidence filtered by work_unit_id | **VERIFIED** |
| `GET` | `/api/v1/evidence/{evidence_id}` | Retrieve specific evidence submission | **VERIFIED** |
| `POST` | `/api/v1/verifications` | Supervisor submits evidence verification decision | **VERIFIED** |
| `GET` | `/api/v1/verifications` | List verification records | **VERIFIED** |
| `GET` | `/api/v1/verifications/{verification_id}` | Retrieve verification record detail | **VERIFIED** |
| `GET` | `/api/v1/compensations` | List compensation eligibility audit records | **VERIFIED** |
| `GET` | `/api/v1/compensations/{comp_id}` | Retrieve specific compensation record | **VERIFIED** |
| `PATCH` | `/api/v1/compensations/{comp_id}/status` | Update compensation payout lifecycle status | **VERIFIED** |
| `POST` | `/api/v1/collections` | Create waste collection transport batch | **VERIFIED** |
| `GET` | `/api/v1/collections` | List waste collection transport batches | **VERIFIED** |
| `GET` | `/api/v1/collections/{batch_id}` | Retrieve waste collection batch detail | **VERIFIED** |
| `PATCH` | `/api/v1/collections/{batch_id}/status` | Update collection batch transport status | **VERIFIED** |
| `GET` | `/api/v1/audit` | Query immutable audit log trail | **VERIFIED** |
| `GET` | `/api/v1/audit/{audit_id}` | Retrieve single audit event | **VERIFIED** |
| `POST` | `/api/v1/auth/login` | Authenticate user & return JWT | PLANNED |
| `GET` | `/api/v1/dashboard/metrics` | Retrieve live operational telemetry | PLANNED |
| `GET` | `/api/v1/hotspots` | Fetch AI risk hotspot regions | PLANNED |

---

## Endpoint Details

### 1. GET `/api/v1/health`
- **Description**: Returns service health status, environment, and PostGIS database connection test.
- **Response** (`200 OK`): `{"status": "healthy", "service": "...", "database": {"status": "connected", "postgis": "..."}}`

### 2. POST `/api/v1/reports`
- **Description**: Ingests new incident report with 20m spatial near-duplicate check.
- **Request Body**: `{"description": "...", "latitude": 13.01, "longitude": 77.62, "category": "electronic", "volume_tier": "minor"}`
- **Response** (`201 Created`): `ReportResponse` JSON. Emits `report_created` audit event.

### 3. POST `/api/v1/workers`
- **Description**: Registers a new cleanup worker.
- **Request Body**: `{"phone": "+919876543210", "identity_ref": "ID-999"}`
- **Response** (`201 Created`): `WorkerResponse` JSON. Emits `worker_created` audit event.

### 4. POST `/api/v1/work-orders`
- **Description**: Dispatches a cleanup work order for an approved report and creates a primary `WorkUnit`.
- **Request Body**: `{"report_id": 1, "classification": "BULK_CLEANUP", "required_worker_count": 2}`
- **Response** (`201 Created`): `WorkOrderResponse` JSON with sub-units. Emits `work_order_created` audit event.

### 5. POST `/api/v1/assignments`
- **Description**: Assigns a registered worker to a `WorkUnit`.
- **Request Body**: `{"worker_id": 1, "work_unit_id": 1}`
- **Response** (`201 Created`): `AssignmentResponse` JSON. Emits `worker_assigned` audit event.

### 6. PATCH `/api/v1/assignments/{assignment_id}/status`
- **Description**: Advances assignment lifecycle state. Only valid transitions permitted:
  - `assigned` -> `accepted` (Emits `assignment_accepted`)
  - `accepted` -> `in_progress` (Emits `work_started`)
  - `in_progress` -> `completed` (Emits `work_completed`)
  - Any non-completed -> `cancelled` (Emits `assignment_cancelled`)
- **Request Body**: `{"status": "in_progress"}`
- **Response** (`200 OK`): `AssignmentResponse` JSON.

### 7. POST `/api/v1/evidence`
- **Description**: Submits photo proof evidence (`before`, `progress`, `after`).
- **Request Body**: `{"work_unit_id": 1, "evidence_type": "after", "image_url": "storage/uploads/after.jpg", "latitude": 12.99, "longitude": 77.61}`
- **Response** (`201 Created`): `EvidenceResponse` JSON. Emits `evidence_submitted` audit event.

### 8. POST `/api/v1/verifications`
- **Description**: Supervisor audit verification decision (`approved`, `rejected`, `requires_review`). If approved, automatically triggers a `Compensation` eligibility record.
- **Request Body**: `{"work_unit_id": 1, "evidence_id": 1, "status": "approved", "method": "manual", "notes": "Verified clean"}`
- **Response** (`201 Created`): `VerificationResponse` JSON. Emits `verification_approved` and `compensation_eligible` audit events.

### 9. GET `/api/v1/compensations`
- **Description**: Queries compensation eligibility records for verified work.
- **Query Params**: `worker_id` (optional), `status` (optional), `skip`, `limit`.
- **Response** (`200 OK`): `List[CompensationResponse]`.

### 10. POST `/api/v1/collections`
- **Description**: Creates durable waste collection batch for transport aggregation.
- **Request Body**: `{"vehicle_id": 1, "total_volume_m3": 5.0}`
- **Response** (`201 Created`): `CollectionBatchResponse` JSON. Emits `collection_batch_created` audit event.

### 11. GET `/api/v1/audit`
- **Description**: Queries immutable audit logs (admin access).
- **Query Params**: `action` (optional), `entity_type` (optional), `skip`, `limit`.
- **Response** (`200 OK`): `List[AuditLogResponse]`.
