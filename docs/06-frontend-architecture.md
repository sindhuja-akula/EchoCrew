# 06 - Frontend Architecture 💻

## Client Framework & Structural Design
The CleanLoop / EchoCrew frontend is designed as a lightweight, modular Single Page Application (SPA) leveraging modern browser ES Modules (ES6+), HTML5, and CSS3 custom properties. It communicates directly with the database-backed FastAPI backend over `/api/v1`.

### 📂 Directory Structure

```
frontend/
├── index.html             # Application HTML shell with viewport, CSS links & entry script
├── app.js                 # Central Application controller & hash router (#report, #dashboard, etc.)
├── server.js              # Lightweight Node static development HTTP server (Port 3000)
├── package.json           # Frontend package manifest & test runner configuration
├── README.md              # Frontend architecture & usage documentation
├── style.css              # Legacy / fallback root styling rules
│
├── public/                # Static public assets
│
├── src/
│   ├── api/ & services/   # Centralized API service wrappers interfacing with backend /api/v1
│   │   ├── apiClient.js            # Centralized fetch wrapper (JSON & FormData support)
│   │   ├── reportsService.js       # Report submission & query
│   │   ├── workersService.js       # Worker registration, list & status updates
│   │   ├── workOrdersService.js    # Work order creation & list
│   │   ├── assignmentsService.js   # Worker assignment creation & state machine updates
│   │   ├── evidenceService.js      # Photo proof evidence submission & query
│   │   ├── verificationService.js  # Quality verification decision submission
│   │   ├── compensationService.js  # Payout eligibility query & status updates
│   │   ├── collectionService.js    # Waste collection batch management
│   │   ├── auditService.js         # Immutable audit trail query
│   │   └── healthService.js        # Backend health check ping
│   │
│   ├── components/        # Modular UI components
│   │   ├── Navbar.js               # Navigation header, role switcher & live health status pill
│   │   ├── StatusBadge.js          # Color-coded status badge renderer
│   │   ├── ReportForm.js           # Citizen report form (photo capture, GPS, category, volume)
│   │   ├── ReportsView.js          # Garbage reports table with filters & work order dispatch
│   │   ├── SupervisorDashboard.js  # Command telemetry dashboard with aggregate cards
│   │   ├── WorkOrdersView.js       # Work order list & creation modal
│   │   ├── AssignmentsView.js      # Worker assignment list & lifecycle state controls
│   │   ├── VerificationView.js     # Evidence review gallery & Approve/Reject audit decision modal
│   │   ├── CompensationView.js     # Payout eligibility list & status update panel
│   │   ├── CollectionsView.js      # Waste collection batch creation & transport status panel
│   │   ├── AuditView.js            # Filterable system audit log history
│   │   └── WorkerView.js           # Responder mobile portal for job tracking & evidence upload
│   │
│   ├── styles/            # Centralized styling design system
│   │   ├── variables.css           # CSS design tokens (colors, radii, shadows, typography)
│   │   └── main.css                # Component styles, forms, grid cards, tables, badges, modals
│   │
│   └── utils/             # Utility helpers & validation contracts
│       ├── constants.js            # API base URL, waste categories, volume tiers, status maps
│       ├── formatters.js           # Date, coordinate, category & badge formatters
│       └── validation.js           # Photo size/mime validation & coordinate bounds validator
│
└── tests/                 # Unit test suite for validation, formatters, and constants
    ├── app.test.js
    ├── formatters.test.js
    └── validation.test.js
```

---

## Key User Workflows

### 1. Citizen Workflow (`#report` & `#my-reports`)
```
Citizen
  ↓
Open application
  ↓
Capture/Upload Site Photo (validated JPEG/PNG/WEBP <= 10MB)
  ↓
Acquire GPS Location ("Use My Location" via HTML5 Geolocation API)
  ↓
Select Waste Classification Category (Wet, Dry, Electronic, Clothing, Hazardous, Mixed, Other)
  ↓
Select Estimated Volume Tier (Minor, Moderate, Bulk with m³ guidance)
  ↓
Provide Optional Description / Landmark Notes
  ↓
Client-Side Validation -> Submit to Backend (POST /api/v1/reports)
  ↓
Spatial Deduplication Check (20m radius notification if duplicate)
  ↓
Show Confirmation Screen with Report Reference ID & Status Badge
```

### 2. Supervisor / Dispatcher Workflow (`#dashboard`, `#reports`, `#work-orders`, `#assignments`, `#verifications`, `#collections`, `#audit`)
- **Dashboard**: Live telemetry stat cards (Total Reports, Open Orders, Active Assignments, Pending Verifications, Collection Volume, Recent Audit Logs).
- **Work Orders**: Create work order for report; auto-generates primary work unit.
- **Assignments**: Link registered workers to work units; advance lifecycle status (`assigned` -> `accepted` -> `in_progress` -> `completed`).
- **Verifications**: Compare BEFORE/PROGRESS/AFTER evidence photos; Approve or Reject cleanup. Approval automatically creates worker compensation eligibility record.
- **Collections**: Create waste transport batch; track transport status (`collecting` -> `sealed` -> `in_transit` -> `delivered`).
- **Audit Log**: Chronological view of immutable backend-generated audit events.

### 3. Responder / Worker Mobile Workflow (`#worker`)
- Mobile-friendly portal to view assigned jobs.
- Single-click action buttons to accept job, start work, upload evidence photos, and mark job complete.
