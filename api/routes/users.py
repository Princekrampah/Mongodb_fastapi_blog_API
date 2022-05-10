# library imports
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

# module imports
from api import oauth2
from ..schemas import User, UserResponse, db
from ..utils import get_password_hash
from ..send_email import send_registration_mail
import secrets


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/registration", response_description="Register New User", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def registration(user_info: User):
    user_info = jsonable_encoder(user_info)

    # check for duplications
    username_found = await db["users"].find_one({"name": user_info["name"]})
    email_found = await db["users"].find_one({"email": user_info["email"]})

    if username_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="There already is a user by that name")

    if email_found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="There already is a user by that email")

    # hash the user password
    user_info["password"] = get_password_hash(user_info["password"])
    # generate apiKey
    user_info["apiKey"] = secrets.token_hex(20)
    new_user = await db["users"].insert_one(user_info)
    created_user = await db["users"].find_one({"_id": new_user.inserted_id})

    # send email
    await send_registration_mail("Registration successful", user_info["email"],
        {
            "title": "Registration successful",
            "name": user_info["name"]
        }
    )

    return created_user


@router.post("/details", response_description="Get user details", response_model=UserResponse)
async def details(current_user=Depends(oauth2.get_current_user)):
    user = await db["users"].find_one({"_id": current_user["_id"]})
    return user
