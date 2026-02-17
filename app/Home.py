import bootstrap  # noqa: F401
import streamlit as st
from app.components.layout import page_header
from app.db.connection import can_connect
from app.db.migrations import setup_schema

st.set_page_config(
    page_title="LoreSmith",
    page_icon="📜",
    layout="wide",
)

page_header("LoreSmith", "Campaign management for serious storytellers.")

is_connected, status_msg = can_connect()
if is_connected:
    st.success(status_msg)
    schema_ok, schema_msg = setup_schema()
    if schema_ok:
        st.info(f"Schema: {schema_msg}")
    else:
        st.warning(f"Schema: {schema_msg}")
else:
    st.error(status_msg)

st.markdown(
    """
    ### Sprint 0 Status

    The application skeleton is live.

    Planned core modules:
    - NPC Management
    - Faction Tracking
    - Session Logs
    - Narrative Relationships

    Database integration coming next.
    """
)

st.info("Select a module from the sidebar to begin.")
