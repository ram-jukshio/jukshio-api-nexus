import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

# ==========================================
# 1. SETUP & CONFIGURATION
# ==========================================
st.set_page_config(page_title="Digital API Library", layout="wide", page_icon="🗂️")

# Ensure this mapping matches your file names in the 'data' folder
DATA_SOURCES = {
    "Defraud & Group Analysis": "data/defrauds.json",
    "Jukshio DKYC (Manappuram)": "data/dkyc.json",
    "DigiLocker Integration": "data/digilocker.json",
    "Verification APIs (NSDL/Govt)": "data/verification.json"
}

# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================
def load_api_data(filepath):
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        return []

# ==========================================
# 3. SIDEBAR NAVIGATION
# ==========================================
st.sidebar.title("📚 Library Categories")
selected_category = st.sidebar.radio("Select Category", list(DATA_SOURCES.keys()))
st.sidebar.markdown("---")
st.sidebar.info("Data loaded from local JSON files.")

# ==========================================
# 4. MAIN CONTENT
# ==========================================
st.title(f"🛠️ {selected_category}")

json_file = DATA_SOURCES[selected_category]
apis = load_api_data(json_file)

if not apis:
    st.error(f"⚠️ Could not load data from {json_file}. Please ensure the file exists in the 'data' folder.")
else:
    for api in apis:
        with st.container():
            st.markdown(f"### {api['title']}")
            
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**Endpoint:** `{api['endpoint']}`")
                st.caption(f"Source: {api['source']}")
            
            with st.expander("Explore API Details", expanded=False):
                st.write(f"**Description:** {api['description']}")
                
                t1, t2, t3 = st.tabs(["📥 Inputs", "💻 cURL", "📤 Response"])
                
                with t1:
                    if api.get("inputs"):
                        st.table(pd.DataFrame(api["inputs"]))
                    else:
                        st.info("No inputs specified.")
                
                with t2:
                    st.code(api["curl"], language="bash")
                
                with t3:
                    st.json(api["outputs"])
            
            st.divider()

# ==========================================
# 5. FOOTER
# ==========================================
st.markdown("---")
current_year = datetime.now().year
footer_html = f"""
<div style='text-align: center; color: #666;'>
    <p>
        Designed and Developed by <a href='mailto:ramarao.bikkina@jukshio.com' style='text-decoration: none; color: #e91e63;'>Ram Bikkina</a> 
        | &copy; {current_year} <a href='http://jukshio.com/' style='text-decoration: none; color: #e91e63;'>Jukshio Org</a>
    </p>
</div>
"""
st.markdown(footer_html, unsafe_allow_html=True)