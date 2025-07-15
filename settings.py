import os
from dotenv import load_dotenv


load_dotenv(override=True)


class Settings:
    APP_NAME: str = "Neptune API"
    API_PREFIX: str = "/api"
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    SERPAPI_KEY: str = os.getenv("SERPAPI_KEY", "")
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GOOGLE_PLACE_URL: str = "https://places.googleapis.com/v1"
    GOOGLE_GEOCODE_URL: str = "https://maps.googleapis.com/maps/api/geocode/json"

    RETRY_ATTEMPTS: int = 3
    AVILABILITY__MINUTES: int = 5 * 24 * 60




settings = Settings()