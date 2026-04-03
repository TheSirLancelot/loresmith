"""Database schema definitions using SQLAlchemy ORM."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from sqlalchemy import CheckConstraint, DateTime, LargeBinary, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class NPC(Base):
    """Non-player character entity for campaign management."""

    __tablename__ = "npc"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="active")
    image_bytes: Mapped[bytes | None] = mapped_column(LargeBinary, nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )

    __table_args__ = (
        CheckConstraint(
            "NOT (image_bytes IS NOT NULL AND image_url IS NOT NULL)",
            name="check_at_most_one_filled",
        ),
    )

    def __repr__(self) -> str:
        return f"<NPC(id={self.id!r}, name={self.name!r}, status={self.status!r})>"


class Location(IdMixin, TimestampMixin, Base):
    """Location entity for campaign management."""

    __tablename__ = "location"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False, default="")

    # Return as expander object
    @st.fragment
    def as_expander(self, session):
        with st.expander(f"{self.name}"):
            st.write(f"Description: {self.description}")

            if st.button("Edit", key=f"edit_btn_{self.id}", type="secondary"):
                st.session_state[f"location_edit_{self.id}"] = True
                st.rerun()

            if st.button("Delete", key=f"del_btn_{self.id}", type="primary"):
                try:
                    location = session.get(Location, self.id)
                    if location:
                        session.delete(location)
                        session.commit()
                        del st.session_state[f"location_edit_{self.id}"]
                        st.rerun()
                except Exception as exc:
                    session.rollback()
                    st.error(
                        "Unable to connect to the database. "
                        + "Please check your configuration or try again later."
                    )
                    logging.getLogger("connection").exception(exc)

    @st.fragment
    def as_edit_expander(self, session):
        with st.expander(f"{self.name}"):
            edit_location_name = st.text_input("Name", value=self.name)
            edit_location_desc = st.text_area("Description", value=self.description)

            if st.button("Update", key=f"update_location_btn_{self.id}", type="secondary"):
                if not edit_location_name:
                    st.error("Name cannot be empty.")
                else:
                    try:
                        location = session.get(Location, self.id)
                        if location is None:
                            st.error("This location no longer exists.")
                            del st.session_state[f"location_edit_{self.id}"]
                            st.rerun()

                        location.name = edit_location_name.strip()
                        location.description = edit_location_desc.strip()
                        session.commit()

                        st.session_state[f"location_edit_{self.id}"] = False

                        st.rerun()
                    except Exception as exc:
                        session.rollback()
                        st.error(
                            "Unable to connect to the database. "
                            + "Please check your configuration or try again later."
                        )
                        logging.getLogger("connection").exception(exc)
            if st.button("Cancel", key="update_location_cancel_btn", type="secondary"):
                st.session_state[f"location_edit_{self.id}"] = False
                st.rerun()
