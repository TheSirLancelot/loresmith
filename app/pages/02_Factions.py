from app.db.migrations import get_session
from app.db.schema import Faction
import bootstrap  # noqa: F401
import streamlit as st
from app.components.layout import page_header

import logging

page_header("Factions", "Track power structures in your world.")

if "edit_status" not in st.session_state:
    st.session_state["edit_status"] = False
if "faction_edit_id" not in st.session_state:
    st.session_state["faction_edit_id"] = None

with st.form("new_faction_form", clear_on_submit=True):
    st.subheader("Create New Faction")
    st.write("Name and description are required.")

    name_field = st.text_input("Name")
    description_field = st.text_area("Description")
    submit = st.form_submit_button("Create Faction")

    if submit:
        name = name_field.strip()
        description = description_field.strip()

        # Check if name is empty
        if not name:
            st.error("Name cannot be empty.")
        else:
            try:
                with get_session() as session:
                    session.add(Faction(name=name, description=description))
                    session.commit()

                st.success(f"{name} created!")
            except ValueError:
                pass  # Error message already shown
            except Exception as exc:
                st.error(
                    "Unable to connect to the database. "
                    + "Please check your configuration or try again later."
                )
                logging.getLogger("connection").exception(exc)

st.divider()

st.markdown(
    """
- Create faction profiles
- Assign NPC members
- Define goals and secrets
- Track influence levels
"""
)

st.warning("Database integration not yet connected.")
