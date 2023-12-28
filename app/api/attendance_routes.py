from fastapi import APIRouter
from ..services import attendance_service

router = APIRouter()
attendance_service = attendance_service.AttendanceService()

@router.get("/get_attendance")
def get_attendance(jwt_token: str):
    return attendance_service.get_attendance(jwt_token)