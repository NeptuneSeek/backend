from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import status
from model import SearchModel


api = APIRouter()



@api.get("/health", tags=["Health Check"])
async def health_check():
    """
    Health check endpoint to verify the API is running.
    Returns a JSON response with a status message.
    """
    from datetime import datetime
    return JSONResponse(
        content={
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat() + "Z"
        },
        status_code=status.HTTP_200_OK,
        headers={
            "X-Health-Check": "OK",
            "X-Server-Time": datetime.utcnow().isoformat() + "Z"
        })


@api.post("/search", tags=["Search"])
async def search(data: SearchModel):
    from agent import search_and_format_artisans
    return JSONResponse(
        content=await search_and_format_artisans(data.search),
        status_code=status.HTTP_200_OK
    )