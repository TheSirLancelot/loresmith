from __future__ import annotations

import logging

import psycopg
import streamlit as st

logger = logging.getLogger(__name__)


def _get_db_conninfo() -> str:
    if "supabase" in st.secrets and "db_url" in st.secrets["supabase"]:
        return st.secrets["supabase"]["db_url"]

    raise RuntimeError("Missing Supabase database secret. Set supabase.db_url in secrets.")


@st.cache_resource
def get_connection() -> psycopg.Connection:
    conninfo = _get_db_conninfo()
    return psycopg.connect(conninfo=conninfo)


def can_connect() -> tuple[bool, str]:
    """
    Check if database is reachable.

    Uses a fresh, short-lived connection to avoid polluting the cached
    connection's transaction state.

    Returns:
        Tuple of (success: bool, message: str)
    """
    try:
        conninfo = _get_db_conninfo()
        with psycopg.connect(conninfo=conninfo) as conn:
            with conn.cursor() as cursor:
                cursor.execute("select 1")
                cursor.fetchone()
        return True, "Database connection is healthy."
    except Exception:
        logger.exception("Database connection check failed.")
        return False, "Database connection failed. Please check server logs for details."
