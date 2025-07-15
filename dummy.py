import random
from urllib.parse import quote_plus

def generate_dummy_business(profession: str, location: str):
    adjectives = ['Affordable', 'Reliable', 'Trusted', 'Expert', 'Quality']
    suffixes = ['Services', 'Solutions', 'Experts', 'Pros', 'Team']
    streets = ['Main St', 'Broadway', 'Elm St', 'Maple Ave', 'Sunset Blvd']

    business_name = f"{random.choice(adjectives)} {profession.title()} {random.choice(suffixes)}"
    street_address = f"{random.randint(100, 9999)} {random.choice(streets)}"
    address = f"{street_address}, {location}"
    phone = f"({random.randint(200, 999)}) {random.randint(100,999)}-{random.randint(1000,9999)}"
    rating = round(random.uniform(3.5, 5.0), 1)
    reviews = random.randint(10, 500)

    # Simulate pricing
    low_price = random.randint(50, 500)
    high_price = random.randint(500, 1500)
    if low_price > high_price:
        low_price, high_price = high_price, low_price
    price_range = f"${low_price} - ${high_price}"
    avg_price = (low_price + high_price) / 2

    # Booking proximity
    availability_options = {
        "Same-day availability": 40,
        "Next-day available": 30,
        "Within 3 days": 20,
        "Next week availability": 10
    }
    availability_desc, calendar_score = random.choice(list(availability_options.items()))

    # Scoring logic
    review_score = round((rating / 5.0) * 30)                          # Out of 30
    value_score = round((1 - min(avg_price, 1500) / 1500) * 30)       # Lower avg = higher score, max 30
    calendar_score = calendar_score                                   # Max 40

    final_score = review_score + value_score + calendar_score         # Max 100

    # Description
    score_description = (
        f"This provider earns a Neptune score of {final_score}, composed of: "
        f"{review_score} points from a {rating}-star rating, "
        f"{value_score} points for offering competitive pricing (average cost ${int(avg_price)}), and "
        f"{calendar_score} points for {availability_desc.lower()}."
    )

    return {
        "name": business_name,
        "description": f"We are a {random.choice(['locally owned', 'family-run', 'certified', 'highly rated'])} {profession} business serving the {location.split(',')[0]} area with excellence and professionalism.",
        "address": address,
        "phone": phone,
        "pricing": price_range,
        "availability": availability_desc,
        "review": f"{rating} ({reviews} reviews)",
        "map": f"https://www.google.com/maps/search/?api=1&query={quote_plus(address)}",
        "neptune_score": final_score,
        "score_description": score_description
    }


def generate_dummy_businesses(profession: str, location: str, count: int = 10):
    return sorted([generate_dummy_business(profession, location) for _ in range(count+1)], key=lambda x: x.get("neptune_score", None), reverse=True)

# Example usage
# dummy = generate_dummy_businesses('plumber', 'Los Angeles, CA', 1)
# print(dummy)
