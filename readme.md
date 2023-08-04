# SemTrack

SemTrack is a Google Calendar manager project, which focuses on attendance tracking and semester calendar management.

# Setup

- Clone the repository to your local machine.
- Install the required dependencies using the command: `pip install -r requirements.txt`.
- Obtain the necessary credentials from the Google Developers Console and save them as credentials.json.
- To get the credentials.json refer to [Set up your environment from Google Calender API docs](https://developers.google.com/calendar/api/quickstart/python#set_up_your_environment)
- Now rename the .env.example file to .env and update it
- Run the script using the command: `python main.py`.

# Usage

- For the first time use of SemTrack
- Update `sem_config.yaml` file as your semester timetable or ask your friends if they have one
- It will create a new calendar name "SemTrack by Ganesh Patil" in your Google Calendar
- If it already exists then it will assume that you've already used this application and won't create events again
- You can modify directly in Google Calendar to add, delete, and update events now

### Features

1. Attendance till date
2. Maximux Attendance possible in the upcoming Semester
3. Mark absent on whole day/s
   - Utilise it to plan future leaves and find out the maximum possible attendance is
4. Delete Events on a particular Date
   - In case any date is declared as a holiday later
5. Delete all events (In case a user wants to start fresh)

# FAQ

### How to mark Absent for a particular class?

Simply change that class's event description in Google Calendar.

### What if the professor doesn't take a class?

Delete that particular event from Google Calender.

### Can I modify events directly in Google Calendar?

Yes, you can directly modify the events in your Google Calendar. SemTrack is designed to work with your Google Calendar, so any changes you make will reflect in SemTrack's attendance calculations.

### How do I plan future leaves and calculate the maximum possible attendance?

Use the "Mark Absent for Events on Date" feature to mark yourself absent for specific dates. Afterward, utilize the "Get Maximum Possible Attendance" feature to calculate the maximum possible attendance for the upcoming semester.

### How do I delete all events in case I want to start fresh?

Use the "Delete All Events" feature in SemTrack to remove all events associated with the semester management.

# Contributing

If you find any issues or have suggestions for improvement, please feel free to open an issue or submit a pull request. Contributions are always welcome!

# Reference

1. Google Calender API
   - https://developers.google.com/calendar/api/quickstart/python
   - https://developers.google.com/calendar/api/v3/reference

# Google Calendar API

This project utilizes the Google Calendar API to interact with your Google Calendar. The API allows the script to read, create, update, and delete events on your calendar. You will need to set up the Google Calendar API and obtain the necessary credentials to run the script successfully.

For more information on setting up the Google Calendar API, refer to the Google Calendar API Documentation.
