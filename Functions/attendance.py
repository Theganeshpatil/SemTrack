from datetime import datetime

CAL_ID = 'bc673861aeb99f89350562855352bd12a53b6a14fe84a8046ff57cd0b9dccf78@group.calendar.google.com'

# Define the start and end dates of the semester
semester_class_start_date = datetime.strptime("2023-08-02", "%Y-%m-%d")
semester_class_end_date = datetime.strptime("2023-11-13", "%Y-%m-%d")
now = datetime.utcnow().isoformat() + 'Z' 

def get_attendance(service):
    
    # Fetch all events within the semester start date till now (range)
    events = service.events().list(
        calendarId=CAL_ID,
        timeMin=semester_class_start_date.isoformat() + 'Z',
        timeMax=now,singleEvents=True,orderBy='startTime'
    ).execute()

    # Get the list of events happed till now
    events_list = events.get('items', [])

    # Get total no of session held till now of each course
    total_session = {}
    