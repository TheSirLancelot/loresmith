import bootstrap  # noqa: F401
import io
import ipaddress
import logging
import socket
import streamlit as st
from urllib.parse import urlparse

import requests
from app.components.layout import page_header
from app.db.migrations import get_session
from app.db.schema import NPC
from PIL import Image
from sqlalchemy import select

page_header("NPCs", "Create, manage, and explore characters.")

if "edit_status" not in st.session_state:
    st.session_state["edit_status"] = False
if "npc_edit_id" not in st.session_state:
    st.session_state["npc_edit_id"] = None


def _is_safe_public_image_url(url: str) -> bool:
    """Validate that URL is safe to fetch: public scheme, public IP, no private networks."""
    try:
        parsed = urlparse(url.strip())
        if parsed.scheme not in {"http", "https"}:
            return False
        if not parsed.hostname:
            return False

        # Resolve all A/AAAA records and reject any non-public target.
        infos = socket.getaddrinfo(parsed.hostname, None)
        for info in infos:
            ip_str = info[4][0]
            ip_obj = ipaddress.ip_address(ip_str)
            if (
                ip_obj.is_private
                or ip_obj.is_loopback
                or ip_obj.is_link_local
                or ip_obj.is_multicast
                or ip_obj.is_reserved
            ):
                return False

        return True
    except Exception:
        return False


def _validate_uploaded_image(uploaded_file) -> bytes | None:
    """Validate and extract bytes from uploaded file. Enforces 2 MB size limit."""
    if uploaded_file is None:
        return None

    MAX_SIZE_MB = 2
    MAX_SIZE_BYTES = MAX_SIZE_MB * 1024 * 1024

    try:
        file_bytes = uploaded_file.getvalue()
        if len(file_bytes) > MAX_SIZE_BYTES:
            return None
        return file_bytes
    except Exception:
        return None


def _fetch_image_bytes(url: str) -> bytes | None:
    """Safely fetch image from URL with validation and limits."""
    if not _is_safe_public_image_url(url):
        return None

    try:
        res = requests.get(
            url,
            timeout=5,
            allow_redirects=False,
            headers={"User-Agent": "LoreSmith/1.0"},
        )
        if res.status_code != 200:
            return None

        content_type = res.headers.get("Content-Type", "").lower()
        if not content_type.startswith("image/"):
            return None

        # 5 MB cap to avoid loading huge payloads.
        if len(res.content) > 5 * 1024 * 1024:
            return None

        return res.content
    except requests.RequestException:
        return None


with st.form("new_npc_form", clear_on_submit=True):
    st.subheader("Create New NPC")
    st.write("Name and status are required. Description is optional.")

    name_field = st.text_input("Name")
    status_field = st.text_input("Status")
    description_field = st.text_area("Description")
    image_bytes_field = st.file_uploader(
        "Upload Image",
        key="new_image_upload",
        type=["jpg", "jpeg", "png", "gif", "webp"],
    )
    image_url_field = st.text_input("Image URL", key="new_image_url")
    submit = st.form_submit_button("Create NPC")

    if submit:
        name = name_field.strip()
        status = status_field.strip()
        description = description_field.strip()
        image_bytes = None
        image_url = image_url_field.strip() if image_url_field else ""

        # Check if name is empty
        if not name:
            st.error("Name cannot be empty.")
        # Check if status is empty
        elif not status:
            st.error("Status cannot be empty.")
        elif image_bytes_field and image_url:
            st.error("Can only upload image or provide image URL, not both!")
        else:
            try:
                with get_session() as session:
                    image_bytes = None
                    if image_bytes_field:
                        image_bytes = _validate_uploaded_image(image_bytes_field)
                        if image_bytes is None:
                            st.error(
                                "Image file too large. Maximum size is 2 MB. "
                                "Please upload a smaller image."
                            )
                            raise ValueError("Image validation failed")

                    session.add(
                        NPC(
                            name=name,
                            status=status,
                            description=description,
                            image_bytes=image_bytes,
                            image_url=image_url,
                        )
                    )
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
        records = session.execute(select(NPC).order_by(NPC.name)).scalars().all()

        if not records:
            st.info("No NPCs found in the database.")
        else:
            if not st.session_state["edit_status"]:
                for item in records:
                    with st.expander(f"{item.name}"):
                        col1, col2 = st.columns([1, 6])

                        with col1:
                            if item.image_bytes:
                                try:
                                    img = Image.open(io.BytesIO(item.image_bytes))
                                    width, height = img.size
                                    aspect_ratio = width / height
                                    resized_img = img.resize((int(175 * aspect_ratio), 175))
                                    st.image(resized_img)
                                except Exception as exc:
                                    st.error("Unable to load profile image.")
                                    logging.getLogger("connection").exception(exc)
                            elif item.image_url:
                                try:
                                    img_bytes = _fetch_image_bytes(item.image_url)
                                    if img_bytes:
                                        img = Image.open(io.BytesIO(img_bytes))
                                        width, height = img.size
                                        aspect_ratio = width / height
                                        resized_img = img.resize((int(175 * aspect_ratio), 175))
                                        st.image(resized_img)
                                except Exception as exc:
                                    st.error("Unable to load profile image.")
                                    logging.getLogger("connection").exception(exc)

                        with col2:
                            st.write(f"Status: {item.status.upper()}")
                            st.write(f"Description: {item.description}")

                            if st.button("Edit", key=f"edit_btn_{item.id}", type="secondary"):
                                st.session_state["edit_status"] = True
                                st.session_state["npc_edit_id"] = item.id
                                st.rerun()

                            if st.button("Delete", key=f"del_btn_{item.id}", type="primary"):
                                npc = session.query(NPC).filter(NPC.id == item.id).first()
                                if npc:
                                    session.delete(npc)
                                    session.commit()
                                    st.rerun()
            else:
                for item in records:
                    if item.id == st.session_state["npc_edit_id"]:
                        with st.expander(f"{item.name}"):
                            # This doubly protects us from None values
                            edit_npc_name = st.text_input("Name", value=item.name) or ""
                            edit_npc_status = st.text_input("Status", value=item.status) or ""
                            edit_npc_desc = (
                                st.text_area("Description", value=item.description) or ""
                            )
                            edit_npc_image_bytes = st.file_uploader(
                                "Upload Image",
                                key="update_image_upload",
                                type=["jpg", "jpeg", "png", "gif", "webp"],
                            )
                            edit_npc_image_url = st.text_input("Image URL", value=item.image_url)
                            updated_name = edit_npc_name.strip()
                            updated_status = edit_npc_status.strip()
                            updated_description = edit_npc_desc.strip()
                            updated_image_url = (
                                edit_npc_image_url.strip() if edit_npc_image_url else ""
                            )

                            if st.button("Update", key=f"update_btn_{item.id}", type="secondary"):
                                if not updated_name:
                                    st.error("Name cannot be empty.")
                                # Check if status is empty
                                elif not updated_status:
                                    st.error("Status cannot be empty.")
                                elif edit_npc_image_bytes and updated_image_url:
                                    st.error(
                                        "Can only upload image or provide image URL, not both!"
                                    )
                                else:
                                    try:
                                        npc = session.query(NPC).filter(NPC.id == item.id).first()
                                        if npc is None:
                                            st.error("This NPC no longer exists.")
                                            st.session_state["edit_status"] = False
                                            st.session_state["npc_edit_id"] = None
                                            st.rerun()

                                        npc.name = updated_name
                                        npc.status = updated_status
                                        npc.description = updated_description
                                        if edit_npc_image_bytes:
                                            validated_bytes = _validate_uploaded_image(
                                                edit_npc_image_bytes
                                            )
                                            if validated_bytes is None:
                                                st.error(
                                                    "Image file too large. Maximum size is 2 MB. "
                                                    "Please upload a smaller image."
                                                )
                                            else:
                                                npc.image_bytes = validated_bytes
                                                npc.image_url = None
                                                session.commit()
                                                st.session_state["edit_status"] = False
                                                st.session_state["npc_edit_id"] = None
                                                st.rerun()
                                        elif updated_image_url:
                                            npc.image_url = updated_image_url
                                            npc.image_bytes = None
                                            session.commit()
                                            st.session_state["edit_status"] = False
                                            st.session_state["npc_edit_id"] = None
                                            st.rerun()
                                        else:
                                            npc.image_url = None
                                            npc.image_bytes = None
                                            session.commit()
                                            st.session_state["edit_status"] = False
                                            st.session_state["npc_edit_id"] = None
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
                                st.session_state["npc_edit_id"] = None
                                st.rerun()
                    else:
                        with st.expander(f"{item.name}"):
                            col1, col2 = st.columns([1, 6])

                            with col1:
                                if item.image_bytes:
                                    try:
                                        img = Image.open(io.BytesIO(item.image_bytes))
                                        width, height = img.size
                                        aspect_ratio = width / height
                                        resized_img = img.resize((int(175 * aspect_ratio), 175))
                                        st.image(resized_img)
                                    except Exception as exc:
                                        st.error("Unable to load profile image.")
                                        logging.getLogger("connection").exception(exc)
                                elif item.image_url:
                                    try:
                                        img_bytes = _fetch_image_bytes(item.image_url)
                                        if img_bytes:
                                            img = Image.open(io.BytesIO(img_bytes))
                                            width, height = img.size
                                            aspect_ratio = width / height
                                            resized_img = img.resize((int(175 * aspect_ratio), 175))
                                            st.image(resized_img)
                                    except Exception as exc:
                                        st.error("Unable to load profile image.")
                                        logging.getLogger("connection").exception(exc)

                            with col2:
                                st.write(f"Status: {item.status.upper()}")
                                st.write(f"Description: {item.description}")

                                if st.button("Edit", key=f"edit_btn_{item.id}", type="secondary"):
                                    st.session_state["edit_status"] = True
                                    st.session_state["npc_edit_id"] = item.id
                                    st.rerun()

                                if st.button("Delete", key=f"del_btn_{item.id}", type="primary"):
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
