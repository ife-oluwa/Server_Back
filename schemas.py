from pydantic import BaseModel
from typing import Optional
from dotenv import dotenv_values
import datetime

class SignUpModel(BaseModel):
    id: Optional[int]
    username: str
    email: str
    password: str
    is_admin: Optional[bool]
    
    class Config:
        orm_mode=True
        schema_extra={
            'example': {
            "username": "JohnDoe",
            "email": "john@example.com",
            "password": "password",
            'is_admin': False,
            }
        }

class Settings(BaseModel):
    authjwt_secret_key: str= dotenv_values('.env')["AUTH_JWT_SECRET"]

class LoginModel(BaseModel):
    username: str
    password: str

class PredictionModel(BaseModel):
    id: Optional[int]
    date_created: Optional[datetime.datetime]
    predictions: int
    user_id: Optional[int]

    class Config:
        orm_mode=True
        schema_extra = {
            "example": {
                "predictions": 100
            }
        }