import os
from httpx import AsyncClient
from settings import settings


BASE_URL = "https://places.googleapis.com/v1"

HEADERS = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": settings.GOOGLE_API_KEY,
    "X-Goog-FieldMask": (
        "places.displayName,"
        "places.formattedAddress,"
        "places.rating,"
        "places.priceLevel,"
        "places.nationalPhoneNumber,"
        "places.websiteUri"
    )
}

async def search_local_artisans(query: str, location: str = "", lat: float = 34.0522, lng: float = -118.2437, radius: int = 10000):
    url = f"{BASE_URL}/places:searchText"
    payload = {
        "textQuery": f"{query} in {location}",
        "locationBias": {
            "circle": {
                "center": {
                    "latitude": lat,
                    "longitude": lng
                },
                "radius": radius
            }
        },
        "maxResultCount": 10
    }

    async with AsyncClient() as client:
        response = await client.post(url, json=payload, headers=HEADERS)
        response.raise_for_status()
        data = response.json()

    results = []
    for place in data.get("places", []):
        results.append({
            "name": place.get("displayName", {}).get("text"),
            "address": place.get("formattedAddress"),
            "rating": place.get("rating"),
            "price_level": place.get("priceLevel"),
            "phone": place.get("nationalPhoneNumber"),
            "website": place.get("websiteUri"),
        })

    return results



import asyncio

if __name__ == "__main__":
    results = asyncio.run(
        search_local_artisans("plumber", "Los Angeles, CA", lat=34.0522, lng=-118.2437)
    )
    for res in results:
        print(res)
