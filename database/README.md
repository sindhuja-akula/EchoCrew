# EchoCrew Database Module 🗄️

Modular PostgreSQL database setup containing migrations, core schemas (extensions, custom enums, indexes), seed data, and administration scripts.

---

## 📂 Directory Structure

```
database/
│
├── migrations/
│   └── versions/       # Alembic/SQL database migration versions
│
├── schema/
│   ├── enums.sql       # Custom PostgreSQL ENUM types
│   ├── extensions.sql  # Database extension activations (uuid, pg_trgm)
│   └── indexes.sql     # Database performance B-Tree indexes
│
├── seeds/
│   ├── users.sql       # Initial user seed data
│   ├── crews.sql       # Initial crews seed data
│   ├── vehicles.sql    # Fleet vehicle seed data
│   └── demo_data.sql   # Demo logs & incident data
│
├── scripts/
│   ├── init_db.sql     # Master database initialization script
│   └── reset_db.sql    # Schema wipe & reset script
│
└── README.md           # Database documentation
```

---

## 🛠️ Usage & Operations

### Initialize Database
Execute `init_db.sql` via `psql`:

```bash
psql -U echocrew -d echocrew_db -f database/scripts/init_db.sql
```

### Reset Database Schema
Execute `reset_db.sql` to clean the database:

```bash
psql -U echocrew -d echocrew_db -f database/scripts/reset_db.sql
```
