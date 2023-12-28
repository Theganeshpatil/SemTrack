from fastapi import APIRouter
from ..services import auth_service
import app.schemas as schemas

router = APIRouter()
auth_service = auth_service.AuthService()

@router.get("/auth_url")
async def get_auth_url():
    return auth_service.get_auth_url()

@router.post("/exchange_code_for_tokens")
async def exchange_code_for_tokens(auth_code: schemas.AuthCode):
    return auth_service.exchange_code_for_tokens(auth_code)