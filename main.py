import streamlit as st
from ui import render_ui

st.set_page_config(
    page_title="Loopify",
    page_icon="➰",
    layout="wide",
)

render_ui()