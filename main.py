from fastapi import FastAPI
from settings import settings
from api import api

app = FastAPI(title=settings.APP_NAME)

app.include_router(api, prefix=settings.API_PREFIX)

