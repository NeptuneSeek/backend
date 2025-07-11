from urllib.parse import quote_plus
from agent import search_classifier
from settings import settings
from utilities import parse_hours_summary
from typing import Tuple, Dict



async def fetch_neptune_rated_artisans(query: str, retry: int = 0) -> Dict[str, list]:
    try:
        artisan, location, message, gmt_offset = await search_classifier(query)
        data = await fetch_neptune_artisans(artisan, location, gmt_offset)
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
        


async def fetch_neptune_artisans(artisan: str, location: str, gmt_offset: int, retry: int = 0) -> Dict[str, list]:
    from service.google import google_local_artisans
    try:
        artisans = await google_local_artisans(artisan, location)
        # print(f"Found {len(artisans)} artisans for '{artisan}' in '{location}'", "\n ===> ", artisans[2])
        if not artisans:
            return {
                "message": f"Sorry, we don't have data for '{artisan}' in '{location}' at the moment.",
                "results": []
            }
        
        return format_artisan_data(artisans, gmt_offset)
    
    except Exception as e:
        print(f"Error during fetch_neptune_artisans [{retry+1}]: {e}")
        if retry < settings.RETRY_ATTEMPTS:
            retry += 1
            return await fetch_neptune_artisans(artisan, location, gmt_offset, retry)
        else:
            return {
                "message": f"Unable to retrieve artisan data for '{artisan}' in '{location}' at the moment after multiple attempts.",
                "results": []
            }
        


def format_artisan_data(artisans: list, gmt_offset: float) -> list:
    formatted_data = []
    for artisan in artisans:
        neptune_score, score_description, is_open, opening_hours_summary = neptune_scoring(artisan, gmt_offset)
        formatted_data.append({
            "name": artisan.get("name", "Unknown"),
            "address": artisan.get("address", "No address provided"),
            "review": f'{artisan.get("rating", 0.0)} ({artisan.get("rating_count", 0):,} reviews)',
            "pricing": artisan.get("price_level", "Not available"),
            "phone": artisan.get("phone", "No phone number"),
            "booking": artisan.get("website", ""),
            "business_status": artisan.get("business_status", "Unknown"),
            "map": f"https://www.google.com/maps/search/?api=1&query={quote_plus(artisan.get('address', ''))}",
            "opening_hours": opening_hours_summary,
            "is_open": is_open,
            "neptune_score": neptune_score,
            "score_description": score_description
            })
    return formatted_data

def neptune_scoring(artisan: dict, gmt_offset: int) -> Tuple[int, str, bool, str]:
    opening_hours_summary, is_open = parse_hours_summary(opening_hours=artisan.get("opening_hours", []), gmt_offset=gmt_offset)
    return int(29), "Scoring description", is_open, opening_hours_summary