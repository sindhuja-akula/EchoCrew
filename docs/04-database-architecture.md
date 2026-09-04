# 04 - Database Architecture 🗄️

## Data Storage Strategy
EchoCrew utilizes PostgreSQL 16 as its relational engine.

### Schema Organization
- **`enums.sql`**: Custom domain types (`user_role`, `task_status`, `risk_level`, `vehicle_status`).
- **`extensions.sql`**: Enabling `uuid-ossp`, `pg_trgm`, and spatial capabilities.
- **`indexes.sql`**: B-Tree and GIST spatial indexes for fast geolocation querying.

### Key Entities
- `users`: Administrative commanders, dispatchers, crew leads.
- `crews`: Response teams and assigned personnel.
- `vehicles`: Fleet vehicles assigned to active crews.
- `reports`: Incoming incident entries.
- `tasks`: Actionable tickets derived from validated reports.
