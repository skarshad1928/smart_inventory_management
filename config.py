import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MONGODB_URI = os.getenv("MONGODB_URI")
    DATABASE_NAME = "E_commerce"
    SECRET_KEY = os.getenv("SECRET_KEY")
    DEBUG = True
