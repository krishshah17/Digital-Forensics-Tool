import streamlit as st
import streamlit_authenticator as stauth
from pathlib import Path
import pickle
from backend import *
from auth import *
from time import *

if 'sidebar_state' not in st.session_state:
    st.session_state.sidebar_state = 'collapsed'
if 'userid' not in st.session_state:
	st.session_state.userid=False

st.set_page_config(page_title="DF Tool",layout="wide",initial_sidebar_state=st.session_state.sidebar_state)
st.empty()
sleep(0.03)


file_path=Path(__file__).parent/"hashed_pw.pkl"
with file_path.open("rb") as file:
    hashed_passwords=pickle.load(file)

usernames,email,password=auth_helper()
authenticator=stauth.Authenticate(usernames,email,hashed_passwords,"dftool","dftool",cookie_expiry_days=30)
name,authentication_status,username=authenticator.login("Welcome to the DF Tool","main")

if authentication_status or st.session_state.userid:
	sleep(0.03)
	st.session_state.sidebar_state = 'expanded'
	st.session_state.userid = name
	st.title(f"Welcome {username}")
	authenticator.logout("Logout","sidebar")


if authentication_status==False:
	st.error("Please enter correct emailID/password")
	#st.rerun()