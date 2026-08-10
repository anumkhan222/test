from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_current_user
from app.controllers import auth_controller
from app.models.auth_schema import (
    SendRegistrationOtpRequest,
    RegisterRequest,
    RegisterResponse,
    LoginRequest,
    LoginResponse,
    MessageResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest,
)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])


@router.post("/send-registration-otp", response_model=MessageResponse)
def send_registration_otp(payload: SendRegistrationOtpRequest):
    auth_controller.send_registration_otp(email=payload.email)
    return MessageResponse(message="An OTP has been sent to your email")


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest):
    user, access_token = auth_controller.register_user(
        full_name=payload.full_name,
        username=payload.username,
        email=payload.email,
        password=payload.password,
        otp=payload.otp,
    )
    return RegisterResponse(message="User registered successfully", access_token=access_token, user=user)


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    access_token, user = auth_controller.login_user(email=payload.email, password=payload.password)
    return LoginResponse(message="Login successful", access_token=access_token, user=user)


@router.post("/logout", response_model=MessageResponse)
def logout(current_user: dict = Depends(get_current_user)):
    return MessageResponse(message="Logged out successfully")


@router.post("/forgot-password", response_model=MessageResponse)
def forgot_password(payload: ForgotPasswordRequest):
    auth_controller.request_password_reset(email=payload.email)
    return MessageResponse(message="An OTP has been sent to your email")


@router.post("/reset-password", response_model=MessageResponse)
def reset_password(payload: ResetPasswordRequest):
    auth_controller.reset_password(
        email=payload.email,
        otp=payload.otp,
        new_password=payload.new_password,
        confirm_password=payload.confirm_password,
    )
    return MessageResponse(message="Password reset successfully")