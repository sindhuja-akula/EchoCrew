# ADR-005: AI Provider Abstraction Interface

## Status
Accepted

## Context
Predictive AI hotspot clustering models may switch between local inference models and cloud LLM services.

## Decision
Decouple AI services behind a standard python abstract base class interface (`AIProvider`).

## Consequences
- **Positive**: Provider agnostic, allowing seamless model swapping without refactoring API handlers.
