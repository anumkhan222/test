import os
from pymongo import MongoClient


MONGO_URI: str = "mongodb+srv://anumkh256_db_user:sc07TzF0ueLiLqr8@cluster0.whlcuvr.mongodb.net/"
DB_NAME: str = "employeesystem"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]


companies_collection = db["companies"]
company_settings_collection = db["company_settings"]
employees_collection = db["employees"]
payrolls_collection = db["payrolls"]
