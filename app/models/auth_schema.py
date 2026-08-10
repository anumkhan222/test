from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator

from app.utils.password_validator import assert_no_edge_spaces


class SendRegistrationOtpRequest(BaseModel):
    email: EmailStr


class RegisterRequest(BaseModel):
    full_name: str = Field(..., min_length=1)
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=8)
    otp: str = Field(..., min_length=6, max_length=6)

    @field_validator("password")
    @classmethod
    def _no_edge_spaces(cls, v):
        assert_no_edge_spaces(v)
        return v


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def _no_edge_spaces(cls, v):
        assert_no_edge_spaces(v)
        return v


class UserOut(BaseModel):
    user_id: str
    full_name: str
    username: str
    email: EmailStr
    company_id: Optional[str] = None
    created_at: str


class RegisterResponse(BaseModel):
    message: str
    access_token: str
    user: UserOut


class LoginResponse(BaseModel):
    message: str
    access_token: str
    user: UserOut


class MessageResponse(BaseModel):
    message: str


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str = Field(..., min_length=6, max_length=6)
    new_password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)

    @field_validator("new_password", "confirm_password")
    @classmethod
    def _no_edge_spaces(cls, v):
        assert_no_edge_spaces(v)
        return v