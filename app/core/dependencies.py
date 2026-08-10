from bson import ObjectId
from bson.errors import InvalidId
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.config import database
from app.utils.jwt_handler import decode_access_token

bearer_scheme = HTTPBearer()


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    try:
        object_id = ObjectId(user_id)
    except (InvalidId, TypeError):
        raise credentials_exception

    user = database.users_collection.find_one({"_id": object_id})
    if user is None:
        raise credentials_exception

    user["user_id"] = str(user.pop("_id"))
    return user


def require_company(current_user: dict = Depends(get_current_user)) -> dict:
    """Use on any endpoint that operates on company/employee/attendance/payroll
    data — guarantees the logged-in user has already created their company."""
    if not current_user.get("company_id"):
        raise HTTPException(status_code=400, detail="You must create a company before accessing this resource")
    return current_user