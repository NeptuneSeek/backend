from httpx import AsyncClient
from agent import search_classifier
from settings import settings
# from dummy import generate_dummy_businesses



async def fetch_neptune_rated_artisans(query: str, retry: int = 0) -> dict:
    try:
        artisan, location, message, number,  = await search_classifier(query)
        data = fetch_neptune_artisans(artisan, location)
        return {
            "message": message,
            "results": data
        }
    except Exception as e:
        print(f"Error during search_classifier [{retry+1}]: {e}")
        if retry < settings.RETRY_ATTEMPTS:
            retry += 1
            return await fetch_neptune_rated_artisans(query, retry)
        else:
            return {
                "message": "Unable to retrieve artisan data after multiple attempts.",
                "results": []
            }
        


async def fetch_neptune_artisans(artisan: str, location: str = "", retry: int = 0) -> dict:
    from google import google_local_artisans
    try:
        artisans = await google_local_artisans(artisan, location)
        if not artisans:
            return {
                "message": f"Sorry, we don't have data for '{artisan}' in '{location}' at the moment.",
                "results": []
            }
    except Exception as e:
        print(f"Error during fetch_neptune_artisans [{retry+1}]: {e}")
        if retry < settings.RETRY_ATTEMPTS:
            retry += 1
            return await fetch_neptune_artisans(artisan, location, retry)
        else:
            return {
                "message": "Unable to retrieve artisan data after multiple attempts.",
                "results": []
            }
        

    
def format_artisan_data(artisans: list) -> list:
    formatted_data = []
    for artisan in artisans:
        formatted_data.append({
            "name": artisan.get("displayName", "Unknown"),
            "address": artisan.get("formattedAddress", "No address provided"),
            "rating": artisan.get("rating", 0.0),
            "price_level": artisan.get("priceLevel", "Not available"),
            "phone": artisan.get("nationalPhoneNumber", "No phone number"),
            "website": artisan.get("websiteUri", ""),
            "business_status": artisan.get("businessStatus", "Unknown"),
            "user_rating_count": artisan.get("userRatingCount", 0),
            "opening_hours": artisan.get("regularOpeningHours", {}).get("periods", []),
        })
    return formatted_data