from datetime import datetime
import yaml

# ✅
def get_unique_events_dict():
    with open("sem_config.yaml", "r") as f:
        sem_config = yaml.safe_load(f)
    event_names_dict = {}
    for event in sem_config["COURSE_SCHEDULE"]:
        event_name = event['event_name']
        if event_name not in event_names_dict:
            event_names_dict[event_name] = 0
    return event_names_dict

# ✅
def get_attendance(service, semester_class_start_date, semester_class_end_date,cal_id):
    # Variables
    semester_class_start_date = datetime.strptime(semester_class_start_date, "%Y-%m-%d")
    semester_class_end_date = datetime.strptime(semester_class_end_date, "%Y-%m-%d")
    now = datetime.utcnow().isoformat() + "Z"
    # Fetch all events within the semester start date till now (range)
    events = (
        service.events()
        .list(
            calendarId=cal_id,
            timeMin=semester_class_start_date.isoformat() + "Z",
            timeMax=now,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    # Get the list of events happed till now
    events_list = events.get("items", [])

    # Get total no of session held till now of each course
    # add pair value in total_session dictionary with key as course name and value as total no of session held till now
    total_session = get_unique_events_dict()
    attended_session = get_unique_events_dict()

    for event in events_list:
        if event["summary"] in total_session.keys():
            total_session[event["summary"]] += 1
        if event["description"] == "Attended":
            attended_session[event["summary"]] += 1

    print("Attendance Report:")
    print("-------------------")
    for course in total_session.keys():
        total_sessions_held = total_session[course]
        attended_sessions = attended_session[course]
        attendance_percentage = (
            (attended_sessions / total_sessions_held) * 100
            if total_sessions_held > 0
            else 0
        )
        print(f"Course: {course}")
        print(f"Total Sessions Held: {total_sessions_held}")
        print(f"Total Sessions Attended: {attended_sessions}")
        print(f"Attendance Percentage: {attendance_percentage:.2f}%")
        print("-------------------")
    return { "total_session": total_session, "attended_session": attended_session }
# ✅
def get_max_attendance(service, semester_class_start_date, semester_class_end_date,cal_id):
    # Variables
    semester_class_start_date = datetime.strptime(semester_class_start_date, "%Y-%m-%d")
    semester_class_end_date = datetime.strptime(semester_class_end_date, "%Y-%m-%d")
    # Fetch all events within the semester start date till now (range)
    events = (
        service.events()
        .list(
            calendarId=cal_id,
            timeMin=semester_class_start_date.isoformat() + "Z",
            timeMax=semester_class_end_date.isoformat() + "Z",
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    # Get the list of events happed till now
    events_list = events.get("items", [])

    # Get total no of session held till now of each course
    # add pair value in total_session dictionary with key as course name and value as total no of session held till now
    total_session = get_unique_events_dict()
    attended_session = get_unique_events_dict()

    for event in events_list:
        if event["summary"] in total_session.keys():
            total_session[event["summary"]] += 1
        if event["description"] == "Attended":
            attended_session[event["summary"]] += 1

    print("Attendance Report:")
    print("-------------------")
    for course in total_session.keys():
        total_possible_held = total_session[course]
        max_attended_sessions = attended_session[course]
        max_attendance_percentage = (
            (max_attended_sessions / total_possible_held) * 100
            if total_possible_held > 0
            else 0
        )
        print(f"Course: {course}")
        print(f"Total Sessions In Semester: {total_possible_held}")
        # print(f"Total Sessions Attended: {max_attended_sessions}")
        print(f"Max Attendance Percentage: {max_attendance_percentage:.2f}%")
        print("-------------------")
