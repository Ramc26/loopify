import streamlit as st
import requests
import pandas as pd
import json
from utilities import (
    load_font, load_svg, parse_curl_command, 
    format_headers, format_form_data, run_batch_requests
)
import os

def initialize_session_state():
    if "headers" not in st.session_state:
        st.session_state.headers = pd.DataFrame([{"Header": "", "Value": ""}])
    if "form_data" not in st.session_state:
        st.session_state.form_data = pd.DataFrame([{"Key": "", "Value": ""}])
    if "request_method" not in st.session_state:
        st.session_state.request_method = "GET"
    if "request_url" not in st.session_state:
        st.session_state.request_url = "https://httpbin.org/get"
    if "payload_type" not in st.session_state:
        st.session_state.payload_type = "None"
    if "payload_body" not in st.session_state:
        st.session_state.payload_body = ""

def render_custom_title():
    ASSETS_DIR = "assets"
    FONT_PATH = os.path.join(ASSETS_DIR, "BagelFatOne-Regular.ttf")
    SVG_PATH = os.path.join(ASSETS_DIR, "loopify.svg")
    FONT_NAME = "BagelFatOne Inline"

    try:
        font_css = load_font(FONT_PATH, FONT_NAME)
        svg_data_url = load_svg(SVG_PATH)
        
        # Apply the CSS styles
        st.markdown(f"<style>{font_css}</style>", unsafe_allow_html=True)
        
        # Apply additional CSS for the custom title
        st.markdown("""
        <style>
        .custom-title {
            display: flex;
            color: #FFB300;
            align-items: center;
            gap: 12px;
            padding-top: 20px;
            padding-bottom: 20px;
        }
        .custom-title img {
            height: 75px;
            width: 75px;
        }
        .custom-title h1 {
            align-items: center;
            font-family: 'BagelFatOne Inline', sans-serif;
            font-size: 3em;
            font-weight: 600;
            margin: 0;
            padding: 0;
        }
        
        .bold-tab {
            font-weight: 900 !important;
            font-size: 1.2em !important;
        }
        .pro-tab {
            font-weight: 900 !important;
            font-size: 1.3em !important;
            color: #FF6B00 !important;
        }
        
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
        }
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            background-color: #F0F2F6;
            border-radius: 4px 4px 0px 0px;
            gap: 1px;
            padding-top: 10px;
            padding-bottom: 10px;
            font-weight: 900;
            font-size: 1.1em;
        }
        .stTabs [aria-selected="true"] {
            background-color: #FFFFFF;
            border-bottom: 3px solid #FF6B00;
            font-weight: 900;
            font-size: 1.2em;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Render the custom title
        st.markdown(f"""
        <div class="custom-title">
            <img src="{svg_data_url}" alt="Loopify Logo">
            <h1>Loopify : <span>Automate Your API Calls</span></h1>
        </div>
        """, unsafe_allow_html=True)

    except FileNotFoundError:
        st.error("Assets not found. Make sure 'assets' directory exists.")
        st.title("➰ Loopify")
    except Exception as e:
        st.error(f"Error loading assets: {e}")
        st.title("➰ Loopify")


def render_single_request_tab():
    with st.expander("Import from cURL"):
        curl_command = st.text_area("Paste cURL command here", 
                                    placeholder='curl -X POST "https://httpbin.org/post" -H "Content-Type: application/json" -d "{\\"key\\":\\"value\\"}"',
                                    key="curl_input")
        
        if st.button("Import cURL", width='stretch'):
            if curl_command:
                try:
                    url, method, headers, data, payload_type = parse_curl_command(curl_command)
                    st.session_state.request_method = method
                    st.session_state.request_url = url
                    headers_list = [{"Header": k, "Value": v} for k, v in headers.items()]
                    if not headers_list:
                        headers_list = [{"Header": "", "Value": ""}]
                    st.session_state.headers = pd.DataFrame(headers_list)
                    st.session_state.payload_type = payload_type
                    if payload_type == "JSON":
                        try:
                            st.session_state.payload_body = json.dumps(json.loads(data), indent=2)
                        except (json.JSONDecodeError, TypeError):
                            st.session_state.payload_body = str(data)
                    elif payload_type == "Form-Data":
                        form_list = [{"Key": k, "Value": v} for k, v in data.items()]
                        st.session_state.form_data = pd.DataFrame(form_list)
                        st.session_state.payload_body = ""
                    elif payload_type == "Text":
                        st.session_state.payload_body = data
                    else:
                        st.session_state.payload_type = "None"
                        st.session_state.payload_body = ""
                    st.success("cURL command imported successfully!")
                except Exception as e:
                    st.error(f"Failed to parse cURL command: {e}")
            else:
                st.warning("Please paste a cURL command.")

    col_method, col_url = st.columns([1, 4])
    with col_method:
        method = st.selectbox("Method", 
                              ["GET", "POST", "PUT", "DELETE", "PATCH"], 
                              key="request_method")
    with col_url:
        url = st.text_input("URL", 
                            placeholder="Enter request URL", 
                            key="request_url")
    if st.button("Send Request", type="primary", width='stretch'):
        method = st.session_state.request_method
        url = st.session_state.request_url
        payload_type = st.session_state.payload_type
        headers = format_headers(st.session_state.headers)
        kwargs = {"headers": headers, "timeout": 10}
        try:
            if method in ["POST", "PUT", "PATCH"]:
                if payload_type == "JSON":
                    kwargs['json'] = json.loads(st.session_state.payload_body)
                elif payload_type == "Form-Data":
                    kwargs['data'] = format_form_data(st.session_state.form_data)
                elif payload_type == "Text":
                    kwargs['data'] = st.session_state.payload_body.encode('utf-8')
                    if 'Content-Type' not in headers:
                        headers['Content-Type'] = 'text/plain'
            with st.spinner("Sending request..."):
                response = requests.request(method, url, **kwargs)
            st.session_state.response = response
        except json.JSONDecodeError:
            st.error("Invalid JSON. Please check your syntax.")
        except Exception as e:
            st.session_state.response = None
            st.error(f"Request failed: {e}")
        
    st.divider()
    col_request, col_response = st.columns(2, gap="large")
    with col_request:
        st.subheader("Request")
        header_tab, payload_tab = st.tabs(["Headers", "Payload"])
        with header_tab:
            st.markdown("###### Headers")
            st.session_state.headers = st.data_editor(
                st.session_state.headers,
                num_rows="dynamic",
                width='stretch',
                column_config={
                    "Header": st.column_config.TextColumn(width="medium"),
                    "Value": st.column_config.TextColumn(width="large"),
                }
            )
        with payload_tab:
            st.markdown("###### Payload")
            if st.session_state.request_method in ["GET", "DELETE"]:
                st.info("Payload is not applicable for GET or DELETE requests.")
                st.session_state.payload_type = "None"
            payload_type = st.radio(
                "Payload Type", 
                ["JSON", "Form-Data", "Text", "None"], 
                horizontal=True,
                key="payload_type",
                disabled=(st.session_state.request_method in ["GET", "DELETE"])
            )
            if st.session_state.payload_type == "JSON":
                payload_body = st.text_area("JSON Body", height=200, key="payload_body")
            elif st.session_state.payload_type == "Form-Data":
                st.session_state.form_data = st.data_editor(
                    st.session_state.form_data,
                    num_rows="dynamic",
                    width='stretch',
                    column_config={
                        "Key": st.column_config.TextColumn(width="medium"),
                        "Value": st.column_config.TextColumn(width="large"),
                    }
                )
            elif st.session_state.payload_type == "Text":
                payload_body = st.text_area("Text Body", height=200, key="payload_body")
    
    with col_response:
        st.subheader("Response")
        if "response" in st.session_state and st.session_state.response:
            response = st.session_state.response
            status = response.status_code
            if 200 <= status < 300:
                st.metric("Status Code", f"{status} ✅")
            elif 400 <= status < 500:
                st.metric("Status Code", f"{status} Client Error ⚠️")
            elif status >= 500:
                st.metric("Status Code", f"{status} Server Error ❌")
            else:
                st.metric("Status Code", f"{status} ℹ️")
            resp_body_tab, resp_header_tab = st.tabs(["Body", "Headers"])
            with resp_body_tab:
                try:
                    st.json(response.json())
                except requests.exceptions.JSONDecodeError:
                    st.code(response.text, language="text")
            with resp_header_tab:
                st.json(dict(response.headers))
        else:
            st.info("Click 'Send Request' to see the response here.")

def render_batch_runner_tab():
    st.header("🚀 Loopify Pro - Batch Runner")
    st.markdown("""
    Execute multiple API requests in sequence with configurable delays between calls.
    Perfect for testing workflows, load testing, or processing batch operations.
    """)
    
    sample_data = [
        {"method": "GET", "url": "https.httpbin.org/get?item=1", "headers": '{"Accept": "application/json"}', "payload_type": "none", "payload": ""},
        {"method": "POST", "url": "https.httpbin.org/post", "headers": '{"Content-Type": "application/json"}', "payload_type": "json", "payload": '{"name": "Item 1", "value": 100}'},
        {"method": "PUT", "url": "https.httpbin.org/put", "headers": "", "payload_type": "form", "payload": '{"id": "A123", "status": "updated"}'},
        {"method": "GET", "url": "https.httpbin.org/status/404", "headers": "", "payload_type": "none", "payload": ""},
    ]
    sample_df = pd.DataFrame(sample_data)
    
    @st.cache_data
    def convert_df_to_csv(df):
        return df.to_csv(index=False).encode('utf-8')
    
    st.download_button(
        label="Download Sample CSV Template",
        data=convert_df_to_csv(sample_df),
        file_name="sample_batch.csv",
        mime="text/csv",
    )
    st.divider()
    uploaded_file = st.file_uploader("Upload your CSV or JSON batch file", type=["csv", "json"])
    delay = st.number_input("Delay between requests (seconds)", min_value=0.0, max_value=60.0, value=1.0, step=0.5)
    if st.button("Run Batch", type="primary", width='stretch', disabled=(not uploaded_file)):
        file_content = uploaded_file.getvalue().decode("utf-8")
        file_type = uploaded_file.type.split('/')[1]
        with st.spinner("Batch in progress..."):
            results_df = run_batch_requests(file_content, file_type, delay)
        if results_df is not None:
            st.session_state.batch_results = results_df
    if "batch_results" in st.session_state:
        st.subheader("Batch Results")
        st.dataframe(st.session_state.batch_results, width='stretch')
        st.download_button(
            label="Download Results as CSV",
            data=convert_df_to_csv(st.session_state.batch_results),
            file_name="batch_results.csv",
            mime="text/csv",
            type="primary"
        )

def render_footer():
    st.markdown(
        """
        <div style='text-align: center; padding: 10px;'>
            <small>Crafted with care by 🦉 <a href='https://ramc26.github.io/RamTechSuite' target='_blank'>RamTechSuite</a> | Hosted on Streamlit</small>
        </div>
        """, 
        unsafe_allow_html=True
    )

def render_ui():
    initialize_session_state()
    render_custom_title()
    
    tab_style = """
    <style>
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #F0F2F6;
        border-radius: 4px 4px 0px 0px;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
        font-weight: 900;
        font-size: 1.1em;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFFFFF;
        border-bottom: 3px solid #FF6B00;
        font-weight: 900;
        font-size: 1.2em;
    }
    </style>
    """
    
    st.markdown(tab_style, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔧 Single Request", "🚀 LOOPIFY PRO"])
    
    with tab1:
        render_single_request_tab()
    
    with tab2:
        render_batch_runner_tab()
    
    render_footer()


