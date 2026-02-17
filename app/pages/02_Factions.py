import bootstrap  # noqa: F401
import streamlit as st
from app.components.layout import page_header

page_header("Factions", "Track power structures in your world.")

st.markdown(
    """
- Create faction profiles
- Assign NPC members
- Define goals and secrets
- Track influence levels
"""
)

st.warning("Database integration not yet connected.")
