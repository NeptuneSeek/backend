from urllib.parse import quote_plus
from agent import search_classifier
from settings import settings
from utilities.utils import parse_hours_summary
from utilities.scoring import price_range_from_price_level, pricing_scoring, ratings_reviews_scoring, availability_scoring
from typing import Tuple, Dict



async def fetch_neptune_rated_artisans(query: str, retry: int = 0) -> Dict[str, list]:
    try:
        artisan, location, message, gmt_offset, currency_symbol, average_price = await search_classifier(query)
        data = await fetch_neptune_artisans(artisan, location, gmt_offset, currency_symbol, average_price)
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
        


async def fetch_neptune_artisans(artisan: str, location: str, gmt_offset: int, currency_symbol: str, average_price: float, retry: int = 0) -> Dict[str, list]:
    from service.google import google_local_artisans
    try:
        artisans = await google_local_artisans(artisan, location)
        # print(f"Found {len(artisans)} artisans for '{artisan}' in '{location}'", "\n ===> ", artisans[2])
        if not artisans:
            return {
                "message": f"Sorry, we don't have data for '{artisan}' in '{location}' at the moment.",
                "results": []
            }
        
        return format_artisan_data(artisans, gmt_offset, currency_symbol, average_price)
    
    except Exception as e:
        print(f"Error during fetch_neptune_artisans [{retry+1}]: {e}")
        if retry < settings.RETRY_ATTEMPTS:
            retry += 1
            return await fetch_neptune_artisans(artisan, location, gmt_offset, currency_symbol, average_price, retry)
        else:
            return {
                "message": f"Unable to retrieve artisan data for '{artisan}' in '{location}' at the moment after multiple attempts.",
                "results": []
            }
        


def format_artisan_data(artisans: list, gmt_offset: float, currency_symbol: str, average_price: float) -> list:
    formatted_data = []
    for artisan in artisans:
        try:
            neptune_score, score_description, is_open, opening_hours_summary = neptune_scoring(artisan, gmt_offset, average_price)
            # print(neptune_score, score_description, is_open, opening_hours_summary)
            business_status = artisan.get("business_status", "N/A")
            if business_status != "OPERATIONAL":
                continue

            formatted_data.append({
                "name": artisan.get("name", "N/A"),
                "address": artisan.get("address", "N/A"),
                "review": f'{float(artisan.get("rating", 0.0))} ({artisan.get("rating_count", 0):,} reviews)',
                "pricing": price_range_from_price_level(artisan.get("price_level", 1), currency_symbol, average_price),
                "phone": artisan.get("phone", "N/A"),
                "booking": artisan.get("website", "N/A"),
                "map": f"https://www.google.com/maps/search/?api=1&query={quote_plus(artisan.get('address', ''))}",
                "opening_hours": opening_hours_summary,
                "is_open": is_open,
                "neptune_score": neptune_score,
                "score_description": score_description
                })
        except Exception as e:
            print(f"Error formatting artisan data: {e}")
    return formatted_data



def neptune_scoring(artisan: dict, gmt_offset: int, average_price: float) -> Tuple[int, str, bool, str]:
    opening_hours = artisan.get("opening_hours", [])
    ratings = float(artisan.get("rating", 0.0))
    reviews = int(artisan.get("rating_count", 0))
    price_level = artisan.get("price_level")

    opening_hours_summary, is_open = parse_hours_summary(opening_hours=opening_hours, gmt_offset=gmt_offset)
    ratings_reviews_score = ratings_reviews_scoring(ratings, reviews)
    availability_score = availability_scoring(opening_hours, is_open)
    pricing_score = pricing_scoring(price_level, average_price)
    score_description = (
        f"This provider earns a Neptune score of {ratings_reviews_score + availability_score}, "
        f"composed of: {ratings_reviews_score} points from a {ratings}-star rating {reviews:,} reviews, "
        f"and {availability_score} points for availability."
    )

    # print(f"Avg Price ${average_price:,}| RR_Score: {ratings_reviews_score}, Availability Score: {availability_score}, Pricing Score: {pricing_score}")

    neptune_score = ratings_reviews_score + availability_score + pricing_score
    return neptune_score, score_description, is_open, opening_hours_summary