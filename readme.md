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

After running the script, you will be presented with a menu containing various options to manage your Google Calendar. Choose the desired option by entering the corresponding number.

Option 1: Create Course Events
Option 2: Delete All Events
Option 3: Get Events
Option 4: Get Attendance
Option 5: Get Maximum Possible Attendance
Option 6: Delete Events on Date
Option 7: Mark Absent for Events on Date
Option 0: Exit
Follow the on-screen instructions for each option to perform the desired action.

# Google Calendar API

This project utilizes the Google Calendar API to interact with your Google Calendar. The API allows the script to read, create, update, and delete events on your calendar. You will need to set up the Google Calendar API and obtain the necessary credentials to run the script successfully.

For more information on setting up the Google Calendar API, refer to the Google Calendar API Documentation.

# Contributing

If you find any issues or have suggestions for improvement, please feel free to open an issue or submit a pull request. Contributions are always welcome!
