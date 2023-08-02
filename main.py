import datetime
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from Functions import course_events, attendance

SCOPES = ["https://www.googleapis.com/auth/calendar"]


def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)

        options = [
            "1. Create Course Events",
            "2. Delete All Events",
            "3. Get Events",
            "4. Get Attendance",
            "5. Get Maximum Possible Attendance",
            "6. Delete Events on Date",
            "7. Mark Absent for Events on Date",
            "8. Remove Sessions of holidays",
            "0. Exit",
        ]

        while True:
            print("\nSelect an option:")
            for option in options:
                print(option)
            choice = input("Enter your choice (0-7): ")

            if choice == "1":
                course_events.create_course_events(service)
            elif choice == "2":
                course_events.delete_all_events(service)
            elif choice == "3":
                get_events(service)
            elif choice == "4":
                attendance.get_attendance(service)
            elif choice == "5":
                attendance.get_max_attendance(service)
            elif choice == "6":
                date = input("Enter the date in YYYY-MM-DD format: ")
                course_events.delete_events_on_date(service=service, date=date)
            elif choice == "7":
                date_start = input("Enter the date in YYYY-MM-DD format: ")
                date_end = input("Enter the date in YYYY-MM-DD format (Leave Blank for one day Absent): ")
                reason = input("Enter the reason for being absent: ")
                course_events.absent_events_on_date(
                    service=service, date_start=date_start, date_end=date_end, reason=reason
                )
            elif choice == "8":
                course_events.remove_sessions_on_holidays(service)
            elif choice == "0":
                break
            else:
                print("Invalid choice. Please enter a valid option (0-8).")

    except HttpError as error:
        print("An error occurred: %s" % error)


if __name__ == "__main__":
    main()
