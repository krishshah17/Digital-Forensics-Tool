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
  
