import os
from httpx import AsyncClient
from settings import settings


BASE_URL = "https://places.googleapis.com/v1"
GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

HEADERS = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": settings.GOOGLE_API_KEY,
    "X-Goog-FieldMask": (
        "places.displayName,"
        "places.formattedAddress,"
        "places.rating,"
        "places.priceLevel,"
        "places.nationalPhoneNumber,"
        "places.businessStatus,"
        "places.userRatingCount,"
        "places.regularOpeningHours,"
        "places.websiteUri"
    )
}

async def geocode_location(location: str):
    params = {"address": location, "key": settings.GOOGLE_API_KEY}
    async with AsyncClient() as client:
        response = await client.get(GEOCODE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        if data["results"]:
            loc = data["results"][0]["geometry"]["location"]
            return loc["lat"], loc["lng"]
        return None, None

async def search_local_artisans(query: str, location: str = "", radius: int = 10000):
    url = f"{BASE_URL}/places:searchText"
    lat, lng = await geocode_location(location)
    print(lat, lng)
    if lat is None or lng is None:
        raise ValueError("Could not geocode the provided location.")
    
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
        "maxResultCount": 15
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
            "business_status": place.get("businessStatus"),
            "opening_hours": place.get("regularOpeningHours", {}).get("periods", []),
            "rating_count": place.get("userRatingCount"),
            "website": place.get("websiteUri"),
        })

    return results



import asyncio

if __name__ == "__main__":
    results = asyncio.run(
        search_local_artisans("locksmith", "Los Angeles, CA")
    )
    for res in results:
        print(res)
