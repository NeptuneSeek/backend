from httpx import AsyncClient
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
import asyncio


async def search_local_artisans(query: str, location: str, client: AsyncClient):
    url = f"https://www.merchantcircle.com/search?q={query}&qn={quote_plus(location)}"
    response = await client.get(url)
    response.raise_for_status()
    data = response.text
    soup = BeautifulSoup(response.text, 'html.parser')
    artisans = soup.find_all("div", attrs={"class": "company-item-block-content"})
    data = []
    for artisan in artisans:
        title = artisan.find("h3", attrs={"class": "company-item-title"})
        name = title.find("a").text.strip() if title else "N/A"
        url = title.find("a")["href"] if title else "N/A"
        address = artisan.find("div", attrs={"class": "company-item-address"})
        address = address.text.strip() if address else "N/A"
        phone = artisan.find("div", attrs={"class": "company-item-phone-wrap"}).find("a", {"class": "company-item-phone"})
        phone = phone.text.strip() if phone else "N/A"
        data.append({
            "name": name,
            "url": url,
            "address": address,
            "phone": phone
        })
    print(data, f"Total: {len(data)}")  # For debugging, you might want to parse this HTML instead

async def artisan_details(url: str, client: AsyncClient):
    response = await client.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    rating = soup.find("div", attrs={"class": "bi-review"}).find("div", attrs={"class": "bi-star-rating"})
    rating = rating["title"] if rating else "N/A"
    about = soup.find("p", attrs={"id": "business-description"}).text.strip()
    reviews = soup.find_all("div", attrs={"class": "listing-review"})
    reviews_data = []
    for review in reviews:
        date = review.find("span", attrs={"class": "listing-review-date"}).text.strip()
        title = review.find("h3", attrs={"class": "listing-review-title"}).text.strip()
        content = review.find("p", attrs={"itemprop": "reviewBody"}).text.strip()
        reviews_data.append({
            "date": date,
            "title": title,
            "content": content
        })



    print ({
        "rating": rating,
        "about": about,
        "reviews": reviews_data
        # Add more fields as necessary
    })


async def main():
    async with AsyncClient() as client:
        # await search_local_artisans("plumber", "Los Angeles, CA", client)
        await artisan_details("https://www.merchantcircle.com/rush-plumbing-los-angeles-ca", client)

asyncio.run(main())