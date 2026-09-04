# 02 - System Workflow 🔄

```
[ Field Responder / Citizen ]
         │
         ▼
[ Submit Incident Report ] ──► [ Spatial Deduplication Check ]
                                       │
                         ┌─────────────┴─────────────┐
                         ▼                           ▼
                 [ Duplicate Found ]         [ New Incident Created ]
                         │                           │
                   [ Append Report ]           [ AI Risk Assessment ]
                                                     │
                                                     ▼
                                            [ Generate Task Ticket ]
                                                     │
                                                     ▼
                                            [ Assign Crew & Vehicle ]
                                                     │
                                                     ▼
                                            [ Field Execution & Completion ]
```

## Workflow Lifecycle
1. **Ingestion**: Incident reports captured via API endpoint.
2. **Deduplication**: Radius buffering and similarity scoring.
3. **Dispatch**: Dispatcher assigns task to designated response crew.
4. **Resolution**: Crew lead updates task state; telemetry logs system status.
