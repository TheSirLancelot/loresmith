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
            if not st.session_state["edit_status"]:
                for item in records:
                    with st.expander(f"{item.name}"):
                        st.write(f"Description: {item.description}")

                        if st.button("Edit", key=f"edit_btn_{item.id}", type="secondary"):
                            st.session_state["edit_status"] = True
                            st.session_state["faction_edit_id"] = item.id
                            st.rerun()

                        if st.button("Delete", key=f"del_btn_{item.id}", type="primary"):
                            session.delete(item)
                            session.commit()
                            st.rerun()
            else:
                for item in records:
                    if item.id == st.session_state["faction_edit_id"]:
                        with st.expander(f"{item.name}"):
                            # This doubly protects us from None values
                            edit_faction_name = st.text_input("Name", value=item.name) or ""
                            edit_faction_description = (
                                st.text_area("Description", value=item.description) or ""
                            )

                            updated_name = edit_faction_name.strip()
                            updated_description = edit_faction_description.strip()

                            if st.button("Update", key=f"update_btn_{item.id}", type="secondary"):
                                if not updated_name:
                                    st.error("Name cannot be empty.")
                                else:
                                    try:
                                        faction = (
                                            session.query(Faction)
                                            .filter(Faction.id == item.id)
                                            .first()
                                        )
                                        if faction is None:
                                            st.error("This faction no longer exists.")
                                            st.session_state["edit_status"] = False
                                            st.session_state["faction_edit_id"] = None
                                            st.rerun()

                                        faction.name = updated_name
                                        faction.description = updated_description
                                        session.commit()
                                        st.session_state["edit_status"] = False
                                        st.session_state["faction_edit_id"] = None
                                        st.rerun()
                                    except Exception as exc:
                                        session.rollback()
                                        st.error(
                                            "Unable to connect to the database. "
                                            + "Please check your configuration or try again later."
                                        )
                                        logging.getLogger("connection").exception(exc)
                            if st.button("Cancel", key="update_cancel_btn", type="secondary"):
                                st.session_state["edit_status"] = False
                                st.session_state["faction_edit_id"] = None
                                st.rerun()
                    else:
                        with st.expander(f"{item.name}"):
                            st.write(f"Description: {item.description}")

                            if st.button("Edit", key=f"edit_btn_{item.id}", type="secondary"):
                                st.session_state["edit_status"] = True
                                st.session_state["faction_edit_id"] = item.id
                                st.rerun()

                            if st.button("Delete", key=f"del_btn_{item.id}", type="primary"):
                                faction = (
                                    session.query(Faction).filter(Faction.id == item.id).first()
                                )
                                if faction:
                                    session.delete(faction)
                                    session.commit()
                                    st.rerun()
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

st.warning("Database integration not yet connected.")
