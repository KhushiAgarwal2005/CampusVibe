import streamlit as st

def inject_custom_css():
    st.markdown("""
        <style>
        .note-card { background-color: #f4f0ff; padding: 1.2rem; border-radius: 12px; margin-bottom: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.05); height: 260px; border: 1px solid #e0e0e0; display: flex; flex-direction: column; justify-content: center; text-align: center; } 
        .note-title { font-weight: 700; font-size: 1.1rem; color: #2575fc; } 
        .note-info { font-size: 0.92rem; color: #555; }
        </style>
        """, unsafe_allow_html=True)
