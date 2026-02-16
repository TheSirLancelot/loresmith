# LoreSmith – Agile Artifacts

## Project Objective

LoreSmith is a lightweight campaign management tool for tabletop RPG Dungeon Masters. The goal is to provide structured management of NPCs, factions, session logs, and narrative relationships through incremental, Agile-driven development using Scrum principles.

The project emphasizes vertical slicing, continuous integration, and empirical feedback to iteratively deliver a functional MVP.

---

## Scrum Framework Usage

LoreSmith follows a lightweight Scrum implementation:

- Sprint Length: 2 weeks
- Roles:
    - Product Owner: Defines backlog and prioritization
    - Developers: Implement stories and review code
- Events:
    - Sprint Planning
    - Sprint Retrospective
- Artifacts:
    - Product Backlog (GitHub Issues)
    - Sprint Backlog (GitHub Project Sprint field)
    - Increment (Deployed version from `main`)

---

## Definition of Done (DoD)

A user story is considered **Done** when:

1. Code is implemented on a feature branch.
2. A Pull Request has been approved and merged into `dev`.
3. The application runs without errors in the intended environment.
4. All acceptance criteria for the story are satisfied.
5. Data persistence works correctly if applicable.
6. No hardcoded secrets or credentials exist.
7. Code has been reviewed and approved.
8. The feature is demonstrable in the integrated application.

Only stable increments are merged from `dev` into `main`.

Stories may not be moved to “Done” unless all criteria above are met.

---

## User Role Modeling

During initial project envisioning, several potential user roles were considered:

- Dungeon Master (DM) – Primary content creator and campaign organizer
- Player – Consumer of session summaries and character information
- Co-Dungeon Master – Collaborative campaign manager
- Campaign Viewer (Read-Only) – Observer with limited interaction

Given the limited scope of a single-semester project, the decision was made to focus primarily on the Dungeon Master role, as this role derives the most direct value from campaign organization tools.

The Player role may receive limited read-only capabilities in later iterations if capacity allows. Other roles were intentionally deferred to reduce complexity and maintain focus on delivering a functional MVP.

This scoping decision supports incremental delivery and prioritization of core value.

---

## Estimation Approach

LoreSmith user stories are estimated using story points on a Fibonacci scale (1, 2, 3, 5, 8, 13).

Estimates reflect:

- Relative effort
- Technical complexity
- Uncertainty
- Integration risk

The baseline story for anchoring estimates is **Create NPC (3 points)**. All other stories were estimated relative to this baseline, considering UI changes, database interactions, and architectural complexity.

Story points are used to measure velocity across sprints and guide capacity planning.

---

## Prioritization Approach

LoreSmith user stories are prioritized using a quantitative 1–10 Business Value scale. Higher values represent greater impact to the primary user (Dungeon Master) and greater contribution to MVP functionality.

Backlog ordering considers:

1. Business Value (descending)
2. Story Points (ascending as tie-breaker)

Core CRUD functionality and hosted data persistence were prioritized highest, as they represent mandatory system capabilities.

Visualization features were prioritized lower, as they provide enhanced insight but are not required for baseline functionality.

### Kano Classification

- Mandatory: Core CRUD, Persistence
- Linear: Factions, Sessions, Search
- Exciters: Visualization features

This prioritization ensures early delivery of core value while preserving flexibility for feature expansion.
