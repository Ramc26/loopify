import streamlit as st
from ui import render_ui

st.set_page_config(
    page_title="Loopify",
    page_icon="➰",
    layout="wide",
)

st.markdown(
    """
    <head>
        <meta property="og:title" content="Loopify - Automate Your API Calls" />
        <meta property="og:description" content="A powerful Streamlit app for testing APIs, executing single requests, and running batch operations. Import from cURL, test endpoints, and automate your API workflows." />
        <meta property="og:image" content="https://github.com/Ramc26/loopify/blob/master/assets/loopify.svg" />
        <meta property="og:url" content="https://loopify.streamlit.app//" />
        <meta property="og:type" content="website" />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="Loopify - Automate Your API Calls" />
        <meta name="twitter:description" content="A powerful Streamlit app for testing APIs, executing single requests, and running batch operations." />
        <meta name="twitter:image" content="https://github.com/Ramc26/loopify/blob/master/assets/loopify.svg" />
    </head>
    """,
    unsafe_allow_html=True,
)

render_ui()