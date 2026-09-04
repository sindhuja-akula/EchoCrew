# 05 - Backend Architecture ⚙️

## Framework & Structural Patterns
The backend is built with FastAPI and Python 3.12 following Clean Architecture principles:

- **Router Layer** (`app/api/v1/endpoints/`): Thin HTTP controllers, routing, request parsing, and error mapping.
- **Schema Validation Layer** (`app/schemas/`): Strict input and output boundary validation via Pydantic V2 models.
- **Service Layer** (`app/services/`): Business logic, state transition enforcement, spatial calculations, and audit log generation.
- **Data Access & ORM** (`database/models/`): SQLAlchemy Declarative ORM models with PostGIS GeoAlchemy2 extensions.
- **Core Layer** (`app/core/`): Cross-cutting settings, database engine/session lifecycle, and JWT security foundations.
- **Storage Layer** (`app/services/storage_service.py`): Object storage integration with local disk fallback and MinIO S3-compatibility.

---

## Directory Structure
```
backend/
│
├── alembic.ini
├── README.md
│
├── alembic/
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
│       ├── 001_phase1_foundation.py      # Core tables: users, garbage_reports
│       ├── 002_phase2_extensions.py      # Operational tables: workers, vehicles, work_orders,
│       │                                 # work_units, assignments, evidence, verifications,
│       │                                 # compensations, collection_batches
│       └── 003_audit_log.py              # Audit logging: audit_logs
│
├── app/
│   ├── main.py                           # Application factory, middleware & routing registration
│   ├── config.py / core/config.py        # Centralized environment settings
│   ├── database.py / core/database.py    # SQLAlchemy session factory & get_db dependency
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── security.py                   # JWT creation, decoding, password hash utilities
│   │   ├── constants.py
│   │   ├── exceptions.py
│   │   └── logging.py
│   │
│   ├── api/
│   │   └── v1/
│   │       ├── router.py                 # Central v1 endpoint router aggregation
│   │       └── endpoints/
│   │           ├── health.py             # System & PostGIS health check
│   │           ├── reports.py            # Citizen/responder report ingestion & 20m spatial dedup
│   │           ├── workers.py            # Worker registration, lifecycle status, listing
│   │           ├── vehicles.py           # Fleet vehicle registration & retrieval
│   │           ├── work_orders.py        # Cleanup dispatching per report & work unit association
│   │           ├── assignments.py        # Worker assignment lifecycle transitions
│   │           ├── evidence.py           # Photo evidence submission & coordinate verification
│   │           ├── verification.py       # Supervisor review, approval & rejection decisions
│   │           ├── compensation.py       # Eligibility tracking & payout status lifecycle
│   │           ├── collections.py        # Batch-level waste transport aggregation
│   │           └── audit.py              # Query immutable audit event trail
│   │
│   ├── schemas/                          # Pydantic validation contracts
│   │   ├── report.py
│   │   ├── worker.py
│   │   ├── vehicle.py
│   │   ├── work_order.py
│   │   ├── work_unit.py
│   │   ├── assignment.py
│   │   ├── evidence.py
│   │   ├── verification.py
│   │   ├── compensation.py
│   │   ├── collection.py
│   │   └── audit.py
│   │
│   ├── services/                         # Business logic services
│   │   ├── report_service.py             # Spatial deduplication (20m PostGIS ST_DWithin)
│   │   ├── worker_service.py             # Worker profile & status management
│   │   ├── vehicle_service.py            # Fleet vehicle operations
│   │   ├── work_order_service.py         # Work order creation & work unit dispatching
│   │   ├── assignment_service.py         # State machine for worker assignments
│   │   ├── evidence_service.py           # Storage validation & evidence recording
│   │   ├── verification_service.py       # Quality review & compensation trigger
│   │   ├── compensation_service.py       # Eligibility records management
│   │   ├── collection_service.py         # Durable transport batch lifecycle
│   │   ├── audit_service.py              # System event audit recorder
│   │   └── storage_service.py            # Local and MinIO object storage
│   │
│   └── utils/
│       └── validation.py                 # Coordinate bounds & mime-type validation
│
└── tests/
    ├── conftest.py                       # Test client setup
    ├── test_health.py                    # Health & DB readiness tests
    ├── test_reports.py                   # Report ingestion, bounds & 20m dedup tests
    ├── test_storage.py                   # Upload mime-type validation tests
    ├── test_workers.py                   # Worker registration & status transition tests
    ├── test_work_orders.py               # Work order creation & invalid report tests
    ├── test_assignments.py               # Worker assignment lifecycle state machine tests
    ├── test_evidence.py                  # Evidence submission & query tests
    ├── test_verification.py              # Verification approval/rejection decision tests
    ├── test_compensation.py              # Compensation eligibility & lifecycle status tests
    ├── test_collections.py               # Transport batch creation & state tests
    ├── test_vehicles_api.py              # Fleet vehicle registration & list tests
    ├── test_audit.py                     # Audit log creation & querying tests
    └── test_api.py                       # Root status tests
```

---

## Core Operational Workflow
```
Garbage Report (ReportStatus.REPORTED)
      ↓ (Dispatch)
Work Order (WorkOrderStatus.OPEN) + Work Units (WorkUnitStatus.PENDING)
      ↓ (Assignment)
Worker Assignment (AssignmentStatus.ASSIGNED -> ACCEPTED -> IN_PROGRESS -> COMPLETED)
      ↓ (Evidence)
Cleaning Evidence (EvidenceType.AFTER / PROGRESS / BEFORE)
      ↓ (Audit Review)
Verification (VerificationStatus.APPROVED)
      ↓ (Automated Trigger)
Compensation (CompensationStatus.ELIGIBLE -> PROCESSING -> PAID)
      ↓ (Aggregation)
Waste Collection Batch (CollectionBatchStatus.COLLECTING -> SEALED -> IN_TRANSIT -> DELIVERED)
```
Each state transition emits an immutable `AuditLog` event via `AuditService`.
