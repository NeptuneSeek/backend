import os
from dotenv import load_dotenv


load_dotenv(override=True)


class Settings:
    APP_NAME: str = "Neptune API"
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")