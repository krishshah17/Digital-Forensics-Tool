from datetime import date, datetime, timedelta, timezone

import mysql.connector
from pathlib import Path
import pickle
import streamlit_authenticator as stauth

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="REPLACE_WITH_MYSQL_PASSWORD",
  database="DF"
)

mycursor = mydb.cursor()

add_mainuser_command = ("INSERT INTO User(username, password, email_ID, phone_no) VALUES (%(username)s, %(password)s, %(email_ID)s, %(phone_no)s)")

auth_query = "SELECT User_ID FROM User WHERE email_ID = %s AND password = %s"
main_auth_query="SELECT User_ID,username,password FROM User"

get_user_info_query="SELECT * FROM User WHERE User_ID = %s"

get_last_user_id=("SELECT LAST_INSERT_ID()")

def gen_keys():
  usernames,email,passwords=auth_helper()

  hashed_passwords=stauth.Hasher(passwords).generate()
  file_path=Path(__file__).parent/"hashed_pw.pkl"

  with file_path.open("wb") as file:
    pickle.dump(hashed_passwords,file)

def auth_helper():
  usernames=[]
  email=[]
  password=[]
  mycursor.execute(main_auth_query)
  for x in mycursor:
    #print(x,type(x))
    usernames.append(x[0])
    email.append(x[1])
    password.append(x[2])

  return usernames,email,password

def insert_user(username,password,email_ID,phone_no):
  user_data = {
  "username": username,
  "password": password,
  "email_ID": email_ID,
  "phone_no": phone_no,
  }
  mycursor.execute(add_mainuser_command, user_data)

  mydb.commit()
  mycursor.execute(get_last_user_id)
  new_id=mycursor.fetchone()[0]
  
  return new_id

def auth_user(email,password):
  mycursor.execute(auth_query,(email,password))
  new_id=mycursor.fetchone()
  if(new_id):
    return new_id[0]
  else:
    return False

def get_user_info(user_id):
  mycursor.execute(get_user_info_query,(user_id,))
  info=mycursor.fetchone()
  current_datetime = datetime.now()
  current_timezone = datetime.now(timezone.utc).astimezone().tzinfo
  csi_info = {
  "CSI ID": info[0],
  "Name": info[1],
  "Email ID": info[3],
  "Phone Number": info[4],
  "Date": current_datetime.strftime("%Y-%m-%d"),
  "Time": current_datetime.strftime("%H:%M:%S"),
  "Timezone": str(current_timezone)
  }
  # print(type(csi_info))
  return csi_info


