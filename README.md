# CleanLoop ♻️

> AI-Assisted Urban Waste Detection, Accountability and Recovery Platform

---

## Project Status

**Phase 0: Project Setup** 🚀

CleanLoop is currently in Phase 0. Initial project scaffolding, microservice directory structures, environment configurations, database schemas, Docker orchestration, and API specifications have been defined and established.

---

## Project Overview

CleanLoop is an enterprise-grade AI-assisted urban waste management, detection, accountability, and recovery platform designed for municipalities, urban sanitation teams, and environmental response crews.

The platform addresses critical urban waste challenges through:
- **Computer Vision Waste Detection**: OpenCV and computer vision image analysis to classify waste density, volume, and material category.
- **Geospatial Hotspot Analytics**: Intelligent spatial radius deduplication and spatial clustering to prevent duplicate tickets and detect high-risk illegal dumping zones.
- **Accountability & Task Routing**: End-to-end task lifecycle management matching incident urgency with crew capabilities and vehicle capacity limits.
- **Real-Time Operational Telemetry**: Incident command dashboard for dispatchers and city planners.

---

## Current Architecture

CleanLoop uses a decoupled modular monorepo architecture:

```
                          ┌────────────────────────┐
                          │   Client Application   │
                          │      (Frontend)        │
                          └───────────┬────────────┘
                                      │ HTTP / REST
                                      ▼
                          ┌────────────────────────┐
                          │     FastAPI Backend    │
                          │   (API Router v1)      │
                          └───────┬────────┬───────┘
                                  │        │
               ┌──────────────────┘        └──────────────────┐
               ▼                                              ▼
    ┌────────────────────┐                         ┌────────────────────┐
    │ PostgreSQL DB      │                         │ MinIO S3 Storage   │
    │ (Schemas & Enums)  │                         │ (Waste Media Files)│
    └────────────────────┘                         └────────────────────┘
```

- **Backend**: FastAPI web service (`backend/app/main.py`) handling JWT authentication, REST endpoints, and domain service repositories.
- **Frontend**: Modular Web client interface (`frontend/`) displaying real-time metrics and task dispatches.
- **Database**: PostgreSQL 16 database (`database/`) with custom ENUMs, spatial indexes, and schema definitions.
- **Object Storage**: Local S3-compatible MinIO instance (`docker/minio/`) for storing image uploads and visual audit media.

---

## Repository Structure

```
EchoCrew/
│
├── .venv/                         # Python virtual environment
├── backend/                       # FastAPI backend service
│   ├── app/
│   │   ├── api/v1/                # Versioned API routes (auth, reports, tasks, crews, etc.)
│   │   ├── core/                  # Security, exceptions, logging, constants
│   │   ├── models/                # SQLAlchemy database entities
│   │   ├── schemas/               # Pydantic request/response models
│   │   ├── services/              # Business logic services
│   │   ├── repositories/          # Data access layer
│   │   ├── ai/                    # Computer vision & spatial cluster modules
│   │   └── utils/                 # Helper tools
│   └── tests/                     # Backend API unit tests
│
├── frontend/                      # Web user interface application
│   └── src/                       # Components, pages, layouts, services, styles
│
├── database/                      # Relational database schemas & migrations
│   ├── schema/                    # Extensions, custom ENUMs, and performance indexes
│   ├── seeds/                     # Initial seed SQL scripts (users, crews, vehicles)
│   └── scripts/                   # Master database initialization & reset scripts
│
├── docker/                        # Docker build & service configurations
│   ├── backend/                   # Backend Dockerfile
│   ├── frontend/                  # Frontend Dockerfile
│   ├── postgres/                  # Container init scripts
│   └── minio/                     # Local S3 object storage setup
│
├── docs/                          # Architecture & project documentation
│   └── decisions/                 # Architectural Decision Records (ADRs)
│
├── scripts/                       # Python administration utilities (setup, seed, reset, health)
├── tests/                         # Root integration test suites
├── storage/                       # Local development file storage (.gitkeep)
│
├── requirements.txt               # Main Python dependencies
├── requirements-dev.txt           # Development & testing dependencies
├── .env                           # Local environment secrets & config
├── .env.example                   # Configuration blueprint template
├── .gitignore                     # Git exclusion rules
├── README.md                      # LIVE project documentation
└── docker-compose.yml             # Container orchestration config
```

---

## Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11)
- **ASGI Server**: Uvicorn
- **ORM & Migrations**: SQLAlchemy, Alembic
- **Database Driver**: Psycopg
- **Data Validation**: Pydantic v2
- **Image Processing & Vision**: OpenCV (`opencv-python`), Pillow
- **Security & Auth**: PyJWT, Passlib (`bcrypt`), Python-Multipart

### Frontend
- **Interface**: HTML5, Vanilla JavaScript (ES6+), Vanilla CSS (Design System Tokens)
- **Architecture**: Component-based layout structure

### Database & Storage
- **Relational DB**: PostgreSQL 16 (Spatial extensions, custom ENUMs, B-Tree indexes)
- **Object Storage**: MinIO (S3-compatible local bucket)

### Infrastructure & Operations
- **Orchestration**: Docker & Docker Compose
- **Testing**: Pytest, Pytest-Asyncio, HTTPX
- **Code Quality**: Ruff, Black, Mypy

---

## Development Setup

### 1. Prerequisites
- Python 3.11+
- Node.js (v18+)
- Docker & Docker Compose

### 2. Environment Configuration
Clone the repository and initialize local environment variables:

```bash
cp .env.example .env
```

### 3. Python Environment & Dependencies
Initialize Python virtual environment and install development dependencies:

```bash
# Run automated setup script
python scripts/setup.py

# Activate virtual environment (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Activate virtual environment (Linux/macOS)
source .venv/bin/activate

# Install dependencies
pip install -r requirements-dev.txt
```

---

## Environment Variables

Key settings configured in `.env`:

| Key | Description | Default |
|---|---|---|
| `APP_NAME` | Service Name | `CleanLoop` |
| `ENVIRONMENT` | Environment Mode | `development` |
| `BACKEND_PORT` | FastAPI Service Port | `8000` |
| `FRONTEND_PORT` | Client App Port | `3000` |
| `SECRET_KEY` | JWT Signing Key | `change_this_super_secret_key` |
| `DATABASE_URL` | PostgreSQL Connection URI | `postgresql://echocrew:echocrew_pass@localhost:5432/echocrew_db` |
| `MINIO_ENDPOINT` | Object Storage Address | `localhost:9000` |
| `SPATIAL_DEDUPLICATION_RADIUS_METERS` | Report Deduplication Radius | `500` |

---

## Running the Project

### Option A: Docker Compose (Recommended)
Launch backend, frontend, database, and MinIO storage in containers:

```bash
docker-compose up --build
```

- **Frontend**: `http://localhost:3000`
- **Backend API**: `http://localhost:8000`
- **API Interactive Specs**: `http://localhost:8000/docs`
- **MinIO Console**: `http://localhost:9001`

### Option B: Local Development
Run backend server directly:

```bash
# Start FastAPI backend
uvicorn backend.app.main:app --reload --port 8000
```

---

## Testing

Run unit and integration test suites:

```bash
# Run backend & API test cases
pytest

# Check code formatting & linting
ruff check .
black --check .
mypy backend/app
```

Run system health check diagnostic:

```bash
python scripts/health_check.py
```

---

## Documentation

Comprehensive project documentation is maintained in the `docs/` folder:

- **[00-project-overview.md](docs/00-project-overview.md)**: Platform vision and objectives
- **[01-requirements.md](docs/01-requirements.md)**: Functional and non-functional requirements
- **[02-system-workflow.md](docs/02-system-workflow.md)**: Incident ingestion and dispatch workflow
- **[03-system-architecture.md](docs/03-system-architecture.md)**: Component diagrams & design patterns
- **[04-database-architecture.md](docs/04-database-architecture.md)**: Database schemas, ENUMs, and spatial indexes
- **[05-backend-architecture.md](docs/05-backend-architecture.md)**: FastAPI clean architecture breakdown
- **[06-frontend-architecture.md](docs/06-frontend-architecture.md)**: UI layout and component modularization
- **[07-api-contract.md](docs/07-api-contract.md)**: OpenAPI REST endpoint reference
- **[08-ai-architecture.md](docs/08-ai-architecture.md)**: Waste vision model & spatial clustering engine
- **[09-security.md](docs/09-security.md)**: Security, authentication, and RBAC rules
- **[10-testing.md](docs/10-testing.md)**: QA strategy and unit test suite organization
- **[11-deployment.md](docs/11-deployment.md)**: Container deployment instructions
- **[Architectural Decision Records (ADRs)](docs/decisions/README.md)**: Technical rationale behind major architecture decisions

---

## Development Roadmap

- [x] **Phase 0: Project Setup** — Repository scaffolding, environment configs, database schemas, Docker orchestration, and API specs.
- [ ] **Phase 1: Ingestion & Spatial Core** — Citizen/field report ingestion with 500-meter radius spatial deduplication buffer.
- [ ] **Phase 2: Computer Vision Integration** — Integration of OpenCV model for waste density and volume estimation.
- [ ] **Phase 3: Dispatch & Crew Optimization** — Automated matching of incidents with vehicle cubic volume and crew skills.
- [ ] **Phase 4: Analytics & Live Dashboard** — Real-time telemetry map dashboard with predictive risk hotspot alerts.

---

## Current Limitations

- **Phase 0 State**: Current API endpoints return structured mock data pending database migration execution.
- **Inference Engine**: Computer vision image analysis currently executes on CPU; GPU acceleration scheduled for Phase 2.

---

## Changelog

### 2026-09-04
- Created initial CleanLoop project structure.
- Added backend, frontend and database modules.
- Added development environment structure.
- Added Docker structure.
- Added documentation structure.
- Added environment templates.
- Added requirements files.

