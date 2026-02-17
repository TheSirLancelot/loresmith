import bootstrap  # noqa: F401
import streamlit as st
from app.components.layout import page_header

page_header("Sessions", "Record events and evolving story arcs.")

st.markdown(
    """
- Session summaries
- Timeline view
- Event tagging
- Cross reference NPC involvement
"""
)

st.warning("Database integration not yet connected.")
