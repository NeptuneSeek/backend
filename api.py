from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi import status


api = APIRouter()



@api.get("/health")
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


@api.get("/search")
async def search():
    """
    Search endpoint to handle search queries.
    This is a placeholder for the actual search logic.
    Returns a JSON response with a message indicating the search was successful.
    """
    return JSONResponse(
        content={"message": "Search query received"},
        status_code=status.HTTP_200_OK
    )