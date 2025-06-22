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
                        "You are a classifier that extracts the profession, service type, or artisan from a user's query and pairs it with the corresponding location.\n"
                        "If the user does not specify a city and state, assume a reasonable or commonly associated location based on the profession or general U.S. context.\n"
                        "\n"
                        "You must also generate:\n"
                        "- A short, friendly reply message for the user.\n"
                        "- A number (an integer, either randomly between 3–10 or inferred from the prompt).\n"
                        "\n"
                        "Return your response as a **single string** in exactly the following format:\n"
                        "profession_or_artisan<->City, State<->reply_text<->number\n"
                        "\n"
                        "Do not include any extra text, line breaks, explanations, or punctuation outside this format."
                    )
                },
                {
                    "role": "user",
                    "content": f"{query}"
                }
            ],
            "temperature": 0.7
        }

        response = await client.post(ENDPOINT, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json().get("choices")[0].get("message").get("content")
        artisan, location, message, number = tuple(result.strip().split("<->"))
        number = int(number.strip())
        print(artisan.strip(), location.strip(), message.strip(), number)
        return artisan.strip(), location.strip(), message.strip(), number


async def search_and_format_artisans(query: str, retry: int = 0) -> dict:
    from dummy import generate_dummy_businesses
    try:
        async with AsyncClient() as client:
            artisan, location, message, number,  = await search_classifier(query)
            data = generate_dummy_businesses(artisan, location, number)
            return {
                "message": message,
                "data": data
            }
    except Exception as e:
        print(f"Error during search_classifier [{retry+1}]: {e}")
        if retry < 3:
            retry += 1
            return await search_and_format_artisans(query, retry)
        else:
            return {
                "message": "Unable to retrieve artisan data after multiple attempts.",
                "data": []
            }

    


# asyncio.run(search_classifier("Been disapointed lately with the quality of work from local plumbers in Los Angeles, CA. Can you help me find a good one?"))