import streamlit as st
from backend import *
from auth import *

st.title("Generate Digital Forensics Report")
st.divider()

user_id=st.session_state.userid

with st.form("ReportForm",clear_on_submit=True):
	case_num = st.text_input("Case number:")
	base_dir = "PATH_TO_STORE_CASE_DIRECTORY"
	reportpath = os.path.join(base_dir, case_num)

	# Create the directory if it doesn't exist
	os.makedirs(reportpath, exist_ok=True)
	submitted=st.form_submit_button()
	csi_info=get_user_info(user_id)
	if submitted:
		if os.path.exists(reportpath):
			save_path=generate_pdf_from_files(reportpath,csi_info)
			st.write(f"Generated Report saved at {save_path}")
