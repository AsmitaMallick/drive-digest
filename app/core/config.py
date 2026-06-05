from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")

    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

    SECRET_KEY = os.getenv("SECRET_KEY")

    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")

settings = Settings()