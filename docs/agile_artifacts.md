# LoreSmith – Agile Artifacts

## Project Objective

LoreSmith is a lightweight campaign management tool for tabletop RPG Dungeon Masters. The goal is to provide structured management of NPCs, factions, session logs, and narrative relationships through incremental, Agile-driven development.

---

## Definition of Done (DoD)

A user story is considered **Done** when:

1. Code is implemented and committed to the main branch.
2. The application runs without errors.
3. All acceptance criteria for the story are satisfied.
4. Data persists correctly between application restarts.
5. Code has been reviewed by the other developer.
6. The feature is demonstrable during Sprint Review.
7. No known critical defects remain.

Stories may not be moved to “Done” unless all criteria above are met.

## User Role Modeling

During initial project envisioning, several potential user roles were considered:

- **Dungeon Master (DM)** – Primary content creator and campaign organizer
- **Player** – Consumer of session summaries and character information
- **Co-Dungeon Master** – Collaborative campaign manager
- **Campaign Viewer (Read-Only)** – Observer with limited interaction

Given the limited scope of a single-semester project, the decision was made to focus primarily on the **Dungeon Master role**, as this role derives the most direct value from campaign organization tools.

The **Player role** may receive limited read-only capabilities in later iterations if capacity allows. Other roles were intentionally deferred to reduce complexity and maintain focus on delivering a functional MVP within the semester timeline.

This scoping decision supports incremental delivery and prioritization of core value.

## Estimation Approach

LoreSmith user stories are estimated using story points on a Fibonacci scale (1, 2, 3, 5, 8, 13). Estimates reflect relative effort and uncertainty rather than time. The baseline story for anchoring estimates is **Create NPC (3 points)**. All other stories were estimated relative to this baseline, considering UI changes, database interactions, and overall complexity.

## Prioritization Approach

LoreSmith user stories are prioritized using a quantitative 1–10 Business Value scale. Higher values represent greater impact to the primary user (Dungeon Master) and greater contribution to the MVP.

Core CRUD functionality and hosted data persistence were prioritized highest, as they represent mandatory system capabilities. Visualization features were prioritized lower, as they provide enhanced insight but are not required for basic operation.

Qualitatively, Kano analysis was applied:

- Mandatory: Core CRUD, Persistence
- Linear: Factions, Sessions, Search
- Exciters: Visualization features
