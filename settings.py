import os
from dotenv import load_dotenv


load_dotenv(override=True)


class Settings:
    APP_NAME: str = "Neptune API"
    API_PREFIX: str = "/api"
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    SERPAPI_KEY: str = os.getenv("SERPAPI_KEY", "")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")



settings = Settings()