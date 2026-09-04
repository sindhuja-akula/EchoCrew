# 03 - System Architecture 🏗️

```
                         ┌───────────────────────┐
                         │   Web / Mobile UI     │
                         └───────────┬───────────┘
                                     │ HTTP / REST
                                     ▼
                         ┌───────────────────────┐
                         │   FastAPI Backend     │
                         └───────┬───────┬───────┘
                                 │       │
              ┌──────────────────┘       └──────────────────┐
              ▼                                             ▼
   ┌────────────────────┐                        ┌────────────────────┐
   │ PostgreSQL DB      │                        │ MinIO S3 Storage   │
   │ (Schemas & Enums)  │                        │ (Media / Attachments)
   └────────────────────┘                        └────────────────────┘
```

## Modular System Layers
- **Presentation Layer**: Client Web Dashboard.
- **Application Layer**: FastAPI application hosting REST endpoints `/api/v1/*`.
- **Persistence Layer**: PostgreSQL database with custom ENUMs, spatial indexes, and schemas.
- **Object Storage Layer**: MinIO S3 instance for local attachment storage.
