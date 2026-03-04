# Sprint 1 Retrospective

Sprint Start: 18 FEB  
Sprint Review / Retro: 01 MAR

---

## Sprint Goal

Deliver a functional MVP allowing Dungeon Masters to create, view, edit, and delete NPCs with persistent hosted storage.

---

## What We Committed

- Persist Data in Hosted Database (8)
- Create NPC (3)
- View NPC List (2)
- Edit NPC (3)
- Delete NPC (2)

Total Commitment: **18 Story Points**

---

## What We Completed

All committed stories were successfully completed during the sprint:

- Persist Data in Hosted Database
- Create NPC
- View NPC List
- Edit NPC
- Delete NPC

Additionally, several small bug fixes were completed toward the end of the sprint to improve stability and user experience.

Total Completed: **18 Story Points**

**Sprint Velocity: 18**

---

## Sprint Outcome

Sprint 1 successfully delivered the first functional vertical slice of the LoreSmith application. Users can now create, view, edit, and delete NPC entries, with all data persisted in the hosted PostgreSQL database.

This validated the core application architecture, database integration, and deployment workflow.

---

## What Went Well

- The initial architecture proved flexible enough to support CRUD functionality without major refactoring.
- The database integration with Supabase worked reliably once configured.
- Pull request workflow and protected branches helped ensure stable integration.

---

## What Did Not Go Well

- Some initial time was spent troubleshooting database connection configuration and secrets management.
- A few minor UI issues and bugs were discovered late in the sprint during testing.

---

## Root Causes

- Early infrastructure setup required experimentation with database hosting and environment configuration.
- UI and interaction issues were only fully apparent after the system was integrated and exercised end-to-end.

---

## Customer Feedback from Sprint Review

During the Sprint 1 demo, the customer provided several suggestions for future improvements:

### NPC Images
- NPC entries should support images.
- Possible UI idea: a small icon next to the NPC name that can be clicked to view the image.

### Character Stat Blocks
- NPCs should support an optional stat block.
- The system must remain system-agnostic, so the stat block should support flexible fields rather than a specific ruleset.

### Multi-Faction Membership
- When factions are implemented, NPCs must be able to belong to **multiple factions**, not just one.

### Locations System
- Add a **Locations** section to the sidebar.
- Locations should contain:
  - associated NPCs
  - associated factions
  - map references
- Future enhancement: map visualization showing where NPCs are located.

These ideas will be converted into new user stories and added to the product backlog for prioritization and estimation.

---

## One Improvement for Next Sprint

Improve early UI validation and testing earlier in the sprint to catch interaction issues sooner.

---

## Overall Sprint Assessment

The Sprint Goal was fully achieved. The team successfully delivered the first usable version of the application and established a working development workflow.

Confidence moving into Sprint 2 is high, with a validated architecture and an initial measured velocity of **18 story points per sprint**.