import streamlit as st
import os
import shutil
from backend import detect_digital_artifacts

st.title("Identify Digital Devices")
st.divider()

user_id = st.session_state.userid

with st.form("ImageForm", clear_on_submit=True):
	case_num = st.text_input("Case number:")
	base_dir = "PATH_TO_STORE_CASE_DIRECTORY"
	directory_path = os.path.join(base_dir, case_num)

	# Create the directory if it doesn't exist
	os.makedirs(directory_path, exist_ok=True)

	img_path = st.text_input("Enter Image Path")
	submitted = st.form_submit_button()

	if submitted:
		image_name = os.path.basename(img_path)
		destination_path = os.path.join(directory_path, image_name)
		shutil.copy(img_path, destination_path)
		annotated_image_path, object_counts = detect_digital_artifacts(destination_path,directory_path)
		st.write(object_counts)
		st.write(f"Annotated image saved at {annotated_image_path}")
        
