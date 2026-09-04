# EchoCrew Backend Service ⚙️

FastAPI backend application structured around domain-driven modules, API versioning (`/api/v1`), security helpers, and data persistence layer.

---

## 📂 Backend Architecture

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI main application
│   ├── config.py          # Application settings & environment configuration
│   ├── database.py        # SQLAlchemy engine & SessionLocal management
│   ├── dependencies.py    # Common FastAPI dependency injections
│   │
│   ├── core/              # Security, exceptions, logging, and constants
│   │   ├── __init__.py
│   │   ├── security.py
│   │   ├── exceptions.py
│   │   ├── logging.py
│   │   └── constants.py
│   │
│   ├── api/               # API Router and versioned v1 routes
│   │   ├── __init__.py
│   │   ├── router.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py
│   │       ├── reports.py
│   │       ├── hotspots.py
│   │       ├── tasks.py
│   │       ├── crews.py
│   │       ├── vehicles.py
│   │       ├── dashboard.py
│   │       └── users.py
│   │
│   ├── models/            # SQLAlchemy database entities
│   ├── schemas/           # Pydantic data schemas
│   ├── services/          # Business logic implementations
│   ├── repositories/      # Data access layer
│   ├── ai/                # AI/ML modules
│   └── utils/             # Helper tools
│
├── tests/                 # Unit & API route test cases
└── README.md
```

---

## 🏃 Running the Backend Locally

```bash
# Set PYTHONPATH to project root or backend
cd backend
uvicorn app.main:app --reload --port 8000
```
