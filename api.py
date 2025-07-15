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
    """
    Handles search requests by forwarding the search query to the agent module
    and returning formatted artisan data in a JSON response.
    """
    from controller.search_controller import fetch_neptune_rated_artisans
    return JSONResponse(
        content=await fetch_neptune_rated_artisans(data.search),
        status_code=status.HTTP_200_OK
    )