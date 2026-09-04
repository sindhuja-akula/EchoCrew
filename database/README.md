# CleanLoop Database Module 🗄️

CleanLoop Phase 1 Database Foundation using PostgreSQL 16 + PostGIS spatial extensions, SQLAlchemy ORM models, Alembic migrations, custom ENUMs, spatial indexing, seed data scripts, and automated unit test suites.

---

## 📂 Directory Structure

```
database/
│
├── migrations/          # Alembic DB migrations
│   ├── versions/
│   │   └── 001_phase1_foundation.py
│   └── README.md
│
├── models/              # SQLAlchemy ORM Models & Enums
│   ├── __init__.py
│   ├── base.py          # Declarative Base & TimestampMixin
│   ├── user.py          # User entity (Commander, Dispatcher, Citizen, etc.)
│   ├── garbage_report.py# GarbageReport entity (PostGIS POINT, Lat/Lon, VolumeTier, ReportStatus)
│   ├── waste.py         # WasteCategory & VolumeTier descriptors
│   └── enums.py         # UserRole, WasteCategory, VolumeTier, ReportStatus
│
├── seed/                # Seed Data Generation
│   ├── __init__.py
│   └── seed_data.py     # Development seed script (users & near-duplicate reports < 20m)
│
├── scripts/             # Administration Utilities
│   ├── init_db.py       # Enable PostGIS, create tables, run seed_data
│   └── reset_db.py      # Schema teardown and re-initialization
│
├── tests/               # Unit & Spatial Test Suite
│   ├── __init__.py
│   ├── test_connection.py # Engine & connection tests
│   ├── test_models.py     # Model & Enum validation tests
│   └── test_spatial.py    # Haversine distance & 20m deduplication spatial tests
│
└── README.md            # Database documentation
```

---

## ⚙️ Core Database Entities (Phase 1)

1. **`User`**:
   - Primary Key `id` (autoincrement)
   - Unique `username`, `email`
   - `role` Enum: `commander`, `dispatcher`, `crew_lead`, `responder`, `citizen`
   - `created_at`, `updated_at`

2. **`GarbageReport`**:
   - Primary Key `id` (autoincrement)
   - Foreign Key `reporter_id` -> `users.id` (Nullable for citizen/anonymous reporting)
   - `latitude`, `longitude` (Float coordinates)
   - `location`: PostGIS `Geometry(POINT, srid=4326)` with GIST spatial index
   - `category` Enum: `wet`, `dry`, `electronic`, `clothing`, `hazardous`, `mixed`, `other`
   - `volume_tier` Enum: `minor` (< 0.2 m³), `moderate` (0.2-1.0 m³), `bulk` (> 1.0 m³)
   - `status` Enum: `reported`, `under_review`, `approved`, `assigned`, `in_progress`, `cleaned`, `verified`
   - `image_url`: S3/MinIO file reference URL
   - `created_at`, `updated_at`

---

## 🧪 Running Database Tests

```bash
python -m unittest discover -s database/tests -p "test_*.py"
```
