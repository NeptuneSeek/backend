from httpx import AsyncClient
from settings import settings
import asyncio

headers = {
  'X-API-KEY': settings.SERPAPI_KEY,
  'Content-Type': 'application/json'
}


async def search_local_artisans(query: str, num: int = 20):
    url = "https://google.serper.dev/search"
    payload = {
        "q": query,
        "num": num
    }

    async with AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

    print(data)
    results = []
    for result in data.get("local", []):
        results.append({
            "name": result.get("title"),
            "address": result.get("address"),
            "rating": result.get("rating"),
            "reviews": result.get("reviews"),
            "phone": result.get("phone"),
            "website": result.get("website"),
        })

    return results

res = asyncio.run(search_local_artisans("plumber in LA"))
print(res)
