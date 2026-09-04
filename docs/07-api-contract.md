# 07 - API Contract Specifications 📜

All API endpoints reside under `/api/v1`.

## Endpoint Matrix

| Method | Path | Description | Access |
|---|---|---|---|
| `POST` | `/api/v1/auth/login` | Authenticate user & return JWT | Public |
| `GET` | `/api/v1/dashboard/metrics` | Retrieve live operational telemetry | Auth Required |
| `GET` | `/api/v1/reports` | List incident reports | Auth Required |
| `POST` | `/api/v1/reports` | Submit new incident report | Auth Required |
| `GET` | `/api/v1/hotspots` | Fetch AI risk hotspot regions | Auth Required |
| `GET` | `/api/v1/tasks` | List active tasks | Auth Required |
| `GET` | `/api/v1/crews` | List response crews | Auth Required |
| `GET` | `/api/v1/vehicles` | List fleet vehicles | Auth Required |
