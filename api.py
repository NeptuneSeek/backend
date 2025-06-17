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
    return JSONResponse(
        content={"status": "ok"},
        status_code=status.HTTP_200_OK
    )


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