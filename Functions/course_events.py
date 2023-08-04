from datetime import datetime
from googleapiclient.discovery import build

def get_events(service):
    print("Getting the upcoming 10 events")
    events_result = (
        service.events()
        .list(
            calendarId=cal_id,
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


# ✅
def create_course_events(service, semester_class_start_date, semester_class_end_date, course_schedule, cal_id, holidays, mid_sem_dates):
    # Define the courses schedule with their respective week day, start time, end time, and event name
    semester_class_start_date = datetime.strptime(semester_class_start_date, "%Y-%m-%d").date()
    semester_class_end_date = datetime.strptime(semester_class_end_date, "%Y-%m-%d").date()

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
                "useDefault": True,
            },
            'colorId': '4',
        }

        event = service.events().insert(calendarId=cal_id, body=event).execute()
        print("Event created: ", event.get("summary"))

    # Delete extra events created by the recurrence rule on first day of class
    print("Deleting extra events created by the recurrence rule on first day of class")
    date_format = semester_class_start_date
    start_of_day = datetime(
        date_format.year, date_format.month, date_format.day, 0, 0, 0
    )
    end_of_day = datetime(
        date_format.year, date_format.month, date_format.day, 23, 59, 59
    )
    events_on_first_day = (
    service.events()
    .list(
        calendarId=cal_id,
        timeMin=start_of_day.isoformat() + "Z",
        timeMax=end_of_day.isoformat() + "Z",
        singleEvents=True,
    )
    .execute()
    )

    events_on_first_day_list = events_on_first_day.get("items", [])

    # Get the day on first date of semester
    first_day_of_semester = ((semester_class_start_date.strftime("%A"))[0:2]).upper() # Wednesday -> WE 

    for event in events_on_first_day_list:
       # Keep only correct events to do so we check the second instance of the event is on the same day as the first day of semester

        # Get the instance
        recurringEventId = event["recurringEventId"]
        instances = service.events().instances(calendarId=cal_id, eventId=recurringEventId).execute()
        instance = instances['items'][1]
        # Get the start date of the instance
        instance_start_date = (instance["start"].get("dateTime", instance["start"].get("date")))
        instance_start_date = datetime.fromisoformat(instance_start_date.replace("T", " "))
        instance_start_day = ((instance_start_date.strftime("%A"))[0:2]).upper()
        
        if instance_start_day != first_day_of_semester:
            print("Deleting event: ", event.get("summary"))
            service.events().delete(calendarId=cal_id, eventId=event["id"]).execute()

        # Successfully removed extra events created by the recurrence rule on first day of class

    # Delete holidays from the calendar
    remove_sessions_on_holidays(service, holidays=holidays, cal_id=cal_id, )
    remove_sessions_on_holidays(service, holidays=mid_sem_dates, cal_id=cal_id)

    print("Successfully created course events")


def delete_all_events(service, semester_class_start_date, semester_class_end_date, cal_id ):
    semester_class_start_date = datetime.strptime(semester_class_start_date, "%Y-%m-%d").date()
    semester_class_end_date = datetime.strptime(semester_class_end_date, "%Y-%m-%d").date()

    # Convert date objects to datetime objects
    start_datetime = datetime.combine(semester_class_start_date, datetime.min.time())
    end_datetime = datetime.combine(semester_class_end_date, datetime.max.time())
    # Fetch all events within the semester date range
    events = (
        service.events()
        .list(
            calendarId=cal_id,
            timeMin=start_datetime.isoformat() + "Z",
            timeMax=end_datetime.isoformat() + "Z",
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )
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
        service.events().delete(calendarId=cal_id, eventId=event_id).execute()
        print(
            f"Event deleted: {event['summary']} : {(counter)*100 /len(events['items'])} % completed"
        )
        counter += 1
    print(f"Deleted {counter} events")

# ✅
def delete_events_on_date(service, date, cal_id):
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
            calendarId=cal_id,
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
        service.events().delete(calendarId=cal_id, eventId=event_id).execute()
        count_events += 1

    print(f"Deleted {count_events} events on", date)

# ✅
def absent_events_on_date(service, date_start, date_end, reason, cal_id):
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
            calendarId=cal_id,
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
            calendarId=cal_id, eventId=event_id, body=event
        ).execute()
        count_events += 1

    print(
        f"Marked Absent for {count_events} events from", date_start_format.strftime("%Y-%m-%d")
    )

# ✅
def remove_sessions_on_holidays(service, holidays, cal_id):
    for holiday in holidays:
        delete_events_on_date(service, date=holiday, cal_id=cal_id)