from httpx import AsyncClient
from typing import List, Dict
from settings import settings
import ast, asyncio

ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {settings.GROQ_API_KEY}",
    "Content-Type": "application/json"
}



def build_parse_results_payload(query: str, scraped_data: list[Dict[str, str]]) -> Dict:
    return {
        "model": "llama3-70b-8192",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a JSON-only formatter that transforms structured artisan listings into valid JSON.\n\n"
                    "Output format:\n"
                    "{\n"
                    "  'message': 'Summary or notes about the results',\n"
                    "  'data': [\n"
                    "    {\n"
                    "      'name': string,\n"
                    "      'rating': float (0.0–5.0),\n"
                    "      'price': string from input field 'price_range',\n"
                    "      'address': string (from 'location'),\n"
                    "      'booking': string (booking_url) or null,\n"
                    "      'neptune_score': integer, calculated as:\n"
                    "          (rating × 20) - (average price ÷ 10),\n"
                    "      'source': 'Yelp' | 'Porch' | 'HomeAdvisor' | 'Angi' | 'Other'\n"
                    "    },\n"
                    "    ... (at least 10 entries)\n"
                    "  ]\n"
                    "}\n\n"
                    "Neptune Score rules:\n"
                    "- Estimate midpoint of price_range (e.g. '$90 - $160' → 125).\n"
                    "- If no price_range is available, assume $100.\n"
                    "- Formula: (rating × 20) - (avg_price ÷ 10), rounded and capped to 0–100.\n\n"
                    "Constraints:\n"
                    "- Output only valid JSON.\n"
                    "- No content outside JSON.\n"
                    "- All extra explanation or fallback messages must go inside the 'message' key.\n"
                )
            },
            {
                "role": "user",
                "content": (
                    f"User query: {query}\n\n"
                    f"Scraped artisan data:\n{scraped_data}"
                )
            }
        ],
        "temperature": 0.7,
        "max_tokens": 1600
    }

async def search_classifier(query: str) -> tuple:
    async with AsyncClient() as client:
        payload = {
        "model": "llama3-70b-8192",
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a classifier that extracts the profession or service type and the location "
                    "from a user's query. Your response should be a string in the format"
                    "profession_or_artisan<->location. Do not include any extra text, just the string."
                )
            },
            {
                "role": "user",
                "content": f"{query}"
            }
        ]}
        response = await client.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json().get("choices")[0].get("message").get("content")
        result = tuple(result.strip().split("<->"))
        print(result)
        return result

async def search_and_format_artisans(query: str) -> List[Dict]:
    async with AsyncClient() as client:
        response = await client.post(ENDPOINT, headers=headers, json=build_parse_results_payload(query))
        result = response.json().get("choices")[0].get("message").get("content")
        return ast.literal_eval(result)
    


asyncio.run(search_classifier("plumber in Los Angeles"))