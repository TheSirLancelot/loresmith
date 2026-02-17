from __future__ import annotations

import psycopg
import streamlit as st


def _get_db_conninfo() -> str:
    if "supabase" in st.secrets and "db_url" in st.secrets["supabase"]:
        return st.secrets["supabase"]["db_url"]

    raise RuntimeError("Missing Supabase database secret. Set supabase.db_url in secrets.")


@st.cache_resource
def get_connection() -> psycopg.Connection:
    conninfo = _get_db_conninfo()
    return psycopg.connect(conninfo=conninfo)


def can_connect() -> tuple[bool, str]:
    try:
        with get_connection().cursor() as cursor:
            cursor.execute("select 1")
            cursor.fetchone()
        return True, "Database connection is healthy."
    except Exception as exc:
        return False, f"Database connection failed: {exc}"
