import bootstrap  # noqa: F401
import streamlit as st
from app.components.layout import page_header

page_header("Relationships", "Define the web between characters.")

st.markdown(
    """
- NPC to NPC connections
- Faction ties
- Hidden alliances
- Conflict tracking
"""
)

st.warning("Graph visualization coming in future sprint.")
