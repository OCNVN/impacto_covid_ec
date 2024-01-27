import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env file.

def create_connection():
    try:
        engine = create_engine(f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASS")}@{os.getenv("DB_HOST", "127.0.0.1")}:{os.getenv("DB_PORT", "5432")}/{os.getenv("DB_NAME")}')
        return engine
    except Exception as error:
        print ("Error while connecting to PostgreSQL", error)