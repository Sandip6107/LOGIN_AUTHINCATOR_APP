import streamlit as st
import auth
from db import execute_query
import time

# Page Config
st.set_page_config(page_title="Login Discovery", page_icon="🔐", layout="centered")

# Custom CSS for Premium Look
st.markdown("""
<style>
    .main {
        background-color: #f0f2f5;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #1877f2;
        color: white;
        font-weight: bold;
    }
    .stTextInput>div>div>input {
        border-radius: 5px;
    }
    .auth-card {
        background-color: white;
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_data' not in st.session_state:
    st.session_state.user_data = None
if 'page' not in st.session_state:
    st.session_state.page = 'login'

def switch_page(page_name):
    st.session_state.page = page_name
    st.rerun()

def handle_login(email, password):
    user, msg = auth.login_user(email, password)
    if user:
        st.session_state.logged_in = True
        st.session_state.user_data = user
        st.success(msg)
        time.sleep(1)
        st.rerun()
    else:
        st.error(msg)

def handle_register(name, email, mobile, password):
    success, msg = auth.register_user(name, email, mobile, password)
    if success:
        st.success(msg)
        time.sleep(1)
        switch_page('login')
    else:
        st.error(msg)

# Navigation
if st.session_state.logged_in:
    # --- DASHBOARD ---
    st.title("🔐 Login Authentication System")
    st.divider()
    st.subheader(f"👋 Welcome, {st.session_state.user_data['full_name']}!")
    st.write(f"Logged in as: **{st.session_state.user_data['role'].capitalize()}**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("View Profile"):
            st.info(f"Name: {st.session_state.user_data['full_name']}\n\nEmail: {st.session_state.user_data['email']}\n\nMobile: {st.session_state.user_data['mobile']}")
            
    if st.session_state.user_data['role'] == 'admin':
        st.divider()
        st.subheader("🛡️ Admin Panel")
        if st.button("List All Users"):
            users = execute_query("SELECT full_name, email, role, status FROM users", fetch=True)
            if users:
                st.table(users)
            else:
                st.write("No users registered.")

    st.divider()
    if st.button("Log Out", type="secondary"):
        st.session_state.logged_in = False
        st.session_state.user_data = None
        st.rerun()

else:
    # --- AUTH SCREENS ---
    st.markdown("<h1 style='text-align: center; color: #1c1e21;'>🔐 Login Authentication System</h1>", unsafe_allow_html=True)
    st.write("") # Spacer
    
    if st.session_state.page == 'login':
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.title("🔐 Login")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        
        if st.button("Log In"):
            handle_login(email, password)
            
        st.write("---")
        if st.button("Create New Account"):
            switch_page('register')
        st.markdown('</div>', unsafe_allow_html=True)

    elif st.session_state.page == 'register':
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.title("📝 Sign Up")
        st.write("It's quick and easy.")
        
        new_name = st.text_input("Full Name")
        new_email = st.text_input("Email")
        new_mobile = st.text_input("Mobile Number")
        new_password = st.text_input("Password", type="password")
        
        if st.button("Sign Up"):
            if all([new_name, new_email, new_mobile, new_password]):
                handle_register(new_name, new_email, new_mobile, new_password)
            else:
                st.warning("Please fill all fields")
                
        st.write("---")
        if st.button("Already have an account?"):
            switch_page('login')
        st.markdown('</div>', unsafe_allow_html=True)
