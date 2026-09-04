# ADR-001: PostgreSQL as Primary Database

## Status
Accepted

## Context
EchoCrew requires relational integrity for user accounts, crew assignments, and audit logs, combined with spatial extension support for geospatial indexing.

## Decision
Adopt PostgreSQL 16 with custom ENUMs and spatial extensions as the primary relational database.

## Consequences
- **Positive**: Native ACID compliance, rich SQL features, custom ENUM support.
- **Negative**: Requires database server instance management.
