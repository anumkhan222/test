from datetime import datetime

from fastapi import HTTPException

from app.config import database
from app.models.auth_schema import UserOut
from app.utils.security import hash_password, verify_password
from app.utils.jwt_handler import create_access_token
from app.utils.otp_helper import generate_otp, get_otp_expiry
from app.utils.email_sender import send_otp_email


def _to_user_out(user: dict) -> UserOut:
    return UserOut(
        user_id=str(user["_id"]),
        full_name=user["full_name"],
        username=user["username"],
        email=user["email"],
        company_id=user.get("company_id"),
        created_at=user["created_at"],
    )


def send_registration_otp(email: str) -> None:
    if database.users_collection.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already exists")

    otp = generate_otp()
    otp_hash = hash_password(otp)
    expires_at = get_otp_expiry()

    database.registration_otp_collection.update_one(
        {"email": email},
        {"$set": {"email": email, "otp_hash": otp_hash, "expires_at": expires_at}},
        upsert=True,
    )

    send_otp_email(to_email=email, otp=otp, purpose="registration")


def register_user(full_name: str, username: str, email: str, password: str, otp: str) -> tuple[UserOut, str]:

    otp_record = database.registration_otp_collection.find_one({"email": email})
    if not otp_record:
        raise HTTPException(status_code=400, detail="No signup OTP was requested for this email. Please request one first.")

    if datetime.utcnow() > otp_record["expires_at"]:
        raise HTTPException(status_code=400, detail="OTP has expired, please request a new one")

    if not verify_password(otp, otp_record["otp_hash"]):
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if database.users_collection.find_one({"username": username}):
        raise HTTPException(status_code=400, detail="Username already exists")

    if database.users_collection.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already exists")

    now = datetime.utcnow().isoformat()
    user_doc = {
        "full_name": full_name,
        "username": username,
        "email": email,
        "password": hash_password(password),
        "company_id": None,  # set once they create their company
        "created_at": now,
    }

    result = database.users_collection.insert_one(user_doc)
    user_doc["_id"] = result.inserted_id

    database.registration_otp_collection.delete_one({"email": email})

    access_token = create_access_token(data={"sub": str(user_doc["_id"])})
    return _to_user_out(user_doc), access_token


def login_user(email: str, password: str) -> tuple[str, UserOut]:

    user = database.users_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": str(user["_id"])})
    return access_token, _to_user_out(user)


def request_password_reset(email: str) -> None:
    user = database.users_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="No account found with this email")

    otp = generate_otp()
    otp_hash = hash_password(otp)
    otp_expires_at = get_otp_expiry()

    database.users_collection.update_one(
        {"_id": user["_id"]},
        {"$set": {"otp_hash": otp_hash, "otp_expires_at": otp_expires_at}},
    )

    send_otp_email(to_email=email, otp=otp, purpose="reset")


def reset_password(email: str, otp: str, new_password: str, confirm_password: str) -> None:

    user = database.users_collection.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=404, detail="No account found with this email")

    if new_password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    otp_hash = user.get("otp_hash")
    otp_expires_at = user.get("otp_expires_at")

    if not otp_hash or not otp_expires_at:
        raise HTTPException(status_code=400, detail="No password reset was requested for this email. Please request an OTP first.")

    if datetime.utcnow() > otp_expires_at:
        raise HTTPException(status_code=400, detail="OTP has expired. Please request a new one.")

    if not verify_password(otp, otp_hash):
        raise HTTPException(status_code=400, detail="Incorrect OTP")

    database.users_collection.update_one(
        {"_id": user["_id"]},
        {
            "$set": {"password": hash_password(new_password)},
            "$unset": {"otp_hash": "", "otp_expires_at": ""},
        },
    )