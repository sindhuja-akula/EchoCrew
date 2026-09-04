# CleanLoop AI Development Rules 🤖📜

> Mandatory operational rules and governance protocol for any AI coding assistant or developer working on CleanLoop / EchoCrew.

---

## 1. Core Mandate & Source of Truth

1. **Repository-First Knowledge**: The repository itself—specifically `docs/PROJECT_STATE.md`—is the single source of truth for project status, completed work, pending tasks, and architecture.
2. **Never Rely on Session Memory**: Never assume a feature exists or is verified based on conversational context alone. Inspect authoritative source files first.
3. **Recovery & Continuity Guarantee**: The codebase must always remain recoverable, runnable, and understandable if:
   - The AI session ends or hits usage limits.
   - Development is paused for days or transferred to another developer/AI.

---

## 2. Before Making Any Change

Before modifying any file:
- [ ] Inspect existing files and understand current implementations.
- [ ] Check `docs/PROJECT_STATE.md` for current phase and status.
- [ ] Check `README.md` if project setup, running, or configuration is affected.
- [ ] Check relevant architecture specs in `docs/` (`04-database-architecture.md`, `05-backend-architecture.md`, `07-api-contract.md`, etc.).
- [ ] Distinguish clearly between **Planned**, **Implemented**, **Tested**, **Verified**, and **Pending**.
- [ ] **Halt & Report**: If a requested change conflicts with an Architectural Decision Record (ADR), STOP immediately and report the conflict before modifying files.

---

## 3. After Every Change

Immediately after executing a meaningful change:
1. Update `docs/PROJECT_STATE.md`:
   - `Current Phase`
   - `Completed`
   - `Newly Changed`
   - `Verification` (Specify exact test method or mark `NOT VERIFIED` with reasons)
   - `Current Status` (`NOT STARTED`, `IN PROGRESS`, `IMPLEMENTED`, `VERIFIED`, `BLOCKED`, `NEEDS REVIEW`)
   - `Known Issues`
   - `Next Step` (ONLY the immediate next logical step)
2. Add a structured entry to `docs/PROJECT_STATE.md` under `## 📜 File Change Log`:
   ```markdown
   Date: YYYY-MM-DD
   Phase: <Phase Name>
   Change: <Brief description>
   Files Modified:
   - path/to/file1
   - path/to/file2
   Reason: <Technical justification>
   Verification: <Exact verification output>
   Status: <Status>
   ```

---

## 4. Specific Domain Rules

### A. Docker Change Rule
Whenever modifying `docker-compose.yml`, `Dockerfile`, `.dockerignore`, or container environment settings:
- Validate file syntax.
- Build affected container image(s).
- Start services where practical (`docker compose up`).
- Inspect container health status and logs.
- Record verification outcome in `docs/PROJECT_STATE.md`.

### B. Database Change Rule
Whenever modifying database structures, schemas, or models:
- Update database documentation (`docs/04-database-architecture.md`).
- Create/update appropriate Alembic migrations under `backend/alembic/versions/`.
- Never alter production-style schemas manually without a migration.
- Test and verify resulting schema.
- Record tables, columns, indexes, and constraints in `docs/PROJECT_STATE.md`.

### C. API Change Rule
Whenever adding, modifying, or removing API routes:
- Update API contract documentation (`docs/07-api-contract.md`).
- Update Pydantic request/response schemas.
- Write/update corresponding unit/integration tests in `backend/tests/`.
- Record route changes in `docs/PROJECT_STATE.md`.

### D. Requirements & Dependencies Rule
Whenever adding new Python or system dependencies:
- Verify genuine necessity (avoid unnecessary bloat).
- Add runtime dependencies to `requirements.txt`.
- Add dev/test dependencies to `requirements-dev.txt`.
- Record justification in `docs/PROJECT_STATE.md`.
- Rebuild Docker backend container to verify build.

---

## 5. Security & Secrets Protection

- **NEVER Commit Secrets**: `.env`, passwords, private API keys, JWT secrets, cloud credentials, database passwords, or private tokens must NEVER be committed to Git.
- **Safe Templates Only**: Maintain safe placeholder values in `.env.example`.
- **Git Auditing**: Ensure `.env` is listed in `.gitignore` and `.dockerignore`.
- **Immediate Halt**: If a secret is accidentally staged, STOP immediately and purge it before committing.

---

## 6. Scope Control & No Unauthorized Expansion

- Implement ONLY the explicitly approved phase and scope.
- Do NOT introduce unapproved technologies (e.g., Redis, Kafka, Celery, Kubernetes, unauthorized AI providers) unless explicitly mandated by an approved ADR.
- Keep CleanLoop modular, minimal, and maintainable.

---

## 7. Task Finalization Checklist

Before marking any task as complete:
- [ ] Review changed files via `git status` and `git diff`.
- [ ] Execute appropriate verification tests.
- [ ] Update `docs/PROJECT_STATE.md` (and `README.md` / `docs/` if applicable).
- [ ] Audit for accidental secrets.
- [ ] Commit with conventional commit messages (`feat:`, `fix:`, `docs:`, `chore:`, `test:`).
- [ ] Push changes to GitHub repository.
- [ ] Report: exact changes, verifications performed, known problems, and immediate next step.
