from ..repositories import attendance 
from ..google_imports import *
from ..yaml_imports import *
from .auth_service import AuthService
auth_service = AuthService()
class AttendanceService:
    def get_attendance(self, jwt_token):
        service = build("calendar", "v3", credentials=auth_service.create_credentials_from_jwt(jwt_token))
        res = attendance.get_attendance(service, semester_class_start_date = SEM_START_DATE, semester_class_end_date=SEM_END_DATE,cal_id=CAL_ID)
        return {"attendance": res}