from fastapi import FastAPI
from settings import settings
from api import api
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=settings.APP_NAME)

app = FastAPI(
    title=settings.APP_NAME,
    # redoc_url=None,
    # docs_url=None
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

app.include_router(api, prefix=settings.API_PREFIX)

