# 04 - Database Architecture: Phase 1 Foundation 🗄️

## Overview
CleanLoop Phase 1 utilizes PostgreSQL 16 with PostGIS spatial extensions for storing users, garbage reports, volumetric classifications, report lifecycle statuses, and spatial geolocation data.

---

## 1. Spatial Architecture & Coordinate System
- **Coordinate Reference System (CRS)**: WGS 84 (`EPSG:4326` / `SRID:4326`).
- **Spatial Field Type**: `Geometry(POINT, srid=4326)` representing exact latitude & longitude coordinates.
- **Spatial Index**: GIST spatial index (`idx_garbage_reports_location`) for sub-millisecond radius search.
- **Deduplication Radius**: **20 meters**. The location geometry supports PostGIS ST_DWithin and ST_Distance calculations to detect near-duplicate citizen reports within 20m.

---

## 2. Core Entities & Schema Definitions

### A. `users` Table
Stores administrative personnel, dispatchers, crew leads, field responders, and reporting citizens.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `INTEGER` | Primary Key, Autoincrement | Unique User ID |
| `username` | `VARCHAR(50)` | UNIQUE, NOT NULL, Index | Unique handle |
| `email` | `VARCHAR(255)` | UNIQUE, NOT NULL, Index | Unique email address |
| `hashed_password` | `VARCHAR(255)` | NULLABLE | Hashed password string |
| `role` | `user_role` (ENUM) | NOT NULL, Default `citizen` | `commander`, `dispatcher`, `crew_lead`, `responder`, `citizen` |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, Default `now()` | Record creation timestamp |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL, Default `now()` | Record last update timestamp |

### B. `garbage_reports` Table
Stores incident reports containing spatial point locations, category tags, volumetric classifications, and status lifecycles.

| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | `INTEGER` | Primary Key, Autoincrement | Unique Report ID |
| `reporter_id` | `INTEGER` | Foreign Key (`users.id`), NULLABLE | Reporting user ID |
| `description` | `TEXT` | NULLABLE | Freeform report description |
| `latitude` | `FLOAT` | NOT NULL | Latitude float coordinate |
| `longitude` | `FLOAT` | NOT NULL | Longitude float coordinate |
| `location` | `GEOMETRY(POINT, 4326)` | NOT NULL, GIST Index | PostGIS spatial point |
| `category` | `waste_category` (ENUM) | NOT NULL, Default `mixed` | `wet`, `dry`, `electronic`, `clothing`, `hazardous`, `mixed`, `other` |
| `volume_tier` | `volume_tier` (ENUM) | NOT NULL, Default `moderate` | `minor` (< 0.2 m³), `moderate` (0.2 - 1.0 m³), `bulk` (> 1.0 m³) |
| `status` | `report_status` (ENUM) | NOT NULL, Default `reported` | `reported`, `under_review`, `approved`, `assigned`, `in_progress`, `cleaned`, `verified` |
| `image_url` | `VARCHAR(512)` | NULLABLE | MinIO / S3 image reference |
| `created_at` | `TIMESTAMPTZ` | NOT NULL, Index | Record creation timestamp |
| `updated_at` | `TIMESTAMPTZ` | NOT NULL | Record last update timestamp |

---

## 3. Custom Enum Definitions

### `waste_category`
- `wet`: Wet / Organic waste
- `dry`: Dry / Recyclable waste
- `electronic`: E-Waste / Electronics
- `clothing`: Textiles & clothing
- `hazardous`: Hazardous / Toxic waste
- `mixed`: Mixed unsorted garbage
- `other`: Other unclassified waste

### `volume_tier` (Volumetric Classification - No Exact Weights)
- `minor`: Small household bag / litter (~ < 0.2 m³)
- `moderate`: Medium pile / multiple dumped bags (~ 0.2 - 1.0 m³)
- `bulk`: Large dumping site / truck load required (~ > 1.0 m³)

### `report_status` (Lifecycle Control)
`reported` ➔ `under_review` ➔ `approved` ➔ `assigned` ➔ `in_progress` ➔ `cleaned` ➔ `verified`

---

## 4. Migration & Seed Strategy
- **Alembic Migrations**: `backend/alembic/versions/001_phase1_foundation.py` applies `postgis` extension, `users` table, `garbage_reports` table, and GIST spatial indexes.
- **Seed Data**: `database/seed/seed_data.py` inserts fake test users and sample garbage reports including spatial near-duplicates within 20 meters.

---

## 5. Testing & Verification
Unit tests in `database/tests/` verify:
- Engine & connection (`test_connection.py`)
- ORM model instantiation & Enum validations (`test_models.py`)
- Spatial WKT formatting & 20-meter Haversine distance logic (`test_spatial.py`)

---

## 6. Future Extension Points
The Phase 1 schema is decoupled to cleanly support future phases:
- `tasks` table linking `garbage_reports.id` to crew assignments.
- `crews` & `vehicles` tables referencing volume capacities (`m³`).
- `verifications` table storing post-cleanup photo audits.
