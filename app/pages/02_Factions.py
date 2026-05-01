from app.db.migrations import get_session
from app.db.schema import Faction
import bootstrap  # noqa: F401
import streamlit as st
from app.components.layout import page_header

import logging
from sqlalchemy import select

page_header("Factions", "Track power structures in your world.")

if "edit_status" not in st.session_state:
    st.session_state["edit_status"] = False
if "faction_edit_id" not in st.session_state:
    st.session_state["faction_edit_id"] = None

with st.form("new_faction_form", clear_on_submit=True):
    st.subheader("Create New Faction")
    st.write("Name is required. Description is optional.")

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

try:
    with get_session() as session:
        records = session.execute(select(Faction).order_by(Faction.name)).scalars().all()

        if not records:
            st.info("No factions found in the database.")
        else:
            for item in records:
                if f"faction_edit_{item.id}" not in st.session_state:
                    st.session_state[f"faction_edit_{item.id}"] = False

                if st.session_state[f"faction_edit_{item.id}"]:
                    item.as_edit_expander(session)
                else:
                    item.as_expander(session)
except Exception as exc:
    st.error(
        "Unable to connect to the database. Please check your configuration or try again later."
    )
    logging.getLogger("connection").exception(exc)

st.markdown(
    """
- Create faction profiles
- Assign NPC members
- Define goals and secrets
- Track influence levels
"""
)
