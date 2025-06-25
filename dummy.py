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
    booking_method = random.choice(['online with Apple Pay', 'online via web form', 'by phone only', 'via text or email'])
    
    # Core components
    review_score = round(rating * 15)
    review_volume_score = round(min(reviews, 100) * 0.35)
    booking_score = random.choice([30, 25, 15])  # Example values

    # Final Neptune score
    neptune_score = min(100, review_score + review_volume_score)

    # Adjust for booking method
    final_score = min(100, neptune_score + booking_score - 15)  # normalize around 100 max

    # Description logic
    score_description = (
        f"This provider gets a Neptune score of {final_score}, awarded as follows: "
        f"{review_score} points for having a {rating} star rating on major platforms, "
        f"{review_volume_score} points based on {reviews} customer reviews, and "
        f"{booking_score} points for offering {booking_method} booking. "
        f"This makes them one of the top-rated providers in the {location.split(',')[0]} area."
    )

    return {
        "name": business_name,
        "description": f"We are a {random.choice(['locally owned', 'family-run', 'certified', 'highly rated'])} {profession} business serving the {location.split(',')[0]} area with excellence and professionalism.",
        "address": address,
        "phone": phone,
        "review": f"{rating} ({reviews} reviews)",
        "map": f"https://www.google.com/maps/search/?api=1&query={quote_plus(address)}",
        "neptune_score": final_score,
        "score_description": score_description
    }

def generate_dummy_businesses(profession: str, location: str, count: int = 10):
    return sorted([generate_dummy_business(profession, location) for _ in range(count+1)], key=lambda x: x.get("neptune_score", None), reverse=True)

# Example usage
dummy = generate_dummy_businesses('plumber', 'Los Angeles, CA', 1)
print(dummy)
