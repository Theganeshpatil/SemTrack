from datetime import datetime, timedelta
from googleapiclient.discovery import build

CAL_ID = 'bc673861aeb99f89350562855352bd12a53b6a14fe84a8046ff57cd0b9dccf78@group.calendar.google.com'

def create_course_events(service):
    
    # Define the courses schedule with their respective week day, start time, end time, and event name
    course_schedule = [
        # Classes
        {'day': 'MO', 'start_time': '09:00:00', 'end_time': '09:55:00', 'event_name': 'CBS 311 LS'},
        {'day': 'TU', 'start_time': '09:00:00', 'end_time': '09:55:00', 'event_name': 'CBS 311 LS'},
        {'day': 'WE', 'start_time': '09:00:00', 'end_time': '09:55:00', 'event_name': 'CBS 312 GBC'},
        {'day': 'TH', 'start_time': '09:00:00', 'end_time': '09:55:00', 'event_name': 'IMA 313 BA'},
        {'day': 'FR', 'start_time': '09:00:00', 'end_time': '09:55:00', 'event_name': 'IEC 312 ES'},
        {'day': 'WE', 'start_time': '10:00:00', 'end_time': '10:55:00', 'event_name': 'IMA 313 BA'},
        {'day': 'TH', 'start_time': '10:00:00', 'end_time': '10:55:00', 'event_name': 'CBS 312 GBC'},
        {'day': 'FR', 'start_time': '10:00:00', 'end_time': '10:55:00', 'event_name': 'IHS 314 SKJ'},
        {'day': 'MO', 'start_time': '10:00:00', 'end_time': '10:55:00', 'event_name': 'CBE 311 VP'},
        {'day': 'TH', 'start_time': '11:05:00', 'end_time': '12:00:00', 'event_name': 'IHS 314 SKJ'},
        {'day': 'FR', 'start_time': '11:05:00', 'end_time': '12:00:00', 'event_name': 'CBS 312 GBC'},
        {'day': 'MO', 'start_time': '12:05:00', 'end_time': '13:00:00', 'event_name': 'CBS 311 LS'},
        {'day': 'TU', 'start_time': '12:05:00', 'end_time': '13:00:00', 'event_name': 'IEC 312 ES'},
        {'day': 'WE', 'start_time': '12:05:00', 'end_time': '13:00:00', 'event_name': 'CBE 311 VP'},
        {'day': 'TH', 'start_time': '12:05:00', 'end_time': '13:00:00', 'event_name': 'CBE 312 ER'},
        {'day': 'FR', 'start_time': '12:05:00', 'end_time': '13:00:00', 'event_name': 'IMA 313 BA'},
        {'day': 'MO', 'start_time': '14:00:00', 'end_time': '14:55:00', 'event_name': 'IEC 312 ES'},
        {'day': 'TU', 'start_time': '14:00:00', 'end_time': '14:55:00', 'event_name': 'CBE 311 VP'},
        {'day': 'WE', 'start_time': '14:00:00', 'end_time': '14:55:00', 'event_name': 'IHS 314 SKJ'},
        
        # Labs
        {'day': 'MO', 'start_time': '15:00:00', 'end_time': '17:00:00', 'event_name': 'CBE 311 LAB VP'},
        {'day': 'TU', 'start_time': '15:00:00', 'end_time': '17:00:00', 'event_name': 'IEC 312 LAB ES'},
        {'day': 'WE', 'start_time': '15:00:00', 'end_time': '17:00:00', 'event_name': 'CBS 312 LAB GBC'},
    ]

    # Define the start and end dates of the semester
    semester_class_start_date = datetime.strptime("2023-08-02", "%Y-%m-%d")
    semester_class_end_date = datetime.strptime("2023-11-13", "%Y-%m-%d")

    for course in course_schedule:
        # Calculate the class start and end time for each day
        class_start_time = datetime.strptime(course['start_time'], "%H:%M:%S").time()
        class_end_time = datetime.strptime(course['end_time'], "%H:%M:%S").time()

        # Calculate the start and end datetime for the event based on the class date and time
        class_start_datetime = datetime.combine(semester_class_start_date, class_start_time)
        class_end_datetime = datetime.combine(semester_class_start_date, class_end_time)

        
        event = {
            'summary': course['event_name'],
            'description': 'Attended',
            'start': {
                'dateTime': class_start_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': class_end_datetime.strftime("%Y-%m-%dT%H:%M:%S"),
                'timeZone': 'Asia/Kolkata',
            },
            'recurrence': [
                f'RRULE:FREQ=WEEKLY;BYDAY={course["day"]};UNTIL={semester_class_end_date.strftime("%Y%m%d")}',
            ],
            'reminders': {
                'useDefault': False,
                'overrides': [
                    {'method': 'email', 'minutes': 24 * 60},
                    {'method': 'popup', 'minutes': 10},
                ],
            },
            'colorId': 6
        }
        
        event = service.events().insert(calendarId=CAL_ID, body=event).execute()
        print('Event created: %s' % (event.get('htmlLink')))
       


def delete_all_events(service):
    # Define the start and end dates of the semester
    semester_class_start_date = datetime.strptime("2023-08-02", "%Y-%m-%d")
    semester_class_end_date = datetime.strptime("2023-11-13", "%Y-%m-%d")
    now = datetime.utcnow().isoformat() + 'Z' 
    # Fetch all events within the semester date range
    events = service.events().list(
        calendarId=CAL_ID,
        timeMin=semester_class_start_date.isoformat() + 'Z',
        timeMax=semester_class_end_date.isoformat() + 'Z',singleEvents=True,
                                            orderBy='startTime'
    ).execute()
    print(events)
    print("events",semester_class_start_date.isoformat() + 'Z', semester_class_end_date.isoformat() + 'Z' )
    events_list = events.get('items', [])
    print(events_list)
    # Delete each event one by one
    counter = 0
    for event in events_list:
        event_id = event['id']
        service.events().delete(
            calendarId=CAL_ID,
            eventId=event_id
        ).execute()
        print(f"Event deleted: {event['summary']} : {(counter)*100 /len(events['items'])} % completed")
        counter += 1
    print(f"Deleted {counter} events")