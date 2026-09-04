# 05 - Backend Architecture ⚙️

## Framework & Structural Patterns
The backend is built with FastAPI and Python 3.11 following Clean Architecture principles:

- **Router Layer** (`app/api/v1/`): Request routing, input validation via Pydantic schemas.
- **Service Layer** (`app/services/`): Business logic, task calculation, and AI model orchestration.
- **Repository Layer** (`app/repositories/`): Abstract data access operations using SQLAlchemy ORM.
- **Core Layer** (`app/core/`): Cross-cutting concerns including security, exceptions, and logging.
