import bootstrap  # noqa: F401
import logging
from datetime import date

import streamlit as st
from app.components.layout import page_header
from app.db.migrations import get_session, setup_schema
from app.db.schema import SessionLog
from sqlalchemy import select

page_header("Sessions", "Record events and evolving story arcs.")

schema_ok, schema_msg = setup_schema()
if not schema_ok:
    st.warning(f"Schema: {schema_msg}")

with st.form("new_session_form", clear_on_submit=True):
    st.subheader("Create Session Log")
    st.write("Title and date are required. All other fields are optional.")

    title_field = st.text_input("Title")
    session_date_field = st.date_input("Date", value=date.today())
    session_number_field = st.number_input("Session Number", min_value=1, step=1, value=None)
    notes_field = st.text_area("Notes", height=180)
    recap_field = st.text_area("Recap (read aloud next session)", height=120)
    hooks_field = st.text_area("Next Session Hooks / Cliffhangers", height=120)
    xp_field = st.number_input("XP Awarded", min_value=0, step=1, value=None)
    loot_field = st.text_area("Loot Awarded", height=80)
    duration_field = st.number_input("Duration (minutes)", min_value=1, step=1, value=None)
    submit = st.form_submit_button("Create Session")

    if submit:
        title = title_field.strip()
        notes = notes_field.strip()

        if not title:
            st.error("Title cannot be empty.")
        else:
            try:
                with get_session() as session:
                    session.add(
                        SessionLog(
                            title=title,
                            session_date=session_date_field,
                            session_number=session_number_field or None,
                            notes=notes or None,
                            recap=recap_field.strip() or None,
                            next_session_hooks=hooks_field.strip() or None,
                            xp_awarded=xp_field if xp_field is not None else None,
                            loot_awarded=loot_field.strip() or None,
                            duration_minutes=duration_field if duration_field is not None else None,
                        )
                    )
                    session.commit()

                st.success(f"Session '{title}' created!")
            except Exception as exc:
                st.error(
                    "Unable to connect to the database. "
                    + "Please check your configuration or try again later."
                )
                logging.getLogger("connection").exception(exc)

st.divider()

try:
    with get_session() as session:
        records = (
            session.execute(select(SessionLog).order_by(SessionLog.session_date.desc()))
            .scalars()
            .all()
        )

        if not records:
            st.info("No session logs found in the database.")
        else:
            st.subheader("Session Logs")
            for item in records:
                if f"session_edit_{item.id}" not in st.session_state:
                    st.session_state[f"session_edit_{item.id}"] = False

                label = f"{item.session_date.isoformat()} - {item.title}"
                if item.session_number is not None:
                    label = f"#{item.session_number} | {label}"

                if st.session_state[f"session_edit_{item.id}"]:
                    with st.expander(label, expanded=True):
                        edit_title = st.text_input(
                            "Title", value=item.title, key=f"edit_title_{item.id}"
                        )
                        edit_date = st.date_input(
                            "Date", value=item.session_date, key=f"edit_date_{item.id}"
                        )
                        edit_number = st.number_input(
                            "Session Number",
                            min_value=1,
                            step=1,
                            value=item.session_number,
                            key=f"edit_number_{item.id}",
                        )
                        edit_notes = st.text_area(
                            "Notes", value=item.notes or "", height=180, key=f"edit_notes_{item.id}"
                        )
                        edit_recap = st.text_area(
                            "Recap (read aloud next session)",
                            value=item.recap or "",
                            height=120,
                            key=f"edit_recap_{item.id}",
                        )
                        edit_hooks = st.text_area(
                            "Next Session Hooks / Cliffhangers",
                            value=item.next_session_hooks or "",
                            height=120,
                            key=f"edit_hooks_{item.id}",
                        )
                        edit_xp = st.number_input(
                            "XP Awarded",
                            min_value=0,
                            step=1,
                            value=item.xp_awarded,
                            key=f"edit_xp_{item.id}",
                        )
                        edit_loot = st.text_area(
                            "Loot Awarded",
                            value=item.loot_awarded or "",
                            height=80,
                            key=f"edit_loot_{item.id}",
                        )
                        edit_duration = st.number_input(
                            "Duration (minutes)",
                            min_value=1,
                            step=1,
                            value=item.duration_minutes,
                            key=f"edit_duration_{item.id}",
                        )

                        if st.button("Update", key=f"update_btn_{item.id}", type="secondary"):
                            if not edit_title.strip():
                                st.error("Title cannot be empty.")
                            else:
                                try:
                                    record = session.get(SessionLog, item.id)
                                    if record is None:
                                        st.error("This session log no longer exists.")
                                        st.session_state[f"session_edit_{item.id}"] = False
                                        st.rerun()
                                    record.title = edit_title.strip()
                                    record.session_date = edit_date
                                    record.session_number = edit_number or None
                                    record.notes = edit_notes.strip() or None
                                    record.recap = edit_recap.strip() or None
                                    record.next_session_hooks = edit_hooks.strip() or None
                                    record.xp_awarded = edit_xp if edit_xp is not None else None
                                    record.loot_awarded = edit_loot.strip() or None
                                    record.duration_minutes = (
                                        edit_duration if edit_duration is not None else None
                                    )
                                    session.commit()
                                    st.session_state[f"session_edit_{item.id}"] = False
                                    st.rerun()
                                except Exception as exc:
                                    session.rollback()
                                    st.error(
                                        "Unable to connect to the database. "
                                        + "Please check your configuration or try again later."
                                    )
                                    logging.getLogger("connection").exception(exc)

                        if st.button("Cancel", key=f"cancel_btn_{item.id}", type="secondary"):
                            st.session_state[f"session_edit_{item.id}"] = False
                            st.rerun()
                else:
                    with st.expander(label):
                        st.write(f"**Date:** {item.session_date.isoformat()}")
                        if item.duration_minutes is not None:
                            st.write(f"**Duration:** {item.duration_minutes} min")
                        if item.notes:
                            st.write(f"**Notes:** {item.notes}")
                        if item.recap:
                            st.write(f"**Recap:** {item.recap}")
                        if item.next_session_hooks:
                            st.write(f"**Next Session Hooks:** {item.next_session_hooks}")
                        if item.xp_awarded is not None:
                            st.write(f"**XP Awarded:** {item.xp_awarded}")
                        if item.loot_awarded:
                            st.write(f"**Loot Awarded:** {item.loot_awarded}")

                        if st.button("Edit", key=f"edit_btn_{item.id}", type="secondary"):
                            st.session_state[f"session_edit_{item.id}"] = True
                            st.rerun()

                        if st.button("Delete", key=f"del_btn_{item.id}", type="primary"):
                            try:
                                record = session.get(SessionLog, item.id)
                                if record:
                                    session.delete(record)
                                    session.commit()
                                    st.session_state.pop(f"session_edit_{item.id}", None)
                                    st.rerun()
                            except Exception as exc:
                                session.rollback()
                                st.error(
                                    "Unable to connect to the database. "
                                    + "Please check your configuration or try again later."
                                )
                                logging.getLogger("connection").exception(exc)
except Exception as exc:
    st.error(
        "Unable to connect to the database. "
        + "Please check your configuration or try again later."
    )
    logging.getLogger("connection").exception(exc)
