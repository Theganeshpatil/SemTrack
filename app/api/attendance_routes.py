from fastapi import APIRouter, Request
from ..services import attendance_service

router = APIRouter()
attendance_service = attendance_service.AttendanceService()

@router.get("/get_attendance")
async def get_attendance(request: Request):
    auth_header = request.headers.get('Authorization')
    if auth_header:
        jwt_token = auth_header.split(" ")[1]
        return attendance_service.get_attendance(jwt_token)
    else:
        return {"error": "Authorization header not found"}