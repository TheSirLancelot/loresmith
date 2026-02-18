"""Seed script for populating test data into the database."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone

from app.db.migrations import get_session
from app.db.schema import NPC


def seed_test_npcs() -> None:
    """Insert sample NPCs for testing and development."""
    session = get_session()

    test_npcs = [
        NPC(
            id=uuid.uuid4(),
            name="Aldric the Wise",
            description="An elderly wizard who serves as the kingdom's chief advisor.",
            status="active",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        ),
        NPC(
            id=uuid.uuid4(),
            name="Lyra Shadowblade",
            description="A skilled rogue with a mysterious past and hidden loyalties.",
            status="active",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        ),
        NPC(
            id=uuid.uuid4(),
            name="Brother Thorne",
            description="A holy priest devoted to spreading light and righteousness.",
            status="active",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        ),
        NPC(
            id=uuid.uuid4(),
            name="Mira Stoneheart",
            description="A dwarf warrior renowned for her strength and honor.",
            status="active",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        ),
        NPC(
            id=uuid.uuid4(),
            name="Lord Vex",
            description="A dangerous noble with ambitions that threaten the realm.",
            status="active",
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        ),
    ]

    try:
        session.add_all(test_npcs)
        session.commit()
        print(f"Successfully inserted {len(test_npcs)} test NPCs.")
    except Exception as exc:
        session.rollback()
        print(f"Failed to insert test data: {exc}")
    finally:
        session.close()


if __name__ == "__main__":
    seed_test_npcs()
