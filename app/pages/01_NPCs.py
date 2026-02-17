import bootstrap  # noqa: F401
import streamlit as st
from app.components.layout import page_header

page_header("NPCs", "Create, manage, and explore characters.")

st.subheader("Planned Capabilities")

st.markdown(
    """
- Create and edit NPC records
- Assign faction affiliations
- Track narrative tags
- View relationship graph
"""
)

st.warning("Database integration not yet connected.")
