# ADR-002: Monorepo with Decoupled FastAPI and Frontend Services

## Status
Accepted

## Context
Clear separation of API logic from UI presentation is necessary to enable multi-client support (web client, mobile client, emergency dispatch consoles).

## Decision
Organize backend (`FastAPI`) and frontend independently inside a structured monorepo.

## Consequences
- **Positive**: Clean interface boundaries via `/api/v1` routes.
- **Negative**: Requires handling CORS headers and client-side error states.
