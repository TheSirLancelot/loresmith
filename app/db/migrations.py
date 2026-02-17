"""Database schema initialization and migration helpers."""

from __future__ import annotations

import logging

import psycopg
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session, sessionmaker

from app.db.connection import _get_db_conninfo
from app.db.schema import Base

logger = logging.getLogger(__name__)


def _get_engine_from_connection():
    """
    Create SQLAlchemy engine that opens fresh psycopg connections on demand.

    The creator callable produces new connections, allowing SQLAlchemy to
    manage pooling and connection lifecycle properly.
    """

    def creator():
        return psycopg.connect(conninfo=_get_db_conninfo())

    return create_engine("postgresql+psycopg://", creator=creator)


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
    except Exception:
        logger.exception("Schema setup failed during schema initialization.")
        user_msg = "Schema setup failed. Please check server logs for details."
        return False, user_msg


def get_session() -> Session:
    """Get a new SQLAlchemy session bound to the cached connection."""
    engine = _get_engine_from_connection()
    session_factory = sessionmaker(bind=engine)
    return session_factory()
