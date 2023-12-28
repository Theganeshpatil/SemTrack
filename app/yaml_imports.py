import yaml

with open("sem_config.yaml", "r") as f:
    sem_config = yaml.safe_load(f)
    
CAL_ID = sem_config.get("CAL_ID")
SEM_START_DATE = sem_config.get("SEM_START_DATE")
SEM_END_DATE = sem_config.get("SEM_END_DATE")
COURSE_SCHEDULE = sem_config.get("COURSE_SCHEDULE")
HOLIDAYS = sem_config.get("HOLIDAYS")
MID_SEM_DATES = sem_config.get("MID_SEM_DATES")
SCOPES = ["https://www.googleapis.com/auth/calendar"]