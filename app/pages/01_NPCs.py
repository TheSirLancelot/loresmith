import bootstrap  # noqa: F401
import io
import streamlit as st
import logging
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

with st.form("new_npc_form", clear_on_submit=True):
    st.subheader("Create New NPC")
    st.write("Name and status are required. Description is optional.")

    name_field = st.text_input("Name")
    status_field = st.text_input("Status")
    description_field = st.text_area("Description")
    image_bytes_field = st.file_uploader("Upload Image")
    image_url_field = st.text_input("Image URL")
    submit = st.form_submit_button("Create NPC")

    if submit:
        name = name_field.strip()
        status = status_field.strip()
        description = description_field.strip()
        image_bytes = None
        image_url = None

        # Check if name is empty
        if not name:
            st.error("Name cannot be empty.")
        # Check if status is empty
        elif not status:
            st.error("Status cannot be empty.")
        elif image_bytes_field and image_url_field:
            st.error("Can only upload image or provide image URL, not both!")
        else:
            try:
                with get_session() as session:
                    if image_bytes_field:
                        image_bytes = image_bytes_field.getvalue()
                    elif image_url_field:
                        image_url = image_url_field.strip()
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
                                img = Image.open(io.BytesIO(item.image_bytes))
                                width, height = img.size
                                aspect_ratio = width / height
                                resized_img = img.resize((int(175 * aspect_ratio), 175))
                                st.image(resized_img)
                            elif item.image_url:
                                res = requests.get(item.image_url)
                                if res.status_code == 200:
                                    img = Image.open(io.BytesIO(res.content))
                                    width, height = img.size
                                    aspect_ratio = width / height
                                    resized_img = img.resize((int(175 * aspect_ratio), 175))
                                    st.image(resized_img)
                                else:
                                    st.error("Could not load image from URL.")
                            else:
                                res = requests.get(
                                    "https://www.nicepng.com/png/full/110-1102214_amanda-m-blank-profile-face-png.png"
                                )
                                if res.status_code == 200:
                                    img = Image.open(io.BytesIO(res.content))
                                    width, height = img.size
                                    aspect_ratio = width / height
                                    resized_img = img.resize((175, int(175 * aspect_ratio)))
                                    st.image(resized_img)
                                else:
                                    st.error("Could not default image.")

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
                            edit_npc_image_bytes = st.file_uploader("Upload Image")
                            edit_npc_image_url = st.text_input("Image URL", value=item.image_url)
                            updated_name = edit_npc_name.strip()
                            updated_status = edit_npc_status.strip()
                            updated_description = edit_npc_desc.strip()

                            if st.button("Update", key=f"update_btn_{item.id}", type="secondary"):
                                if not updated_name:
                                    st.error("Name cannot be empty.")
                                # Check if status is empty
                                elif not updated_status:
                                    st.error("Status cannot be empty.")
                                elif edit_npc_image_bytes and edit_npc_image_url:
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
                                            npc.image_bytes = edit_npc_image_bytes.getvalue()
                                        elif edit_npc_image_url:
                                            npc.image_url = edit_npc_image_url
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
                                    img = Image.open(io.BytesIO(item.image_bytes))
                                    width, height = img.size
                                    aspect_ratio = width / height
                                    resized_img = img.resize((int(175 * aspect_ratio), 175))
                                    st.image(resized_img)
                                elif item.image_url:
                                    res = requests.get(item.image_url)
                                    if res.status_code == 200:
                                        img = Image.open(io.BytesIO(res.content))
                                        width, height = img.size
                                        aspect_ratio = width / height
                                        resized_img = img.resize((int(175 * aspect_ratio), 175))
                                        st.image(resized_img)
                                    else:
                                        st.error("Could not load image from URL.")
                                else:
                                    res = requests.get(
                                        "https://www.nicepng.com/png/full/110-1102214_amanda-m-blank-profile-face-png.png"
                                    )
                                    if res.status_code == 200:
                                        img = Image.open(io.BytesIO(res.content))
                                        width, height = img.size
                                        aspect_ratio = width / height
                                        resized_img = img.resize((175, int(175 * aspect_ratio)))
                                        st.image(resized_img)
                                    else:
                                        st.error("Could not default image.")

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
