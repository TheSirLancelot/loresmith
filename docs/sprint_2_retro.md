# Sprint 2 Retrospective

Sprint Start: 01 MAR  
Sprint Review / Retro: 15 MAR  

---

## Sprint Goal

Expand NPC functionality and introduce campaign locations as a new core entity within the system.

---

## What We Committed

- Add NPC Stat Block (5)  
- Add NPC Image (5)  
- Create Location (3)  
- View Locations (2)  
- Edit Locations (3)  
- Delete Location (2)  

Total Commitment: **20 Story Points**

---

## What We Completed

All committed stories were completed, with one item (NPC Stat Block) entering review at the end of the sprint and expected to be merged shortly after.

- Add NPC Image  
- Create Location  
- View Locations  
- Edit Locations  
- Delete Location  
- Add NPC Stat Block (in review)

Total Completed: **~18–20 Story Points**

**Sprint Velocity: ~19**

---

## Sprint Outcome

Sprint 2 successfully expanded the LoreSmith application beyond basic NPC management by introducing richer NPC detail and a second core entity: locations.

NPC entries now support both images and stat blocks, significantly improving their usefulness at the table. Additionally, the application now supports full CRUD operations for locations, establishing a foundation for organizing campaign world data.

This sprint validated the system’s ability to scale to multiple entity types and confirmed that the current architecture can support additional feature layers without major refactoring.

---

## What Went Well

- The existing architecture cleanly supported adding a new entity (locations) without significant rework.  
- NPC enhancements (images and stat blocks) integrated smoothly into the existing UI.  
- Development flow improved compared to Sprint 1, with fewer infrastructure-related blockers.  
- Story sizing was generally accurate, with most work aligning well to estimates.

---

## What Did Not Go Well

- The NPC stat block feature extended later into the sprint than expected and did not fully complete before review.  
- Some UI polish and edge cases were again identified late in the sprint.  
- Minor friction still exists around coordinating feature completion and PR review timing.

---

## Root Causes

- The stat block feature had more complexity than initially anticipated due to flexibility requirements (system-agnostic design).  
- UI issues continue to surface primarily during final integration and testing rather than earlier in development.  
- PR review timing is still slightly reactive instead of being planned earlier in the sprint.

---

## Customer Feedback from Sprint Review

During the Sprint 2 demo, the customer responded positively to the increased depth of NPCs and the addition of locations. Several new feature ideas were identified:

### Factions System
- Introduce factions as a core campaign entity.  
- NPCs should be assignable to one or more factions.  
- Users should be able to view faction membership.

### Filtering and Organization
- Ability to filter NPCs by faction.  
- Ability to sort NPC lists for easier navigation.

### Session Tracking
- Add session logs to track campaign progression.  
- Ability to associate NPCs with specific sessions.  
- Future enhancement: search across sessions.

### Future Visualization
- Interest in eventually visualizing relationships between entities (NPCs, factions, locations).  
- Map visualization remains a longer-term goal.

These items have been added to the backlog and prioritized for upcoming sprints.

---

## One Improvement for Next Sprint

Pull PR review and integration earlier into the sprint timeline to avoid end-of-sprint bottlenecks.

---

## Overall Sprint Assessment

The Sprint Goal was achieved. Sprint 2 delivered meaningful user-facing improvements and successfully expanded the system to support multiple entity types.

The team demonstrated improved execution compared to Sprint 1, with fewer setup issues and more predictable delivery.

Velocity remains consistent at approximately **18–20 story points**, providing a reliable baseline for Sprint 3 planning.