from pydantic import BaseModel


class AuthCode(BaseModel):
    auth_code: str
