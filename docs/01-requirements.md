# 01 - Functional & Non-Functional Requirements 📋

## Functional Requirements
- **FR-1**: Users must be able to log field incident reports with geolocation coordinates and asset descriptions.
- **FR-2**: The backend must execute spatial deduplication when a new report is logged near existing active incidents.
- **FR-3**: Dispatchers must be able to assign tasks to specific crews and assign designated vehicles to crews.
- **FR-4**: Field leads must update task progression status (`pending` -> `in_progress` -> `completed`).
- **FR-5**: Command dashboard must stream metrics and hotspot alerts.

---

## Non-Functional Requirements
- **NFR-1 (Performance)**: Sub-second ( < 200ms ) latency for API queries and spatial radius lookups.
- **NFR-2 (Scalability)**: Support up to 10,000 active concurrent report submissions.
- **NFR-3 (Availability)**: 99.9% uptime target for command dashboard API services.
- **NFR-4 (Security)**: Role-based Access Control (RBAC) across all endpoints with JWT authentication.
