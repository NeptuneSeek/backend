from httpx import AsyncClient
from typing import List, Dict
from settings import settings
import ast, asyncio

ENDPOINT = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {settings.GROQ_API_KEY}",
    "Content-Type": "application/json"
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
                "If the user does not specify a city and state, assume a reasonable or commonly associated U.S. location based on the profession.\n"
                "\n"
                "You must also:\n"
                "- Generate a short, friendly reply message for the user.\n"
                "- Determine the correct GMT offset (in whole hours, as an integer) based on the chosen city and state.\n"
                "- Identify the appropriate currency symbol for the location.\n"
                "- Estimate an average price for the requested service or profession (in the local currency, as a float only).\n"
                "\n"
                "Return your response as a single string in exactly the following format:\n"
                "profession_or_artisan<->City, State<->reply_text<->gmt_offset<->currency_symbol<->average_price\n"
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
        artisan, location, message, gmt_offset, currency_symbol, average_price = tuple(result.strip().split("<->"))
        # print(artisan.strip(), location.strip(), message.strip(), number)
        return artisan.strip(), location.strip(), message.strip(), int(gmt_offset.strip()), currency_symbol.strip(), float(average_price.strip())




    


# asyncio.run(search_classifier("Been disapointed lately with the quality of work from local plumbers in Los Angeles, CA. Can you help me find a good one?"))