import bootstrap  # noqa: F401
import streamlit as st
import logging
from app.components.layout import page_header
from app.db.migrations import get_session
from app.db.schema import NPC
from sqlalchemy import select

page_header("NPCs", "Create, manage, and explore characters.")

with st.form("new_npc_form", clear_on_submit=True):
    st.subheader("Create New NPC")
    st.write("Name and status are required. Description is optional.")

    name_field = st.text_input("Name")
    status_field = st.text_input("Status")
    description_field = st.text_area("Description")
    submit = st.form_submit_button("Create NPC")

    if submit:
        name = name_field.strip()
        status = status_field.strip()
        description = description_field.strip()

        # Check if name is empty
        if not name:
            st.error("Name cannot be empty.")
        # Check if status is empty
        elif not status:
            st.error("Status cannot be empty.")
        else:
            try:
                with get_session() as session:
                    session.add(NPC(name=name, status=status, description=description))
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
        records = session.execute(select(NPC).order_by(NPC.name)).scalars().all()

        if not records:
            st.info("No NPCs found in the database.")
        else:
            for item in records:
                with st.expander(f"{item.name}"):
                    st.write(f"Status: {item.status.upper()}")
                    st.write(f"Description: {item.description}")

                    if st.button("Delete", key=f"btn_{item.id}", type="primary"):
                        npc = session.query(NPC).filter(NPC.id == item.id).first()
                        if npc:
                            session.delete(npc)
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
- Create and edit NPC records
- Assign faction affiliations
- Track narrative tags
- View relationship graph
"""
)
