import streamlit as st


def page_header(title: str, description: str = ""):
    st.title(title)
    if description:
        st.caption(description)
    st.divider()
