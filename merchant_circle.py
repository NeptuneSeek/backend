from httpx import AsyncClient
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import asyncio


async def search_local_artisans(query: str, location: str, client: AsyncClient):
    url = f"https://www.merchantcircle.com/search?q={query}&qn={quote_plus(location)}"
    # print(url)
    response = await client.get(url)
    response.raise_for_status()
    data = response.text
    soup = BeautifulSoup(response.text, 'html.parser')
    comp = soup.find_all("div", attrs={"class": "company-item"})
    print(comp)  # For debugging, you might want to parse this HTML instead



async def main():
    async with AsyncClient() as client:
        await search_local_artisans("plumber", "Los Angeles, CA", client)

asyncio.run(main())