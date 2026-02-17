import bootstrap  # noqa: F401
import streamlit as st
from app.components.layout import page_header

st.set_page_config(
    page_title="LoreSmith",
    page_icon="📜",
    layout="wide",
)

page_header("LoreSmith", "Campaign management for serious storytellers.")

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
