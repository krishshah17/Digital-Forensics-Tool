import cv2
import os
import numpy as np
from ultralytics import YOLO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Image, Paragraph, Spacer, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from PIL import Image as PILImage
import tempfile
import firebase_admin
from firebase_admin import credentials, db
forensic_descriptions = {
	"tv": (
		"Data Acquisition: Establish Chain of Custody. "
		"Data Acquisition: Identify Storage Medium (e.g., flash memory). "
		"Data Acquisition: Choose Acquisition Method (e.g., eMMC five-wire method). "
		"Data Acquisition: Acquire Data using write-blocking techniques. "
		"Digital Traces Analysis: Maintain Chain of Custody. "
		"Digital Traces Analysis: Utilize Forensic Tools (e.g., EnCase). "
		"Digital Traces Analysis: Retrieve Relevant Traces (e.g., system information, network details). "
		"File System Analysis: Document Examination. "
		"File System Analysis: Analyze Partition Scheme and File Systems (e.g., SquashFS). "
		"File System Analysis: Review Boot Images (e.g., U-boot). "
		"File System Analysis: Identify Partition Redundancy."
	),
	"laptop": (
		"Initial Documentation and Evidence Log: Create a detailed evidence log documenting all actions and transfers. "
		"Initial Documentation and Evidence Log: Securely store the evidence log and maintain a clear chain of custody. "
		"Short-Term Memory (RAM) Analysis: Extract data from RAM promptly to capture recent computer activities. "
		"Short-Term Memory (RAM) Analysis: Use tools like Volatility or Redline for RAM analysis. "
		"Short-Term Memory (RAM) Analysis: Document all RAM extraction actions and maintain the chain of custody. "
		"Long-Term Storage Device Preservation: Create exact copies of the data on write-once optical media. "
		"Long-Term Storage Device Preservation: Seal the original storage medium and transfer it to a responsible party. "
		"Long-Term Storage Device Preservation: Maintain locked containers with verified copies for distribution. "
		"Live Forensic Process: Document all actions during live system analysis. "
		"Live Forensic Process: Use tools like FTK Imager or Helix3 for live system analysis. "
		"Live Forensic Process: Establish a trusted network repository and document all transfers. "
		"Live Forensic Process: Maintain the chain of custody for any extracted or transferred data. "
		"Disk Imaging: Use specialized tools like EnCase or X-Ways Forensics for forensic-grade disk imaging. "
		"Disk Imaging: Ensure correct recognition of physical parameters. "
		"Disk Imaging: Perform cryptographic verification before and after imaging. "
		"Disk Imaging: Document all imaging steps and maintain the chain of custody."
	),
	"mouse": (
		"Data Acquisition: Establish Chain of Custody. "
		"Data Acquisition: Identify the Mouse Interface (e.g., USB, Bluetooth). "
		"Data Acquisition: Choose Acquisition Method (e.g., USB data extraction, Bluetooth packet capture). "
		"Data Acquisition: Acquire Data using write-blocking techniques if applicable. "
		"Digital Traces Analysis: Maintain Chain of Custody. "
		"Digital Traces Analysis: Utilize Forensic Tools (e.g., Volatility, USBDeview). "
		"Digital Traces Analysis: Retrieve Relevant Traces (e.g., mouse movement patterns, clicks, device identification). "
		"Device Analysis: Document Examination. "
		"Device Analysis: Analyze Device Metadata (e.g., manufacturer, model, serial number). "
		"Device Analysis: Review Connection History and Timestamps. "
		"Device Analysis: Identify Interaction Patterns (e.g., usage frequency, timestamps of usage)."
	),
	"keyboard": (
		"Data Acquisition: Establish Chain of Custody. "
		"Data Acquisition: Identify the Keyboard Interface (e.g., USB for wired, Bluetooth for wireless). "
		"Data Acquisition: Choose Acquisition Method (e.g., USB data extraction, Bluetooth packet capture). "
		"Data Acquisition: Acquire Data using write-blocking techniques if applicable. "
		"Digital Traces Analysis: Maintain Chain of Custody. "
		"Digital Traces Analysis: Utilize Forensic Tools (e.g., Volatility, USBDeview). "
		"Digital Traces Analysis: Retrieve Relevant Traces (e.g., keystrokes, keylogging data, device identification). "
		"Device Analysis: Document Examination. "
		"Device Analysis: Analyze Device Metadata (e.g., manufacturer, model, serial number). "
		"Device Analysis: Review Connection History and Timestamps. "
		"Device Analysis: Identify Interaction Patterns (e.g., frequency of key presses, timestamps of usage)."
	),
	"microwave": (
		"Data Acquisition: Establish Chain of Custody. "
		"Data Acquisition: Identify the IoT Communication Protocol (e.g., Wi-Fi, Bluetooth, Zigbee). "
		"Data Acquisition: Choose Acquisition Method (e.g., network packet capture, device memory extraction). "
		"Data Acquisition: Acquire Data using appropriate techniques ensuring preservation of integrity. "
		"Digital Traces Analysis: Maintain Chain of Custody. "
		"Digital Traces Analysis: Utilize Forensic Tools (e.g., Wireshark, tcpdump). "
		"Digital Traces Analysis: Retrieve Relevant Traces (e.g., cooking history, device settings, network activity). "
		"Device Analysis: Document Examination. "
		"Device Analysis: Analyze Device Metadata (e.g., manufacturer, model, firmware version). "
		"Device Analysis: Review Network Connections and Logs. "
		"Device Analysis: Identify User Interaction Patterns (e.g., cooking duration, power levels)."
	),
	"oven": (
		"Data Acquisition: Establish Chain of Custody. "
		"Data Acquisition: Identify the IoT Communication Protocol (e.g., Wi-Fi, Bluetooth, Zigbee). "
		"Data Acquisition: Choose Acquisition Method (e.g., network packet capture, device memory extraction). "
		"Data Acquisition: Acquire Data using appropriate techniques ensuring preservation of integrity. "
		"Digital Traces Analysis: Maintain Chain of Custody. "
		"Digital Traces Analysis: Utilize Forensic Tools (e.g., Wireshark, tcpdump). "
		"Digital Traces Analysis: Retrieve Relevant Traces (e.g., cooking history, device settings, network activity). "
		"Device Analysis: Document Examination. "
		"Device Analysis: Analyze Device Metadata (e.g., manufacturer, model, firmware version). "
		"Device Analysis: Review Network Connections and Logs. "
		"Device Analysis: Identify User Interaction Patterns (e.g., cooking duration, power levels)."
	),
	"toaster": (
		"Data Acquisition: Establish Chain of Custody. "
		"Data Acquisition: Identify the IoT Communication Protocol (e.g., Wi-Fi, Bluetooth, Zigbee). "
		"Data Acquisition: Choose Acquisition Method (e.g., network packet capture, device memory extraction). "
		"Data Acquisition: Acquire Data using appropriate techniques ensuring preservation of integrity. "
		"Digital Traces Analysis: Maintain Chain of Custody. "
		"Digital Traces Analysis: Utilize Forensic Tools (e.g., Wireshark, tcpdump). "
		"Digital Traces Analysis: Retrieve Relevant Traces (e.g., cooking history, device settings, network activity). "
		"Device Analysis: Document Examination. "
		"Device Analysis: Analyze Device Metadata (e.g., manufacturer, model, firmware version). "
		"Device Analysis: Review Network Connections and Logs. "
		"Device Analysis: Identify User Interaction Patterns (e.g., cooking duration, power levels)."
	),
	"cell phone": (
		"Cellphone Identification: Establish the purpose and scope of identification to locate relevant digital evidence. "
		"Cellphone Identification: Recognize that data may extend beyond the device to cloud accounts or other devices. "
		"Cellphone Identification: Document comprehensively to avoid errors that could compromise evidence. "
		"Mobile Phone Collection: Gather physical devices including smartphones and other relevant mobile devices. "
		"Mobile Phone Collection: Protect digital evidence from contamination by isolating devices from users until forensic acquisition. "
		"Mobile Phone Collection: Take measures to isolate devices from data transmission networks to prevent data alteration. "
		"Mobile Phone Acquisition: Perform logical extraction using tools like Cellebrite UFED or Oxygen Forensic Detective to collect active data. "
		"Mobile Phone Acquisition: Conduct file system extraction with tools such as XRY or Magnet AXIOM to access internal memory and retrieve system files, logs, and database files. "
		"Mobile Phone Acquisition: Execute physical extraction using tools like Cellebrite UFED Physical Analyzer or MSAB XAMN to capture the entire contents of the device, including deleted data and unallocated space. "
		"Mobile Phone Acquisition: Analyze backup files created when connecting the phone to a computer using software like iTunes or Oxygen Forensic Detective. "
		"Mobile Phone Acquisition: Utilize tools such as Cellebrite UFED Cloud Analyzer or Oxygen Forensic Cloud Extractor to access and acquire data stored in the cloud. "
		"Cellphone Data Preservation: Maintain a chain of custody using digital evidence management systems like ADF Digital Evidence Investigator or BlackBag BlackLight to protect digital evidence from modification or tampering. "
		"Cellphone Data Preservation: Apply mathematical hashing algorithms with tools like HashCalc or md5deep to create unique hash values, ensuring the integrity of extracted data. "
		"Reporting on Mobile Devices: Prepare reports detailing the data extracted from the mobile device using forensic report generation tools such as XRY or Cellebrite Physical Analyzer, formatted for accessibility and review. "
		"Reporting on Mobile Devices: Create more in-depth reports when necessary to explain timelines, data types, or specific forensic artifacts using tools like Oxygen Forensic Detective or Magnet AXIOM. "
		"Cellphone Forensics Expert Testimony: Select experts with appropriate technical expertise and communication skills. "
		"Cellphone Forensics Expert Testimony: Ensure experts can effectively explain technical concepts and forensic procedures in plain language to judges and juries."
	)
}


model = YOLO("yolov8m.pt")

def detect_digital_artifacts(image_path,destination_path):
	frame = cv2.imread(image_path)
	#frame = cv2.imread('pls_work.jpg')

	results = model(frame)
	# print(results)
	result = results[0]
	# print(result)


	bboxes = np.array(result.boxes.xyxy.cpu(), dtype="int")
	classes = np.array(result.boxes.cls.cpu(), dtype="int")


	classes = [result.names[i] for i in classes]
	object_counts = {
	"tv": 0,
	"laptop": 0,
	"mouse": 0,
	"remote": 0,
	"keyboard": 0,
	"cell phone": 0,
	"microwave": 0,
	"oven": 0,
	"toaster": 0
	}


	for cls, bbox in zip(classes, bboxes):
		if cls in object_counts.keys():
			object_counts[cls] += 1
			(x, y, x2, y2) = bbox
			cv2.rectangle(frame, (x, y), (x2, y2), (0, 0, 255), 2)  # Draw bounding box
			cv2.putText(frame, cls, (x, y - 5), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)  # Display class label


	image_name = image_path[:image_path.rfind(".")]
	annotated_image_path = image_name+"_annotated.jpg"
	cv2.imwrite(annotated_image_path, frame)
	
	object_counts_file_path = annotated_image_path.replace('.jpg', '_counts.txt')
	with open(object_counts_file_path, 'w') as file:
		for key, value in object_counts.items():
			file.write(f"{key}: {value}\n")

	file_path = os.path.join(destination_path,"description_file.txt")
	if os.path.exists(file_path):
		existing_descriptions = set()
		try:
			with open(file_path, 'r') as file:
				for line in file:
					key, description = line.strip().split(": ", 1)
					existing_descriptions.add(description)
		except FileNotFoundError:
			existing_descriptions = set()

		with open(file_path, 'a') as file:
			# Iterate through object_counts
			for item, count in object_counts.items():
				if count > 0:
					description = forensic_descriptions.get(item)
					if description and description not in existing_descriptions:
						file.write(f"{item}: {description}\n\n\n")
						print(f"Key: {item}, Description: {description} written to file.")
						existing_descriptions.add(description)
					elif description:
						print(f"Description for {item}: {description} already exists in the file.")
					else:
						print(f"No description found for {item}.")
	else:
		with open(file_path, "w") as file:
			for item, count in object_counts.items():
				if count > 0:
					description = forensic_descriptions.get(item)
					file.write(f"{item}: {description}\n\n\n")



	
	return annotated_image_path,object_counts;

def resize_image(image_path, max_width, max_height):

	img = PILImage.open(image_path)
	img.thumbnail((max_width, max_height), PILImage.LANCZOS)  # Use LANCZOS for resizing
	return img

def generate_pdf_from_files(directory_path,csi_info):

	
	output_pdf_path=os.path.basename(directory_path)+"_report.pdf"
	doc = SimpleDocTemplate(output_pdf_path, pagesize=letter)

	elements = []


	max_width = 500
	max_height = 700


	elements.append(Paragraph(f"<u>{os.path.basename(directory_path)}</u>", getSampleStyleSheet()["Title"]))
	elements.append(Paragraph("<b>Case report generated by: </b>", getSampleStyleSheet()["BodyText"]))
	elements.append(Spacer(1, 0.3 * inch))  # Add some space between lines
	for key, value in csi_info.items():
		line = f"<b>{key}:</b> {value}"
		elements.append(Paragraph(line, getSampleStyleSheet()["BodyText"]))
		elements.append(Spacer(1, 0.1 * inch))  # Add some space between lines

	elements.append(PageBreak()) 


	for filename in sorted(os.listdir(directory_path)):
		file_path = os.path.join(directory_path, filename)
		if filename.lower().endswith((".jpg", ".png", ".jpeg")):  

			resized_img = resize_image(file_path, max_width, max_height)

			temp_file = tempfile.NamedTemporaryFile(suffix=".jpg", delete=False)
			temp_file_path = temp_file.name
			resized_img.save(temp_file_path)

			elements.append(Paragraph(f"<b>{filename}</b>", getSampleStyleSheet()["Heading2"]))

			elements.append(Image(temp_file_path, width=resized_img.width, height=resized_img.height))
			elements.append(PageBreak())
			temp_file.close()

		elif filename.lower().endswith(".txt"):

			with open(file_path, "r") as f:

				elements.append(Paragraph(f"<b>{filename}</b>", getSampleStyleSheet()["Heading2"]))
				for line in f:
					elements.append(Paragraph(line.strip(), getSampleStyleSheet()["BodyText"]))
			elements.append(PageBreak())
		else:
			print(f"Ignoring {filename}: Unsupported file format")


	doc.build(elements)
	return os.getcwd()+"/"+output_pdf_path

def verify_checksum(filename):
	checksum = subprocess.check_output(["shasum", filename]).decode("utf-8").split()[0]
	st.write(f"SHA checksum of {filename}: {checksum}")

def checksum_func(dev_addr,image_name):
	checksum = st.radio("Would you like to verify SHA checksum of this image?", ("Yes", "No"))
	if checksum == "Yes":
		verify_checksum(dev_addr)
		verify_checksum(image_name)
	else:
		st.write("No checksum will be verified.")
