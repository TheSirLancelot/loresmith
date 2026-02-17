"""Database schema initialization and migration helpers."""

from __future__ import annotations

import logging

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session, sessionmaker

from app.db.connection import get_connection
from app.db.schema import Base

logger = logging.getLogger(__name__)


def _get_engine_from_connection():
    """Create SQLAlchemy engine bound to cached psycopg connection."""
    conn = get_connection()
    return create_engine("postgresql+psycopg://", creator=lambda: conn)


def setup_schema() -> tuple[bool, str]:
    """
    Create all tables defined in schema.Base if they do not exist.

    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        engine = _get_engine_from_connection()
        inspector = inspect(engine)
        existing_tables = inspector.get_table_names()

        tables_to_create = [
            table for table in Base.metadata.tables.keys() if table not in existing_tables
        ]

        if tables_to_create:
            Base.metadata.create_all(engine)
            msg = f"Created {len(tables_to_create)} table(s): {', '.join(tables_to_create)}"
            logger.info(msg)
            return True, msg

        return True, "All tables already exist."
    except Exception as exc:
        error_msg = f"Schema setup failed: {exc}"
        logger.error(error_msg)
        return False, error_msg


def get_session() -> Session:
    """Get a new SQLAlchemy session bound to the cached connection."""
    engine = _get_engine_from_connection()
    session_factory = sessionmaker(bind=engine)
    return session_factory()
