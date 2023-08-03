from dotenv import load_dotenv
import os

load_dotenv()

def init_setup():
    os.environ['SEM_START_DATE'] = input("SEM_START_DATE = ")
    os.environ['SEM_END_DATE'] = input("SEM_END_DATE = ")

    course_schedule = []
    while True:
        course_name = input("Enter course name: ")
        if course_name == "":
            break
        course_day = input("Enter course day: ")
        start_time = input("Enter start time: ")
        end_time = input("Enter end time: ")

        course = {
            "day": course_day,
            "start_time": start_time,
            "end_time": end_time,
            "event_name": course_name,
        }
        course_schedule.append(course)
        print("Leave course name blank to stop adding courses.")
    print("Added the courses: ", course_schedule)

    holidays = []
    while True:
        holiday = input("Enter holiday date: (YYYY-MM-DD)")
        if holiday == "":
            break
        holidays.append(holiday)
        print("Leave holiday blank to stop adding holidays.")
    
    mid_sem_dates = []
    while True:
        mid_sem_date = input("Enter mid sem date: (YYYY-MM-DD)")
        if mid_sem_date == "":
            break
        mid_sem_dates.append(mid_sem_date)
        print("Leave mid sem date blank to stop adding mid sem dates.")
    
    os.environ['HOLIDAYS'] = str(holidays)
    os.environ['MID_SEM_DATES'] = str(mid_sem_dates)
    os.environ['COURSE_SCHEDULE'] = str(course_schedule)
