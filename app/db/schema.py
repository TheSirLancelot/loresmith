"""Database schema definitions using SQLAlchemy ORM."""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import Column, DateTime, String, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class NPC(Base):
    """Non-player character entity for campaign management."""

    __tablename__ = "npc"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False, server_default=text("''"))
    status = Column(String(50), nullable=False, server_default=text("'active'"))
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        server_default=text("timezone('utc', now())"),
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        server_default=text("timezone('utc', now())"),
        onupdate=lambda: datetime.now(UTC),
    )

    def __repr__(self) -> str:
        return f"<NPC(id={self.id!r}, name={self.name!r}, status={self.status!r})>"
