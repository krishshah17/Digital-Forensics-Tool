import streamlit as st
import subprocess
import datetime
import threading
from backend import *

st.title("Digital Forensics for SD Cards")
st.write("Understand your physical device better")

case_num = st.text_input("Case number:")
evidence_num = st.text_input("Evidence number:")
unq_desc = st.text_input("Unique description:")
notes = st.text_input("Notes:")

base_dir = "PATH_TO_STORE_CASE_DIRECTORY"
directory_path = os.path.join(base_dir, case_num)

# Create the directory if it doesn't exist
os.makedirs(directory_path, exist_ok=True)

return_disks = subprocess.check_output("diskutil list", shell=True).decode("utf-8")
st.code(return_disks, language='text')

dev_addr = st.text_input("Enter your device from the above list:")

if st.button("Run Forensics"):
    st.write(f"Running Forensics on device {dev_addr}")
    st.write("Basic Information about Physical device:")
    
    disk_info_output = subprocess.check_output(f"diskutil info {dev_addr} | grep -E 'Device / Media Name:|Protocol:|Disk Size:|Device Block Size:' | awk -F': +\' '{{print $2}}'", shell=True).decode("utf-8").split("\n")

    st.write(f"Device/Media Name: {disk_info_output[0]}")
    st.write(f"Protocol: {disk_info_output[1]}")
    st.write(f"Disk Size: {disk_info_output[2]}")
    st.write(f"Device Block Size: {disk_info_output[3]}")

    st.write(f"Device/Media Name: {disk_info_output[0]}\nProtocol: {disk_info_output[1]}\nDisk Size: {disk_info_output[2]}\nDevice Block Size: {disk_info_output[3]}")

    # make_image_func(dev_addr, disk_info_output[3].split(" ")[0])

    file_name = os.path.join(directory_path, f"{case_num}-{evidence_num}-{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.txt")
    with open(file_name, 'w') as file:
        file.write("Date and Time: " + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n\n")
        file.write("Case Number: " + case_num + "\n")
        file.write("Evidence Number: " + evidence_num + "\n")
        file.write("Unique Description: " + unq_desc + "\n")
        file.write("Notes: " + notes + "\n\n")
        file.write("Device Information:\n")
        file.write("Device/Media Name: " + disk_info_output[0] + "\n")
        file.write("Protocol: " + disk_info_output[1] + "\n")
        file.write("Disk Size: " + disk_info_output[2] + "\n")
        file.write("Device Block Size: " + disk_info_output[3] + "\n")

    st.write(f"Generated report saved at {file_name}")
