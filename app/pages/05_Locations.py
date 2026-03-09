import bootstrap  # noqa: F401
import streamlit as st
import logging
from app.components.layout import page_header
from app.db.migrations import get_session
from app.db.schema import Location
from sqlalchemy import select

page_header("Locations", "Create, manage, and explore locations.")

if "location_edit_status" not in st.session_state:
    st.session_state["location_edit_status"] = False
if "location_edit_id" not in st.session_state:
    st.session_state["location_edit_id"] = None

with st.form("new_location_form", clear_on_submit=True):
    st.subheader("Create New Location")
    st.write("Name is required. Description is optional.")

    name_field = st.text_input("Name")
    description_field = st.text_area("Description")
    submit = st.form_submit_button("Create location")

    if submit:
        name = name_field.strip()
        description = description_field.strip()

        # Check if name is empty
        if not name:
            st.error("Name cannot be empty.")
        else:
            try:
                with get_session() as session:
                    session.add(Location(name=name, description=description))
                    session.commit()

                st.success(f"{name} created!")
            except Exception as exc:
                st.error(
                    "Unable to connect to the database. "
                    + "Please check your configuration or try again later."
                )
                logging.getLogger("connection").exception(exc)

st.divider()


st.subheader("Planned Capabilities")

st.markdown(
    """
- Create and edit location records
- Track narrative tags
- View relationship graph
"""
)
