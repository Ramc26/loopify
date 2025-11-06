import streamlit as st
from ui import render_ui

def main():
    st.set_page_config(
        page_title="Loopify",
        page_icon="➰",
        layout="wide",
    )
    render_ui()

if __name__ == "__main__":
    main()