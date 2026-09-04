============================================================
CLEANLOOP / ECHOCREW
AI DEVELOPMENT AND DOCUMENTATION RULES
============================================================

STATUS:
MANDATORY

This document defines the mandatory workflow that every AI
coding agent must follow when modifying this repository.

The AI must treat the repository documentation as the
persistent source of truth.

AI conversation history must NEVER be treated as the only
source of project state.

------------------------------------------------------------
1. BEFORE STARTING ANY TASK
------------------------------------------------------------

Before making any change:

1. Read:
   - README.md
   - docs/PROJECT_STATE.md
   - the relevant architecture/documentation files

2. Inspect the existing implementation relevant to the task.

3. Determine:
   - current project phase
   - current implementation status
   - existing dependencies
   - existing architecture
   - existing related files
   - known issues

4. Do not assume that planned functionality is implemented.

5. Clearly distinguish between:
   - PLANNED
   - IN PROGRESS
   - IMPLEMENTED
   - VERIFIED
   - BLOCKED
   - DEPRECATED

6. Do not overwrite existing implementation blindly.

7. Do not introduce a new architecture merely because it is
   easier to implement.

------------------------------------------------------------
2. SCOPE CONTROL
------------------------------------------------------------

Only implement the task currently requested.

Do not independently introduce unrelated:

- frameworks
- libraries
- databases
- services
- microservices
- AI providers
- infrastructure
- APIs
- features

unless explicitly required by the approved architecture.

If a requested implementation conflicts with the existing
architecture:

STOP.

Explain the conflict and ask for approval before changing
architecture.

------------------------------------------------------------
3. AFTER EVERY MEANINGFUL CHANGE
------------------------------------------------------------

After completing every meaningful logical change, the AI MUST
update the appropriate documentation.

At minimum:

docs/PROJECT_STATE.md

must be updated.

The AI must not finish a task while leaving project state
outdated.

------------------------------------------------------------
4. PROJECT_STATE.MD REQUIREMENTS
------------------------------------------------------------

After each meaningful change, update:

docs/PROJECT_STATE.md

The update must include:

A. Current Phase

B. Current Status

C. Completed Work

D. Newly Implemented/Changed Work

E. Files Created

F. Files Modified

G. Files Deleted, if any

H. Dependencies Added/Removed

I. Configuration Changes

J. Database Changes, if applicable

K. API Changes, if applicable

L. Documentation Changes

M. Verification/Test Results

N. Known Issues

O. Remaining Work

P. Immediate Next Step

Do not write vague statements such as:

"Updated backend."

Instead write specifically what changed.

Example:

"Added POST /api/v1/reports endpoint for citizen garbage
report creation with latitude, longitude, image metadata,
and report category validation."

------------------------------------------------------------
5. CHANGE HISTORY
------------------------------------------------------------

Maintain a chronological change history in:

docs/PROJECT_STATE.md

Every meaningful milestone must record:

Date
Phase
Change
Files Created
Files Modified
Reason
Verification
Status

Example:

Date: 2026-09-04

Phase:
Phase 0 - Development Environment

Change:
Finalized Docker development environment.

Files Created:
- docker/backend/Dockerfile

Files Modified:
- docker-compose.yml
- requirements.txt
- .env.example
- README.md

Reason:
Standardize the development environment for all team members.

Verification:
docker compose config
docker compose build
docker compose ps

Status:
VERIFIED

------------------------------------------------------------
6. DOCUMENTATION FILE SELECTION
------------------------------------------------------------

Update documentation according to the type of change.

Project state:
docs/PROJECT_STATE.md

Development setup:
docs/12-development-setup.md

Docker/deployment:
docs/11-deployment.md

Database:
docs/04-database-architecture.md

Backend:
docs/05-backend-architecture.md

Frontend:
docs/06-frontend-architecture.md

API:
docs/07-api-contract.md

AI:
docs/08-ai-architecture.md

Security:
docs/09-security.md

Testing:
docs/10-testing.md

Project overview/workflow:
corresponding project documentation under docs/

Do not create duplicate documentation when an appropriate
document already exists.

------------------------------------------------------------
7. README.MD RULE
------------------------------------------------------------

README.md is stable project documentation.

Update README.md when a change affects:

- installation
- setup
- Docker usage
- environment configuration
- project execution
- major project functionality
- major architecture
- developer workflow

Do not unnecessarily modify README.md for every small code
change.

Detailed implementation history belongs in:

docs/PROJECT_STATE.md

------------------------------------------------------------
8. DATABASE CHANGE RULE
------------------------------------------------------------

Whenever database structure changes, update:

docs/04-database-architecture.md
docs/PROJECT_STATE.md

Record:

- new tables
- removed tables
- modified tables
- columns
- relationships
- constraints
- indexes
- spatial fields
- spatial indexes
- migrations

Use the approved migration system.

Never make an undocumented schema change.

------------------------------------------------------------
9. API CHANGE RULE
------------------------------------------------------------

Whenever an API endpoint is:

- created
- modified
- deleted

update:

docs/07-api-contract.md
docs/PROJECT_STATE.md

Also update:

- request schemas
- response schemas
- validation
- tests

Record:

- endpoint
- HTTP method
- authentication requirement
- request structure
- response structure
- errors
- status codes

------------------------------------------------------------
10. BACKEND CHANGE RULE
------------------------------------------------------------

Whenever backend architecture or implementation changes:

Update the relevant backend documentation and:

docs/PROJECT_STATE.md

Record important:

- modules
- services
- dependencies
- database interactions
- authentication
- authorization
- background processing
- external integrations

------------------------------------------------------------
11. FRONTEND CHANGE RULE
------------------------------------------------------------

Whenever frontend architecture or major functionality changes:

Update:

docs/06-frontend-architecture.md
docs/PROJECT_STATE.md

Record:

- pages
- dashboards
- components
- state management
- API integrations
- authentication flow
- important UI workflows

------------------------------------------------------------
12. AI CHANGE RULE
------------------------------------------------------------

Whenever AI functionality changes:

Update:

docs/08-ai-architecture.md
docs/PROJECT_STATE.md

Record:

- AI task
- input
- output
- model/provider
- fallback behavior
- confidence handling
- limitations
- verification strategy

Never describe an AI capability as production-ready if it
has only been mocked or prototyped.

------------------------------------------------------------
13. DOCKER CHANGE RULE
------------------------------------------------------------

Whenever any Docker-related file changes:

- docker-compose.yml
- Dockerfile
- .dockerignore
- Docker configuration
- container environment configuration

the AI MUST:

1. Validate Docker configuration.

2. Build affected containers.

3. Start the affected services where possible.

4. Check container status.

5. Inspect relevant logs if required.

6. Record the verification result in:

docs/PROJECT_STATE.md

If Docker was not successfully tested, explicitly write:

NOT VERIFIED

Do not claim Docker is working merely because configuration
files look correct.

------------------------------------------------------------
14. REQUIREMENTS.TXT RULE
------------------------------------------------------------

Whenever a dependency is added or removed:

Update:

requirements.txt

or:

requirements-dev.txt

as appropriate.

Then update:

docs/PROJECT_STATE.md

Record:

- package name
- version constraint if applicable
- reason
- whether runtime or development dependency
- verification result

Do not add unnecessary dependencies.

------------------------------------------------------------
15. ENVIRONMENT CONFIGURATION RULE
------------------------------------------------------------

When environment variables change:

Update:

.env.example

and relevant documentation.

NEVER commit:

.env

NEVER place real secrets in:

.env.example

Use safe placeholders.

Record environment variable changes in:

docs/PROJECT_STATE.md

------------------------------------------------------------
16. TESTING RULE
------------------------------------------------------------

After implementing functionality, run the appropriate tests.

Examples:

- unit tests
- integration tests
- API tests
- database tests
- Docker verification
- frontend tests
- manual verification

Only mark:

VERIFIED

when verification was actually performed.

If testing could not be performed:

Status:
IMPLEMENTED - NOT VERIFIED

Explain why.

Never fabricate test results.

------------------------------------------------------------
17. FILE CHANGE REVIEW
------------------------------------------------------------

Before considering a task complete:

Run/check equivalent of:

git status

and:

git diff

Review every changed file.

Ensure:

- no unrelated files changed
- no secrets were added
- no accidental deletions occurred
- no unnecessary dependencies were added
- documentation reflects the implementation
- PROJECT_STATE.md is updated

------------------------------------------------------------
18. GIT RULE
------------------------------------------------------------

After every meaningful completed milestone:

1. Update documentation.
2. Verify functionality.
3. Review changes.
4. Create a logical Git commit.

Example:

chore: finalize docker development environment

feat: add garbage report model

feat: add spatial report clustering

feat: add report creation API

test: add report verification tests

Do not create meaningless commits for individual lines.

Commit logical milestones.

------------------------------------------------------------
19. PARTIAL IMPLEMENTATION RULE
------------------------------------------------------------

If a task cannot be fully completed:

DO NOT mark it complete.

Update:

docs/PROJECT_STATE.md

with:

Status:
IN PROGRESS

Record:

- what was completed
- what remains
- why it remains
- errors encountered
- immediate next step

This is mandatory because another developer or AI agent
must be able to continue from the repository.

------------------------------------------------------------
20. ERROR HANDLING
------------------------------------------------------------

If an error occurs:

DO NOT randomly modify multiple files.

Instead:

1. Identify the failing component.
2. Read the error.
3. Inspect relevant logs.
4. Identify the likely root cause.
5. Make the smallest appropriate change.
6. Test again.
7. Document the result.

Record unresolved errors under:

Known Issues

in:

docs/PROJECT_STATE.md

------------------------------------------------------------
21. ARCHITECTURE CHANGE RULE
------------------------------------------------------------

Do not change major architecture without explicit approval.

Examples:

- changing database technology
- adding/removing major infrastructure
- changing authentication architecture
- converting monolith to microservices
- adding message queues
- changing storage architecture
- replacing the AI architecture

If such a change appears necessary:

STOP.

Explain:

1. Current architecture
2. Problem
3. Proposed change
4. Benefits
5. Risks
6. Files affected

Wait for approval.

------------------------------------------------------------
22. END-OF-TASK CHECKLIST
------------------------------------------------------------

Before responding that a task is complete, the AI MUST verify:

[ ] Existing implementation inspected
[ ] Requested change implemented
[ ] Relevant tests executed
[ ] Docker verified if affected
[ ] Database verified if affected
[ ] API verified if affected
[ ] requirements.txt updated if required
[ ] .env.example updated if required
[ ] Relevant architecture documentation updated
[ ] README.md updated if required
[ ] docs/PROJECT_STATE.md updated
[ ] Known issues documented
[ ] Immediate next step documented
[ ] git diff reviewed
[ ] No secrets included
[ ] No unrelated files modified

------------------------------------------------------------
23. FINAL RESPONSE FORMAT FOR AI AGENT
------------------------------------------------------------

At the end of every task, report:

1. TASK COMPLETED

2. CHANGES MADE
   - file
   - change

3. DOCUMENTATION UPDATED
   - file
   - what was documented

4. VERIFICATION
   - exact tests/commands performed
   - result

5. CURRENT STATUS
   - VERIFIED
   - IMPLEMENTED
   - IN PROGRESS
   - BLOCKED
   - etc.

6. KNOWN ISSUES

7. IMMEDIATE NEXT STEP

Do not simply say:

"Done."

------------------------------------------------------------
24. PROJECT STATE IS THE SOURCE OF TRUTH
------------------------------------------------------------

The repository must always be capable of answering:

What has been completed?

What is currently being developed?

What changed recently?

What files were affected?

What was actually tested?

What is not verified?

What problems remain?

What should be done next?

The primary source for this information is:

docs/PROJECT_STATE.md

------------------------------------------------------------
25. NO CONVERSATION-DEPENDENT STATE
------------------------------------------------------------

The project must never depend on the AI remembering previous
conversation messages.

If a new AI session starts tomorrow, next week, or from
another account, it must be possible to understand the
current project state by reading the repository.

Therefore:

DOCUMENT THE WORK.

DO NOT RELY ON MEMORY.

============================================================
END OF MANDATORY AI DEVELOPMENT RULES
============================================================
