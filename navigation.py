import streamlit as st
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages


def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Não foi possível obter o contexto do script")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]


def make_sidebar():
    with st.sidebar:
        st.title("Login")
        st.write("")
        st.write("")

        if st.session_state.get("logged_in", False):
            st.page_link("pages/home.py", label="Home", icon="🔒")
            st.page_link("pages/cadastro.py", label="Cadastro", icon="🕵️")

            st.write("")
            st.write("")

            if st.button("Log out"):
                logout()

        elif get_current_page_name() != "login":
            st.switch_page("login.py")


def logout():
    st.session_state.logged_in = False
    st.info("Logado com sucesso!")
    sleep(0.5)
    st.switch_page("login.py")
