# Digital Forensics Tool

A Digital Forensics Tool built specifically to run on MacOS based systems due to lack of supported software.  
This tool is mainly aimed for preliminary analysis of crime scenes and helping maintain Chain of Custody. 

# Technologies Used
- Python
- MySQL
- Streamlit
- YoloV8

# Features
- Object Detection for identifying Digital Evidences 
- Digital Forensics for SD Cards and USB Devices
- Maintain chain of custody by access control 
- Suggesting plan of action for devices
- Report Generation to maintain chain of custody and provide comprehsnive information.
- Dedicated Sign Up page for onbarding new CSI's

# Usage 
First set up the database, then
In auth.py edit
```
password="REPLACE_WITH_MYSQL_PASSWORD"
```
and in all the pages edit
```
base_dir = "PATH_TO_STORE_CASE_DIRECTORY"
```
In the project directory
```
pip install -r requirements.txt
```
And then to start the application

```
streamlit run app.py
```

To view the application, in a browser go to
```
localhost:8501
```

# Future Scope
- Enable remote logging to firebase
- Add functionality using Sleuth Kit
- Extend for all OS'
  
# Working 
### Home Page
<img width="1508" alt="Screenshot 2024-04-20 at 3 11 00 PM" src="https://github.com/krishshah17/Digital-Forensics-Tool/assets/26605210/53d66ccb-2f21-4e47-b1cc-99e6da1370db">  

### Sign Up Page
<img width="1512" alt="Screenshot 2024-04-20 at 3 11 07 PM" src="https://github.com/krishshah17/Digital-Forensics-Tool/assets/26605210/e194496f-9784-4c2e-90e9-9016f3bbb1a2">

### Login Page
<img width="1511" alt="Screenshot 2024-04-20 at 3 13 41 PM" src="https://github.com/krishshah17/Digital-Forensics-Tool/assets/26605210/5bd5420e-e117-41c2-adeb-a324d8deddcc">

### Identify Digital Evidence 
<img width="1511" alt="Screenshot 2024-04-20 at 3 14 07 PM" src="https://github.com/krishshah17/Digital-Forensics-Tool/assets/26605210/e0d0afc9-2c3d-4f54-8988-f5630d13629d">

### SD Card Forensics 
<img width="1512" alt="Screenshot 2024-04-20 at 3 14 16 PM" src="https://github.com/krishshah17/Digital-Forensics-Tool/assets/26605210/d2a6032d-aa96-4aa0-b156-deed14743cd6">

### USB Forensics 
<img width="1509" alt="Screenshot 2024-04-20 at 3 14 24 PM" src="https://github.com/krishshah17/Digital-Forensics-Tool/assets/26605210/1e3d3221-49a9-410a-9eb7-6fe812475b70">

### Generate Report
<img width="1512" alt="Screenshot 2024-04-20 at 3 13 59 PM" src="https://github.com/krishshah17/Digital-Forensics-Tool/assets/26605210/440ba95a-5622-4d47-9107-0cfdc4410d3d">

An example report is included for Case 3


