from ..yaml_imports import *
from ..google_imports import *
from fastapi import HTTPException
import yaml
import jwt
import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv('JWT_SECRET')
class AuthService:
    def get_auth_url(self):
        try:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", scopes=SCOPES)
            flow.redirect_uri = 'http://localhost:5173'
            auth_url, _ = flow.authorization_url()
            return {'auth_url': auth_url}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def exchange_code_for_tokens(self, auth_code):
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

            jwt_token = jwt.encode({"access_token": access_token, "refresh_token": refresh_token}, JWT_SECRET, algorithm='HS256')
            print(jwt_token)
            self.check_new_user(jwt_token)
            return {"jwt_token": jwt_token}
        except Exception as e:
            print(e)
            # raise HTTPException(status_code=500, detail=str(e))
            return {"msg": "error while exchanging code for tokens"}

    def check_new_user(self, jwt_token):
        self.create_credentials_from_jwt(jwt_token)
        service = build("calendar", "v3", credentials=self.create_credentials_from_jwt(jwt_token))
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

    def create_credentials_from_jwt(self, jwt_token):
        if jwt_token is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        decoded = jwt.decode(jwt_token, JWT_SECRET, algorithms=['HS256'])

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