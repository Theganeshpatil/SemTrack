from datetime import datetime, timedelta
from googleapiclient.discovery import build

from dotenv import load_dotenv
import os

load_dotenv()
CAL_ID = os.environ.get("CAL_ID")
SEM_START_DATE = os.environ.get("SEM_START_DATE")
SEM_END_DATE = os.environ.get("SEM_END_DATE")

# Variables
semester_class_start_date = datetime.strptime(SEM_START_DATE, "%Y-%m-%d")
semester_class_end_date = datetime.strptime(SEM_END_DATE, "%Y-%m-%d")
now = datetime.datetime.utcnow().isoformat() + "Z"

def get_events(service):
    print("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId=CAL_ID,
            timeMin=now,
            maxResults=10,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    events = events_result.get("items", [])

    if not events:
        print("No upcoming events found.")
        return

    # Prints the start and name of the next 10 events
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        print(start, event["summary"])



def create_course_events(service):
    # Define the courses schedule with their respective week day, start time, end time, and event name
    course_schedule = [
        # Classes
        {
            "day": "MO",
            "start_time": "09:00:00",
            "end_time": "09:55:00",
            "event_name": "CBS 311 LS",
        },
        {
            "day": "TU",
            "start_time": "09:00:00",
            "end_time": "09:55:00",
            "event_name": "CBS 311 LS",
        },
        {
            "day": "WE",
            "start_time": "09:00:00",
            "end_time": "09:55:00",
            "event_name": "CBS 312 GBC",
        },
        {
            "day": "TH",
            "start_time": "09:00:00",
            "end_time": "09:55:00",
            "event_name": "IMA 313 BA",
        },
        {
            "day": "FR",
            "start_time": "09:00:00",
            "end_time": "09:55:00",
            "event_name": "IEC 312 ES",
        },
        {
            "day": "WE",
            "start_time": "10:00:00",
            "end_time": "10:55:00",
            "event_name": "IMA 313 BA",
        },
        {
            "day": "TH",
            "start_time": "10:00:00",
            "end_time": "10:55:00",
            "event_name": "CBS 312 GBC",
        },
        {
            "day": "FR",
            "start_time": "10:00:00",
            "end_time": "10:55:00",
            "event_name": "IHS 314 SKJ",
        },
        {
            "day": "MO",
            "start_time": "10:00:00",
            "end_time": "10:55:00",
            "event_name": "CBE 311 VP",
        },
        {
            "day": "TH",
            "start_time": "11:05:00",
            "end_time": "12:00:00",
            "event_name": "IHS 314 SKJ",
        },
        {
            "day": "FR",
            "start_time": "11:05:00",
            "end_time": "12:00:00",
            "event_name": "CBS 312 GBC",
        },
        {
            "day": "MO",
            "start_time": "12:05:00",
            "end_time": "13:00:00",
            "event_name": "CBS 311 LS",
        },
        {
            "day": "TU",
            "start_time": "12:05:00",
            "end_time": "13:00:00",
            "event_name": "IEC 312 ES",
        },
        {
            "day": "WE",
            "start_time": "12:05:00",
            "end_time": "13:00:00",
            "event_name": "CBE 311 VP",
        },
        {
            "day": "TH",
            "start_time": "12:05:00",
            "end_time": "13:00:00",
            "event_name": "CBE 312 ER",
        },
        {
            "day": "FR",
            "start_time": "12:05:00",
            "end_time": "13:00:00",
            "event_name": "IMA 313 BA",
        },
        {
            "day": "MO",
            "start_time": "14:00:00",
            "end_time": "14:55:00",
            "event_name": "IEC 312 ES",
        },
        {
            "day": "TU",
            "start_time": "14:00:00",
            "end_time": "14:55:00",
            "event_name": "CBE 311 VP",
        },
        {
            "day": "WE",
            "start_time": "14:00:00",
            "end_time": "14:55:00",
            "event_name": "IHS 314 SKJ",
        },
        # Labs
        {
            "day": "MO",
            "start_time": "15:00:00",
            "end_time": "17:00:00",
            "event_name": "CBE 311 LAB VP",
        },
        {
            "day": "TU",
            "start_time": "15:00:00",
            "end_time": "17:00:00",
            "event_name": "IEC 312 LAB ES",
        },
        {
            "day": "WE",
            "start_time": "15:00:00",
            "end_time": "17:00:00",
            "event_name": "CBS 312 LAB GBC",
        },
    ]


    for course in course_schedule:
        # Calculate the class start and end time for each day
        class_start_time = datetime.strptime(course["start_time"], "%H:%M:%S").time()
        class_end_time = datetime.strptime(course["end_time"], "%H:%M:%S").time()

        # Calculate the start and end datetime for the event based on the class date and time
        class_start_datetime = datetime.combine(
            semester_class_start_date, class_start_time
        )
        class_end_datetime = datetime.combine(semester_class_start_date, class_end_time)

        event = {
            "summary": course["event_name"],
            "description": "Attended",
            "start": {
                "dateTime": class_start_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                "timeZone": "Asia/Kolkata",
            },
            "end": {
                "dateTime": class_end_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                "timeZone": "Asia/Kolkata",
            },
            "recurrence": [
                f'RRULE:FREQ=WEEKLY;BYDAY={course["day"]};UNTIL={semester_class_end_date.strftime("%Y%m%d")}',
            ],
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 24 * 60},
                    {"method": "popup", "minutes": 10},
                ],
            },
            "colorId": 6,
        }

        event = service.events().insert(calendarId=CAL_ID, body=event).execute()
        print("Event created: %s" % (event.get("htmlLink")))


def delete_all_events(service):
    
    # Fetch all events within the semester date range
    events = (
        service.events()
        .list(
            calendarId=CAL_ID,
            timeMin=semester_class_start_date.isoformat() + "Z",
            timeMax=semester_class_end_date.isoformat() + "Z",
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
    print(events)
    print(
        "events",
        semester_class_start_date.isoformat() + "Z",
        semester_class_end_date.isoformat() + "Z",
    )
    events_list = events.get("items", [])
    print(events_list)
    # Delete each event one by one
    counter = 0
    for event in events_list:
        event_id = event["id"]
        service.events().delete(calendarId=CAL_ID, eventId=event_id).execute()
        print(
            f"Event deleted: {event['summary']} : {(counter)*100 /len(events['items'])} % completed"
        )
        counter += 1
    print(f"Deleted {counter} events")


def delete_events_on_date(service, date):
    """Delete all events on a given date

    Args: date (str): Date in YYYY-MM-DD format"""
    # Fetch all events on that date
    date_format = datetime.strptime(date, "%Y-%m-%d")
    start_of_day = datetime(
        date_format.year, date_format.month, date_format.day, 0, 0, 0
    )
    end_of_day = datetime(
        date_format.year, date_format.month, date_format.day, 23, 59, 59
    )

    events = (
        service.events()
        .list(
            calendarId=CAL_ID,
            timeMin=start_of_day.isoformat() + "Z",
            timeMax=end_of_day.isoformat() + "Z",
            singleEvents=True,
        )
        .execute()
    )

    events_list = events.get("items", [])
    count_events = 0
    for event in events_list:
        event_id = event["id"]
        service.events().delete(calendarId=CAL_ID, eventId=event_id).execute()
        count_events += 1

    print(f"Deleted {count_events} events on", date)


def absent_events_on_date(service, date_start, date_end, reason):
    """Mark absent on all events of a given date

    Args: date (str): Date in YYYY-MM-DD format"""
    # Fetch all events on that date
    date_start_format = datetime.strptime(date_start, "%Y-%m-%d")
 
    if not date_end:
        date_end_format = date_start_format
    else:
        date_end_format = datetime.strptime(date_end, "%Y-%m-%d")
    start_of_day = datetime(
        date_start_format.year, date_start_format.month, date_start_format.day, 0, 0, 0
    )
    end_of_day = datetime(
        date_end_format.year, date_end_format.month, date_end_format.day, 23, 59, 59
    )
    print(start_of_day, end_of_day)
    events = (
        service.events()
        .list(
            calendarId=CAL_ID,
            timeMin=start_of_day.isoformat() + "Z",
            timeMax=end_of_day.isoformat() + "Z",
            singleEvents=True,
        )
        .execute()
    )

    events_list = events.get("items", [])
    count_events = 0
    for event in events_list:
        event_id = event["id"]
        event["description"] = f"Absent due to {reason}"
        # print(event)
        service.events().update(
            calendarId=CAL_ID, eventId=event_id, body=event
        ).execute()
        count_events += 1

    print(
        f"Marked Absent for {count_events} events from", date_start_format.strftime("%Y-%m-%d")
    )


def remove_sessions_on_holidays(service):
    holidays = ["2023-08-15", "2023-08-29", "2023-09-27", "2023-10-02", "2023-10-23", "2023-10-24", "2023-11-12"]
    for holiday in holidays:
        delete_events_on_date(service, holiday)