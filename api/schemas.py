# library imports
import motor.motor_asyncio
from pydantic import BaseModel, Field, EmailStr
from pydantic import BaseModel
from bson import ObjectId
from typing import Optional
import os
from dotenv import load_dotenv

# do not specify the '.env'
load_dotenv()

# pip install pydantic[email]
# python -m pip install motor
# python3 -m pip install "pymongo[srv]"

# connect to mongodb
client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv('MONGODB_URL'))

# create the news_summary_users database
db = client.news_summary_users


# BSON and JSON compatibility addressed here
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "jdoe@example.com",
                "password": "secret_code"
            }
        }


class UserResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "jdoe@example.com"
            }
        }


class BlogContent(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(...)
    body: str = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "blog title",
                "body": "blog content"
            }
        }


class BlogContentResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(...)
    body: str = Field(...)
    auther_name: str = Field(...)
    auther_id: str = Field(...)
    created_at: str = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "title": "blog title",
                "body": "blog content",
                "auther_name": "name of the auther",
                "auther_id": "ID of the auther",
                "created_at": "Date of blog creation"
            }
        }


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class PasswordResetRequest(BaseModel):
    email: EmailStr = Field(...)


class PasswordReset(BaseModel):
    password: str = Field(...)
