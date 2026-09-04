# ADR-004: Spatial Buffer Incident Deduplication

## Status
Accepted

## Context
During major incidents, multiple citizens report the same emergency in close proximity, flooding dispatch queues with redundant tickets.

## Decision
Implement a 500-meter geospatial radius buffer to automatically flag and group duplicate incoming reports.

## Consequences
- **Positive**: Significantly reduces ticket clutter for dispatchers.
