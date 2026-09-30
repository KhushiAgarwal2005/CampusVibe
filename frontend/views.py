import streamlit as st
from backend.database import (
    login_user, register_user, get_trending_notes, 
    get_specific_resource, submit_note_feedback
)

def render_auth():
    st.markdown("<h1 style='text-align:center;color:#2575fc;'>CampusVibe</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 2, 1]) 
    with col2:
        tab1, tab2 = st.tabs(["🔒 Sign In", "📝 Register"])

        with tab1:
            with st.form("login_form"):
                st.subheader("Sign In")
                email = st.text_input("Email")
                pw = st.text_input("Password", type="password")
                if st.form_submit_button("SIGN IN", type="primary", use_container_width=True):
                    ok, msg = login_user(email, pw)
                    if ok:
                        st.session_state.auth, st.session_state.user_email, st.session_state.user_name = True, email, msg
                        st.rerun()
                    else: st.error(msg)

        with tab2:
            with st.form("register_form"):
                st.subheader("Create New Account")
                new_name = st.text_input("Full Name")
                new_email = st.text_input("Email Address")
                new_pw = st.text_input("Create Password", type="password")
                if st.form_submit_button("REGISTER", use_container_width=True):
                    if not new_name or not new_email or not new_pw:
                        st.warning("Please fill all fields.")
                    else:
                        success, msg = register_user(new_email, new_pw, new_name)
                        if success: st.success(msg)
                        else: st.error(msg)

def render_dashboard(rag_query_engine):
    col_logo, col_search, col_notify = st.columns([2, 6, 1])
    col_logo.markdown("### 🎓 CampusVibe")
    col_search.text_input("Search anything...", label_visibility="collapsed", placeholder="Search for notes...")
    col_notify.markdown("🔔")
    st.markdown("---")

    with st.sidebar:
        st.markdown(f"👋 Welcome, **{st.session_state.user_name}**")
        if st.button("Logout", use_container_width=True): 
            st.session_state.auth = False
            st.rerun()
        st.markdown("### Filters")
        y = st.selectbox("Select Year", ["1st Year", "2nd Year", "3rd Year", "4th Year"])
        s = st.selectbox("Select Semester", ["5th Sem", "6th Sem"] if y == "3rd Year" else ["1st Sem", "2nd Sem"])
        b = st.selectbox("Branch", ["CSE", "ECE", "ME", "CE"])
        if st.button("Submit", use_container_width=True, type="primary"):
            st.session_state.filter_applied, st.session_state.submitted_year, st.session_state.submitted_sem, st.session_state.selected_subject_view, st.session_state.selected_resource_type = True, y, s, None, None
            st.rerun()

    if not st.session_state.filter_applied:
        st.markdown("## 🔥 Trending Notes")
        cols = st.columns(3)
        for i, note in enumerate(get_trending_notes()):
            with cols[i % 3]:
                st.markdown(f"<div class='note-card'><div class='note-title'>📄 {note.get('name')}</div><div class='note-info'>Subject: <b>{note.get('subject')}</b></div></div>", unsafe_allow_html=True)
                st.link_button("⬇️ View/Download", url=note.get("download_url", "#"), use_container_width=True)
                with st.form(key=f"fb_tr_{note['_id']}", clear_on_submit=True):
                    fb_t = st.text_input("Quick Feedback", key=f"it_tr_{note['_id']}")
                    if st.form_submit_button("Submit"): 
                        submit_note_feedback(note['_id'], st.session_state.user_email, fb_t)
                        st.success("Sent!")
    else:
        if st.session_state.submitted_year == "3rd Year" and st.session_state.submitted_sem == "5th Sem":
            if st.session_state.selected_subject_view and st.session_state.selected_resource_type:
                sub = st.session_state.selected_subject_view
                res_type = st.session_state.selected_resource_type
                st.markdown(f"## {sub} - {res_type}")
                if st.button("⬅️ Back to Categories"): st.session_state.selected_resource_type = None; st.rerun()
                
                cols = st.columns(3)
                if res_type == "Notes":
                    for u_num in range(1, 6):
                        data = get_specific_resource(sub, "3rd Year", "5th Sem", "Notes", u_num)
                        with cols[(u_num-1) % 3]:
                            display_name = data.get('name') if data else f"{sub} Unit {u_num}"
                            drive_url = data.get('download_url', '#') if data else "#"
                            st.markdown(f"<div class='note-card'><div class='note-title'>📄 {display_name}</div><div class='note-info'>Subject: <b>{sub}</b><br>Year: <b>3rd Year</b></div></div>", unsafe_allow_html=True)
                            st.link_button("⬇ View/Download", url=drive_url, use_container_width=True)
                            with st.form(key=f"fb_u_{sub}_{u_num}", clear_on_submit=True):
                                fb_val = st.text_input("Quick Feedback", key=f"in_u_{sub}_{u_num}")
                                if st.form_submit_button("Submit"):
                                    if data: 
                                        submit_note_feedback(data['_id'], st.session_state.user_email, fb_val)
                                        st.success("Feedback Saved!")
                                    else: st.warning("Resource not found.")
                else:
                    data = get_specific_resource(sub, "3rd Year", "5th Sem", res_type)
                    with cols[0]:
                        if data:
                            st.markdown(f"<div class='note-card'><div class='note-title'>📂 {res_type}</div><div class='note-info'>Subject: <b>{sub}</b></div></div>", unsafe_allow_html=True)
                            st.link_button("⬇️ View/Download", url=data.get('download_url', '#'), use_container_width=True)
                        else: st.info(f"No {res_type} found.")
            elif st.session_state.selected_subject_view:
                sub = st.session_state.selected_subject_view
                st.markdown(f"## {sub} - Select Category")
                if st.button("⬅️ Back to Subjects"): st.session_state.selected_subject_view = None; st.rerun()
                res_types = ["Notes", "PYQ", "Lab File"]
                cols = st.columns(3)
                for i, r_type in enumerate(res_types):
                    with cols[i % 3]:
                        st.markdown(f"<div class='note-card'><div class='note-title'>📂 {r_type}</div></div>", unsafe_allow_html=True)
                        if st.button(f"Open {r_type}", key=f"btn_res_{r_type}", use_container_width=True):
                            st.session_state.selected_resource_type = r_type; st.rerun()
            else:
                st.markdown("## Choose a Subject")
                if st.button("🏠 Back to Home"): st.session_state.filter_applied = False; st.rerun()
                subs = ["OS", "AI", "Computer Networking", "Deep Learning", "NN"]
                cols = st.columns(3)
                for i, s_name in enumerate(subs):
                    with cols[i % 3]:
                        st.markdown(f"<div class='note-card'><div class='note-title'>📄 {s_name}</div></div>", unsafe_allow_html=True)
                        if st.button(f"Select {s_name}", key=f"btn_s_{s_name}", use_container_width=True):
                            st.session_state.selected_subject_view = s_name; st.rerun()
        else:
            st.warning("Notes for this year/semester are yet to be uploaded.")
            if st.button("🏠 Back to Home"): st.session_state.filter_applied = False; st.rerun()

    # AI CHAT
    st.markdown("---")
    st.markdown("## 🧠 Ask the AI Senior")
    if p := st.chat_input("Ask a question..."):
        st.session_state.messages.append({"role": "user", "content": p})
        if rag_query_engine:
            res = rag_query_engine.query(p)
            st.session_state.messages.append({"role": "assistant", "content": "".join(res.response_gen)})
        st.rerun()
    for m in st.session_state.messages:
        with st.chat_message(m["role"]): st.markdown(m["content"])
