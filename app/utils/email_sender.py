
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.configr import settings


def _get_mail_client() -> FastMail:
    connection_config = ConnectionConfig(
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_FROM=settings.MAIL_FROM,
        MAIL_PORT=settings.MAIL_PORT,
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_STARTTLS=True,
        MAIL_SSL_TLS=False,
        USE_CREDENTIALS=True,
        VALIDATE_CERTS=True,
    )
    return FastMail(connection_config)


import asyncio

def send_otp_email(to_email: str, otp: str, purpose: str = "verification") -> None:
    if purpose == "registration":
        subject = "Signup Verification Code"
        intro = "Your signup verification code is"
    else:
        subject = "Your Password Reset Code"
        intro = "Your password reset code is"

    body = (
        f"{intro}: {otp}\n\n"
        f"This code expires in {settings.OTP_EXPIRE_MINUTES} minutes.\n"
        f"If you didn't request this, you can safely ignore this email."
    )

    if not settings.MAIL_SERVER or not settings.MAIL_USERNAME:
        print(f"[DEV MODE - no SMTP configured] OTP for {to_email}: {otp}")
        return

    message = MessageSchema(
        subject=subject,
        recipients=[to_email],
        body=body,
        subtype=MessageType.plain,
    )

    fast_mail = _get_mail_client()

    asyncio.run(fast_mail.send_message(message))