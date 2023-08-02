from datetime import datetime

from dotenv import load_dotenv
import os

load_dotenv()
CAL_ID = os.environ.get("CAL_ID")
SEM_START_DATE = os.environ.get("SEM_START_DATE")
SEM_END_DATE = os.environ.get("SEM_END_DATE")

# Variables
semester_class_start_date = datetime.strptime(SEM_START_DATE, "%Y-%m-%d")
semester_class_end_date = datetime.strptime(SEM_END_DATE, "%Y-%m-%d")
now = datetime.utcnow().isoformat() + "Z"


def get_attendance(service):
    # Fetch all events within the semester start date till now (range)
    events = (
        service.events()
        .list(
            calendarId=CAL_ID,
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
    total_session = {
        "CBS 311 LS": 0,
        "CBS 312 GBC": 0,
        "IMA 313 BA": 0,
        "IEC 312 ES": 0,
        "IHS 314 SKJ": 0,
        "CBE 311 VP": 0,
        "CBE 312 ER": 0,
        "CBE 311 LAB VP": 0,
        "IEC 312 LAB ES": 0,
        "CBS 312 LAB GBC": 0,
    }

    attended_session = {
        "CBS 311 LS": 0,
        "CBS 312 GBC": 0,
        "IMA 313 BA": 0,
        "IEC 312 ES": 0,
        "IHS 314 SKJ": 0,
        "CBE 311 VP": 0,
        "CBE 312 ER": 0,
        "CBE 311 LAB VP": 0,
        "IEC 312 LAB ES": 0,
        "CBS 312 LAB GBC": 0,
    }

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


def get_max_attendance(service):
    # Fetch all events within the semester start date till now (range)
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

    # Get the list of events happed till now
    events_list = events.get("items", [])

    # Get total no of session held till now of each course
    # add pair value in total_session dictionary with key as course name and value as total no of session held till now
    total_session = {
        "CBS 311 LS": 0,
        "CBS 312 GBC": 0,
        "IMA 313 BA": 0,
        "IEC 312 ES": 0,
        "IHS 314 SKJ": 0,
        "CBE 311 VP": 0,
        "CBE 312 ER": 0,
        "CBE 311 LAB VP": 0,
        "IEC 312 LAB ES": 0,
        "CBS 312 LAB GBC": 0,
    }

    attended_session = {
        "CBS 311 LS": 0,
        "CBS 312 GBC": 0,
        "IMA 313 BA": 0,
        "IEC 312 ES": 0,
        "IHS 314 SKJ": 0,
        "CBE 311 VP": 0,
        "CBE 312 ER": 0,
        "CBE 311 LAB VP": 0,
        "IEC 312 LAB ES": 0,
        "CBS 312 LAB GBC": 0,
    }

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
