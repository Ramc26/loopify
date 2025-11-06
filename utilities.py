import requests
import pandas as pd
import json
import time
import shlex 
import re
import base64
import os
from io import StringIO
from urllib.parse import parse_qsl
import streamlit as st

def load_font(font_path, font_name):
    with open(font_path, "rb") as f:
        font_data = f.read()
    font_base64 = base64.b64encode(font_data).decode('utf-8')
    css = f"""
    @font-face {{
        font-family: '{font_name}';
        src: url(data:font/ttf;base64,{font_base64}) format('truetype');
    }}
    """
    return css

def load_svg(svg_path):
    with open(svg_path, "rb") as f:
        svg_data = f.read()
    svg_base64 = base64.b64encode(svg_data).decode('utf-8')
    return f"data:image/svg+xml;base64,{svg_base64}"

def parse_curl_command(curl_string):
    try:
        processed_string = re.sub(r'\\(\s*)\n', ' ', curl_string)
        tokens = shlex.split(processed_string)
    except ValueError as e:
        raise Exception(f"Invalid cURL syntax: {e}")

    url = ""
    method = "GET"
    headers = {}
    data_parts = []
    
    it = iter(tokens)
    for token in it:
        if token == 'curl':
            continue
        if token.startswith('http://') or token.startswith('https://'):
            url = token
            continue
        if token in ['-X', '--request']:
            try:
                method = next(it).upper()
            except StopIteration:
                raise Exception(f"Missing value for {token}")
            continue
        if token in ['-H', '--header']:
            try:
                header_str = next(it)
                if ':' in header_str:
                    k, v = header_str.split(':', 1)
                    headers[k.strip()] = v.strip()
            except (StopIteration, ValueError):
                raise Exception(f"Invalid header format: {header_str}")
            continue
        if token in ['-d', '--data', '--data-raw', '--data-binary']:
            try:
                data_parts.append(next(it))
                if method == "GET": method = "POST"
            except StopIteration:
                raise Exception(f"Missing value for {token}")
            continue
        if not url and not token.startswith('-'):
            url = token
    data = None
    payload_type = "None"
    if data_parts:
        lower_headers = {k.lower(): v for k, v in headers.items()}
        content_type = lower_headers.get('content-type', '')
        if len(data_parts) > 1 or 'application/x-www-form-urlencoded' in content_type:
            payload_type = "Form-Data"
            form_string = "&".join(data_parts)
            data = dict(parse_qsl(form_string))
        else:
            data_string = data_parts[0]
            if 'application/json' in content_type or (not content_type and data_string.startswith('{') and data_string.endswith('}')):
                payload_type = "JSON"
                data = data_string
                if 'content-type' not in lower_headers:
                    headers['Content-Type'] = 'application/json'
            else:
                payload_type = "Text"
                data = data_string
    return url, method, headers, data, payload_type

def format_headers(header_df):
    headers = {}
    for _, row in header_df.iterrows():
        key = row["Header"]
        value = row["Value"]
        if key:
            headers[key] = value
    return headers

def format_form_data(form_df):
    form_data = {}
    for _, row in form_df.iterrows():
        key = row["Key"]
        value = row["Value"]
        if key:
            form_data[key] = value
    return form_data

def run_batch_requests(file_content, file_type, delay):
    results = []
    try:
        if file_type == 'csv':
            df = pd.read_csv(StringIO(file_content))
        else:
            df = pd.read_json(StringIO(file_content), orient='records')
    except Exception as e:
        st.error(f"Error parsing file: {e}")
        return None
    required_cols = ['method', 'url', 'payload_type']
    if not all(col in df.columns for col in required_cols):
        st.error(f"File must contain at least these columns: {', '.join(required_cols)}")
        st.info("Optional columns: 'headers' (JSON string), 'payload' (JSON string or text)")
        return None
    if 'headers' not in df.columns: df['headers'] = None
    if 'payload' not in df.columns: df['payload'] = None
    df = df.fillna('')
    progress_bar = st.progress(0, text="Starting batch...")
    status_text = st.empty()
    for i, row in df.iterrows():
        method = row['method'].upper()
        url = row['url']
        payload_type = row['payload_type'].lower()
        try:
            headers = json.loads(row['headers']) if row['headers'] else {}
        except json.JSONDecodeError:
            headers = {}
            st.warning(f"Row {i+1}: Invalid JSON in headers. Using empty headers.")
        kwargs = {"timeout": 10}
        payload_data = row['payload']
        if method in ['POST', 'PUT', 'PATCH'] and payload_data:
            if payload_type == 'json':
                try:
                    kwargs['json'] = json.loads(payload_data)
                except json.JSONDecodeError:
                    st.warning(f"Row {i+1}: Invalid JSON in payload. Sending as raw text.")
                    kwargs['data'] = payload_data
            elif payload_type == 'form':
                try:
                    kwargs['data'] = json.loads(payload_data)
                except json.JSONDecodeError:
                     st.warning(f"Row {i+1}: Invalid JSON for form data. Skipping payload.")
            elif payload_type == 'text':
                kwargs['data'] = payload_data.encode('utf-8')
                if 'Content-Type' not in headers:
                    headers['Content-Type'] = 'text/plain'
        result_row = {
            "Request #": i + 1, "Method": method, "URL": url,
            "Status Code": "N/A", "Response Body": "N/A", "Error": "N/A"
        }
        status_text.text(f"Running request {i+1} of {len(df)}: {method} {url}")
        try:
            response = requests.request(method=method, url=url, headers=headers, **kwargs)
            result_row["Status Code"] = response.status_code
            try:
                result_row["Response Body"] = response.json()
            except requests.exceptions.JSONDecodeError:
                result_row["Response Body"] = response.text
        except Exception as e:
            result_row["Status Code"] = "ERROR"
            result_row["Error"] = str(e)
        results.append(result_row)
        progress_bar.progress((i + 1) / len(df), text=f"Request {i+1} of {len(df)} complete.")
        if i < len(df) - 1:
            time.sleep(delay)
    progress_bar.empty()
    status_text.empty()
    st.success("Batch complete!")
    return pd.DataFrame(results)