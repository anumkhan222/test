from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    MONGO_URI: str = "mongodb+srv://anumkh256_db_user:sc07TzF0ueLiLqr8@cluster0.whlcuvr.mongodb.net/"
    DATABASE_NAME: str = "employeesystem"
    SECRET_KEY: str = "7d3f9c2b8e5a4f1d9a6c3b7e8f2a1d4c5b9e7a3f6d8c2b1a4e9f5c7d3b8a6e1"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    OTP_EXPIRE_MINUTES: int = 10
    MAIL_USERNAME: str = "anumkh256@gmail.com"
    MAIL_PASSWORD: str = "mjwylizireqhzhmh"
    MAIL_FROM: str = "anumkh256@gmail.com"
    MAIL_SERVER: str = "smtp.gmail.com"
    MAIL_PORT: int = 587



    class Config:
        env_file = ".env"

settings = Settings()
