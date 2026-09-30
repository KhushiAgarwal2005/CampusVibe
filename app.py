import streamlit as st
from frontend.components import inject_custom_css
from frontend.views import render_auth, render_dashboard
from backend.rag_engine import rag_query_engine

# Session Defaults
keys = [
    "auth",
    "user_email",
    "user_name",
    "filter_applied",
    "submitted_year",
    "submitted_sem",
    "selected_subject_view",
    "selected_resource_type",
]
for key in keys:
    if key not in st.session_state:
        st.session_state[key] = (
            False if "applied" in key or "auth" in key else None
        )
if "messages" not in st.session_state:
    st.session_state.messages = []

st.set_page_config(page_title="CampusVibe", layout="wide")
inject_custom_css()

if not st.session_state.auth:
    render_auth()
else:
    render_dashboard(rag_query_engine)
