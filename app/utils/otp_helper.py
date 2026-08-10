
import secrets
from datetime import datetime, timedelta

from app.configr import settings
 
OTP_EXPIRE_MINUTES = 10

def generate_otp() -> str:

    return f"{secrets.randbelow(1_000_000):06d}"


def get_otp_expiry() -> datetime:
    
    return datetime.utcnow() + timedelta(minutes=OTP_EXPIRE_MINUTES)
