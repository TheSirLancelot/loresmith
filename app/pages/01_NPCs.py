import bootstrap  # noqa: F401
import streamlit as st
from app.components.layout import page_header
from app.db.migrations import get_session
from app.db.schema import NPC
from sqlalchemy import select

page_header("NPCs", "Create, manage, and explore characters.")

session = get_session()

with session:
    records = session.execute(select(NPC)).scalars().all()

    if not records:
        st.info('No NPCs found in the database.')
    else:
        for item in records:
            with st.expander(f'{item.name}'):
                st.write(f'Status: {item.status.upper()}')
                st.write(f'Description: {item.description}')

st.subheader("Planned Capabilities")

st.markdown(
    """
- Create and edit NPC records
- Assign faction affiliations
- Track narrative tags
- View relationship graph
"""
)