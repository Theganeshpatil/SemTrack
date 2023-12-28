import datetime
import os.path
import yaml
import jwt
import os
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from Functions import course_events, attendance

with open("sem_config.yaml", "r") as f:
    sem_config = yaml.safe_load(f)

CAL_ID = sem_config.get("CAL_ID")
SEM_START_DATE = sem_config.get("SEM_START_DATE")
SEM_END_DATE = sem_config.get("SEM_END_DATE")
COURSE_SCHEDULE = sem_config.get("COURSE_SCHEDULE")
HOLIDAYS = sem_config.get("HOLIDAYS")
MID_SEM_DATES = sem_config.get("MID_SEM_DATES")
SCOPES = ["https://www.googleapis.com/auth/calendar"]

from typing import Union
from fastapi import FastAPI, Body, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Schemas
class AuthCode(BaseModel):
    auth_code: str

app = FastAPI()

origins = [
    "http://localhost:5173",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/auth/url")
async def get_auth_url():
    try:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes=SCOPES)
        flow.redirect_uri = 'http://localhost:5173'
        auth_url, _ = flow.authorization_url()
        return {'auth_url': auth_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def check_new_user(jwt_token):
    create_credentials_from_jwt(jwt_token)
    service = build("calendar", "v3", credentials=create_credentials_from_jwt(jwt_token))
    calender_list = service.calendarList().list().execute()
    calender_name = "SemTrack by Ganesh Patil"
    
    calendar_exists = False
    for item in calender_list.get("items", []):
        if "summary" in item and item["summary"] == calender_name:
            calendar_exists = True
            sem_config["CAL_ID"] = item["id"]
            with open("sem_config.yaml", "w") as f:
                yaml.dump(sem_config, f)
                print("sem config updated with \n ", sem_config)
            break
    # User has never created the calendar & so create a new calender

@app.post("/exchange_code_for_tokens")
async def exchange_code_for_tokens(auth_code: AuthCode):
    print("inside", auth_code)
    try:
        print(1)
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes=SCOPES)
        flow.redirect_uri = 'http://localhost:5173'

        print(auth_code.auth_code)
        flow.fetch_token(code=auth_code.auth_code)
        print(flow.credentials)
        access_token = flow.credentials.token
        refresh_token = flow.credentials.refresh_token 

        jwt_token = jwt.encode({"access_token": access_token, "refresh_token": refresh_token}, 'your-secret-key', algorithm='HS256')
        print(jwt_token)
        check_new_user(jwt_token)
        return {"jwt_token": jwt_token}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))

def create_credentials_from_jwt(jwt_token):
    # Decode the JWT token
    decoded = jwt.decode(jwt_token, 'your-secret-key', algorithms=['HS256'])

    # Extract the access and refresh tokens
    access_token = decoded['access_token']
    refresh_token = decoded['refresh_token']

    # Create the credentials object
    creds = Credentials.from_authorized_user_info({
        'access_token': access_token,
        'refresh_token': refresh_token,
        'client_id': os.getenv('GOOGLE_CLIENT_ID'),
        'client_secret': os.getenv('GOOGLE_CLIENT_SECRET'),
        'token_uri': 'https://oauth2.googleapis.com/token',
    })

    return creds

@app.get("/get_attendance")
def get_attendance(jwt_token: str):
    service = build("calendar", "v3", credentials=create_credentials_from_jwt(jwt_token))
    res = attendance.get_attendance(service, semester_class_start_date = SEM_START_DATE, semester_class_end_date=SEM_END_DATE,cal_id=CAL_ID)
    return {"attendance": res}
    

