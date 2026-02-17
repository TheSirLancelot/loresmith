"""Database schema definitions using SQLAlchemy ORM."""

from __future__ import annotations

from datetime import datetime

from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class NPC(Base):
    """Non-player character entity for campaign management."""

    __tablename__ = "npc"

    id = Column(String(36), primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, default="")
    status = Column(String(50), nullable=False, default="active")
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<NPC(id={self.id!r}, name={self.name!r}, status={self.status!r})>"
