# LoreSmith

LoreSmith is a lightweight campaign management tool for tabletop RPG Dungeon Masters. It is built in **Python** using **Streamlit** and developed iteratively using **Agile Scrum practices**.

The goal of LoreSmith is to provide a structured way to manage campaign elements such as NPCs, factions, session logs, relationships, and narrative timelines, while delivering value incrementally through short development sprints.

---

## Features (Planned)

- NPC management (create, view, edit, delete)
- Faction management and character associations
- Session logging and tagging
- Filtering and search
- Relationship visualization
- Campaign timeline view
- Persistent local data storage

---

## Tech Stack

- Python
- Streamlit
- GitHub Projects (Agile backlog and sprint tracking)

---

## Development Approach

LoreSmith is being developed as part of a graduate-level Agile Software Development course. The project follows Scrum practices, including:

- User role modeling
- User stories with acceptance criteria
- Story point estimation (Fibonacci scale)
- Backlog prioritization (quantitative + qualitative)
- Sprint planning and reviews
- Velocity tracking and burndown charts
- Iterative releases

The focus of this project is not only the working software, but also the disciplined application of Agile principles and artifacts.

---

## Status

Active development – Sprint 0 (Setup & Backlog Creation)

# Contributing to LoreSmith

LoreSmith uses a lightweight Git workflow designed to support Agile development while protecting production stability.

## Branch Strategy

### main

- Production branch.
- Streamlit deployment is tied to this branch.
- Always stable and demo-ready.
- Protected: requires Pull Request and 1 approval.

### dev

- Integration branch for the active sprint.
- All completed stories are merged here first.
- Used to test feature integration before release.
- Protected: requires Pull Request and 1 approval.

### feature branches

- All development work occurs on feature branches.
- Branch naming convention:

    feature/<short-description>

    Examples:
    - feature/create-npc
    - feature/edit-npc
    - feature/db-connection

Feature branches are created from `dev`.

---

## Workflow

1. Create a feature branch from `dev`.
2. Implement the story.
3. Open a Pull Request into `dev`.
4. Obtain 1 approval.
5. Merge into `dev`.
6. When the sprint is complete and `dev` is stable:
    - Open a Pull Request from `dev` into `main`.
    - Obtain 1 approval.
    - Merge to release.

---

## Definition of Done

A story may be merged into `dev` only when:

- All acceptance criteria are satisfied.
- Code runs locally without errors.
- Database changes (if applicable) are documented.
- Tasks in the issue are completed.
- Another contributor has reviewed and approved the PR.

Only stable, demo-ready increments are merged from `dev` to `main`.

---

## Commit Guidelines

- Keep commits small and focused.
- Write meaningful commit messages.
- Do not commit secrets or credentials.
- Use Streamlit secrets configuration for sensitive values.

## Pre-Commit Hooks

This repository uses pre-commit hooks to run Ruff checks and formatting before each commit.

Set up once after cloning:

1. Install dependencies:
   `pip install -r requirements.txt`
2. Install hooks:
   `pre-commit install`

Run hooks manually at any time:

`pre-commit run --all-files`

## Supabase Secrets Setup

LoreSmith uses Streamlit secrets for the Supabase Postgres connection string.

1. Create the secrets file:
   `.streamlit/secrets.toml`
2. Add in the required Supabase values

Expected format:

`[supabase]`
`db_url = "postgresql://postgres:[YOUR_DB_PASSWORD]@db.[YOUR_PROJECT_REF].supabase.co:5432/postgres"`

For Streamlit Community Cloud, add the same values in App settings under Secrets.

---

## Sprint Discipline

- No direct commits to `main` or `dev`.
- All work must flow through Pull Requests.
- Scope changes during sprint must be agreed upon before merging.
