from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
    LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN")
    GOOGLE_CALENDAR_CREDENTIALS = os.getenv("GOOGLE_CALENDAR_CREDENTIALS")