import streamlit as st
from goldhand import *


st.set_page_config( layout="wide", page_title="EU Finance",page_icon="📊",)


# --- INTRO ---
about_page = st.Page(
    "views/intro.py",
    title="About this app",
    icon=":material/account_circle:",
    default=True,
)

# --- STOCK ---
adat_page = st.Page(
    "views/data_watch.py",
    title="Adatok",
    icon=":material/trending_up:",
)



# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Info": [about_page],
        "Adat": [adat_page],
    }
)


# --- SHARED ON ALL PAGES ---
st.logo(
    'https://i.ibb.co/Pgw52bM/Screenshot-from-2024-12-26-09-41-17-removebg-preview.png',
    link="https://goldhandfinance.streamlit.app/",
    size="large")

st.sidebar.markdown("valami  [Átlátszó.hu](https://atlatszo.hu)")


# --- RUN NAVIGATION ---
pg.run()
