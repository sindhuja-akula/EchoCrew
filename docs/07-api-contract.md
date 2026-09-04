# 07 - API Contract Specifications 📜

All API endpoints reside under `/api/v1`.

## Endpoint Matrix

| Method | Path | Description | Status |
|---|---|---|---|
| `GET` | `/api/v1/health` | Service health & PostGIS DB readiness check | **IMPLEMENTED** |
| `POST` | `/api/v1/reports` | Submit new incident report (20m spatial dedup check) | **IMPLEMENTED** |
| `POST` | `/api/v1/reports/upload-photo` | Upload report photo to storage | **IMPLEMENTED** |
| `GET` | `/api/v1/reports` | List incident reports with category/status filters | **IMPLEMENTED** |
| `GET` | `/api/v1/reports/{report_id}` | Retrieve incident report details | **IMPLEMENTED** |
| `POST` | `/api/v1/workers` | Register new cleanup worker profile | **IMPLEMENTED** |
| `GET` | `/api/v1/workers` | List workers with status & verification filters | **IMPLEMENTED** |
| `GET` | `/api/v1/workers/{worker_id}` | Retrieve worker detail | **IMPLEMENTED** |
| `PATCH` | `/api/v1/workers/{worker_id}/status` | Update worker availability status | **IMPLEMENTED** |
| `POST` | `/api/v1/vehicles` | Register transport fleet vehicle | **IMPLEMENTED** |
| `GET` | `/api/v1/vehicles` | List fleet vehicles | **IMPLEMENTED** |
| `GET` | `/api/v1/vehicles/{vehicle_id}` | Retrieve vehicle detail | **IMPLEMENTED** |
| `POST` | `/api/v1/work-orders` | Dispatch cleanup work order for approved report | **IMPLEMENTED** |
| `GET` | `/api/v1/work-orders` | List dispatched work orders | **IMPLEMENTED** |
| `GET` | `/api/v1/work-orders/{work_order_id}` | Retrieve work order with sub-units | **IMPLEMENTED** |
| `POST` | `/api/v1/assignments` | Assign worker to a work unit | **IMPLEMENTED** |
| `GET` | `/api/v1/assignments` | List worker assignments | **IMPLEMENTED** |
| `PATCH` | `/api/v1/assignments/{assignment_id}/status` | Update assignment status (in_progress/completed) | **IMPLEMENTED** |
| `POST` | `/api/v1/evidence` | Worker submits photo proof evidence | **IMPLEMENTED** |
| `POST` | `/api/v1/verifications` | Supervisor submits evidence verification decision | **IMPLEMENTED** |
| `GET` | `/api/v1/compensations` | List compensation eligibility audit records | **IMPLEMENTED** |
| `POST` | `/api/v1/collections` | Create waste collection transport batch | **IMPLEMENTED** |
| `GET` | `/api/v1/collections` | List waste collection transport batches | **IMPLEMENTED** |
| `GET` | `/api/v1/collections/{batch_id}` | Retrieve waste collection batch detail | **IMPLEMENTED** |
| `PATCH` | `/api/v1/collections/{batch_id}/status` | Update collection batch transport status | **IMPLEMENTED** |
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
- **Response** (`201 Created`): `ReportResponse` JSON.

### 3. POST `/api/v1/workers`
- **Description**: Registers a new cleanup worker.
- **Request Body**: `{"phone": "+919876543210", "identity_ref": "ID-999"}`
- **Response** (`201 Created`): `WorkerResponse` JSON.

### 4. POST `/api/v1/work-orders`
- **Description**: Dispatches a cleanup work order for an approved report and creates a primary `WorkUnit`.
- **Request Body**: `{"report_id": 1, "classification": "BULK_CLEANUP", "required_worker_count": 2}`
- **Response** (`201 Created`): `WorkOrderResponse` JSON with sub-units.

### 5. POST `/api/v1/assignments`
- **Description**: Assigns a registered worker to a `WorkUnit`.
- **Request Body**: `{"worker_id": 1, "work_unit_id": 1}`
- **Response** (`201 Created`): `AssignmentResponse` JSON.

### 6. POST `/api/v1/evidence`
- **Description**: Submits photo proof evidence (`before`, `progress`, `after`).
- **Request Body**: `{"work_unit_id": 1, "evidence_type": "after", "image_url": "storage/uploads/after.jpg", "latitude": 12.99, "longitude": 77.61}`
- **Response** (`201 Created`): `EvidenceResponse` JSON.

### 7. POST `/api/v1/verifications`
- **Description**: Supervisor audit verification decision (`approved`, `rejected`, `requires_review`). Automatically creates a Compensation eligibility record if approved.
- **Request Body**: `{"work_unit_id": 1, "evidence_id": 1, "status": "approved", "method": "manual", "notes": "Verified clean"}`
- **Response** (`201 Created`): `VerificationResponse` JSON.

### 8. POST `/api/v1/collections`
- **Description**: Creates durable waste collection batch for transport aggregation.
- **Request Body**: `{"vehicle_id": 1, "total_volume_m3": 5.0}`
- **Response** (`201 Created`): `CollectionBatchResponse` JSON.
