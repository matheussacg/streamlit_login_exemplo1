import streamlit as st
from time import sleep
from navigation import make_sidebar
import requests

BASE_URL = "http://127.0.0.1:8001"

make_sidebar()

st.title("Bem vindo, Streamlit")

st.write("Faça login para continuar (username `matheus`, password `123`).")

username = st.text_input("Username")
password = st.text_input("Password", type="password")

# Botão de Login
if st.button("Entrar"):
    if username and password:
        # Requisição ao backend
        response = requests.post(
            f"{BASE_URL}/login/", json={"username": username, "password": password}
        )

        if response.status_code == 200:
            st.session_state.logged_in = True  # Define o estado como logado
            st.success("Login realizado com sucesso! Redirecionando...")
            sleep(0.5)
            st.switch_page("pages/home.py")
        else:
            st.error("Usuário ou senha incorretos.")
    else:
        st.warning("Preencha todos os campos.")
