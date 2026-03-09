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

try:
    with get_session() as session:
        records = session.execute(select(Location).order_by(Location.name)).scalars().all()

        if not records:
            st.info("No locations found in the database.")
        else:
            if not st.session_state["location_edit_status"]:
                for item in records:
                    with st.expander(f"{item.name}"):
                        st.write(f"Status: {item.status.upper()}")
                        st.write(f"Description: {item.description}")

                        if st.button("Edit", key=f"edit_btn_{item.id}", type="secondary"):
                            st.session_state["location_edit_status"] = True
                            st.session_state["location_edit_id"] = item.id
                            st.rerun()

                        if st.button("Delete", key=f"del_btn_{item.id}", type="primary"):
                            location = (
                                session.query(Location).filter(Location.id == item.id).first()
                            )
                            if location:
                                session.delete(location)
                                session.commit()
                                st.rerun()
            else:
                for item in records:
                    if item.id == st.session_state["location_edit_id"]:
                        with st.expander(f"{item.name}"):
                            # This doubly protects us from None values
                            edit_location_name = st.text_input("Name", value=item.name) or ""
                            edit_location_desc = (
                                st.text_area("Description", value=item.description) or ""
                            )
                            updated_name = edit_location_name.strip()
                            updated_description = edit_location_desc.strip()

                            if st.button("Update", key=f"update_btn_{item.id}", type="secondary"):
                                if not updated_name:
                                    st.error("Name cannot be empty.")
                                else:
                                    try:
                                        location = (
                                            session.query(Location)
                                            .filter(Location.id == item.id)
                                            .first()
                                        )
                                        if location is None:
                                            st.error("This location no longer exists.")
                                            st.session_state["location_edit_status"] = False
                                            st.session_state["location_edit_id"] = None
                                            st.rerun()

                                        location.name = updated_name
                                        location.description = updated_description
                                        session.commit()

                                        st.session_state["location_edit_status"] = False
                                        st.session_state["location_edit_id"] = None

                                        st.rerun()
                                    except Exception as exc:
                                        session.rollback()
                                        st.error(
                                            "Unable to connect to the database. "
                                            + "Please check your configuration or try again later."
                                        )
                                        logging.getLogger("connection").exception(exc)
                            if st.button("Cancel", key="update_cancel_btn", type="secondary"):
                                st.session_state["location_edit_status"] = False
                                st.session_state["location_edit_id"] = None
                                st.rerun()
                    else:
                        with st.expander(f"{item.name}"):
                            st.write(f"Status: {item.status.upper()}")
                            st.write(f"Description: {item.description}")

                            if st.button("Edit", key=f"edit_btn_{item.id}", type="secondary"):
                                st.session_state["location_edit_status"] = True
                                st.session_state["location_edit_id"] = item.id
                                st.rerun()

                            if st.button("Delete", key=f"del_btn_{item.id}", type="primary"):
                                location = (
                                    session.query(Location).filter(Location.id == item.id).first()
                                )
                                if location:
                                    session.delete(location)
                                    session.commit()
                                    st.rerun()
except Exception as exc:
    st.error(
        "Unable to connect to the database. "
        + f"Please check your configuration or try again later. Error: {exc}"
    )

st.subheader("Planned Capabilities")

st.markdown(
    """
- Create and edit location records
- Track narrative tags
- View relationship graph
"""
)
