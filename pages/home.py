import streamlit as st
from navigation import make_sidebar
import numpy as np

st.set_page_config(layout="wide")
make_sidebar()

st.title("Página Home")
st.write("Bem-vindo à página inicial!")

numero = st.slider(min_value=0, max_value=100, label="Escolha um número")
st.write(f"o número é: {numero}")

with st.container():
    st.write("Isso está dentro do contêiner")

    # You can call any Streamlit command, including custom components:
    st.bar_chart(np.random.randn(50, 3))

st.write("Isso está fora do contêiner")
imagem = st.image(
    image="https://cdn.pixabay.com/photo/2024/02/26/19/39/monochrome-image-8598798_1280.jpg",
    width=300,
)
