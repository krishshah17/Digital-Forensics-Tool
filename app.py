import streamlit as st
from pathlib import Path
from time import sleep
import subprocess
import sys
from main.backend import *
from main.auth import *
import streamlit_authenticator as stauth
import pickle
import subprocess
import sys

st.set_page_config(page_title="DF Tool",layout="wide",initial_sidebar_state="collapsed")

st.header("Digital Forensics Tool",divider='red')

usernames,emails,passwords=auth_helper()
sub_clicked=False
reset_clicked=False

def update_signup_state():
    st.session_state.sub_clicked=True

def update_reset_state():
    st.session_state.reset_clicked=True

def empty():
    placeholder.empty()
    sleep(0.03)
if "sub_clicked" not in st.session_state:
        st.session_state.sub_clicked = False
if "reset_clicked" not in st.session_state:
    st.session_state.reset_clicked = False
placeholder = st.empty()
with placeholder.container():
    st.markdown('''<h2>Digital Forensics </h2>''', unsafe_allow_html=True)
    st.markdown('''<h2>Made Easy.</h2><br>''', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        st.button("Sign Up Now!   ", on_click=update_signup_state)
    with col2:
        login = st.button("Login!")

# Handle sign up button click
if st.session_state.sub_clicked:
    empty()

    with placeholder.container():
        with st.form("RegistrationForm", clear_on_submit=True):
            st.title("Registration Form")

            user_col, super_col = st.columns(2)
            username = user_col.text_input("Name:")

            email_col, mob_col = st.columns([3, 1])
            email = email_col.text_input("Email ID:")
            mob = mob_col.text_input("Mob Number:")

            pw, pw2 = st.columns(2)
            password = pw.text_input("Password", type="password")
            password2 = pw2.text_input("Re-enter Password", type="password")

            submitted = st.form_submit_button("Submit")

            if submitted:
                if(username):
                    if(username in usernames):
                        st.write("Username already exists, please refresh and try again.")
                    elif(email in emails):
                        st.write("User with this email is already registered, please login.")
                        subprocess.run(["streamlit", "run", "main/Overview.py"])
                    elif(password!=password2):
                        st.write("Passwords donot match, please refresh and try again.")
                    # if((email not in emails) and (password==password2)):
                    else:
                        new_id=insert_user(username,password2,email,mob)
                        gen_keys()
                        st.write(f"Thank you for registering your User_ID is: {new_id}")
                        subprocess.run(["streamlit", "run", "main/Overview.py"])
                        sys.exit()
                else:
                    st.error("Please enter a username")

# Handle login button click
elif login:
    subprocess.run(["streamlit", "run", "main/Overview.py"])
    sys.exit()
