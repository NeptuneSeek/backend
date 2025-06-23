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
    description = f"We are a {random.choice(['locally owned', 'family-run', 'certified', 'highly rated'])} {profession} business serving the {location.split(',')[0]} area with excellence and professionalism."
    map_url = f"https://www.google.com/maps/search/?api=1&query={quote_plus(address)}"
    neptune_score = round((rating * 20) - (random.randint(50, 200) / 10), 0)

    return {
        "name": business_name,
        "description": description,
        "address": address,
        "phone": phone,
        "review": f"{rating} ({reviews} reviews)",
        "map": map_url,
        "neptune_score": neptune_score
    }

def generate_dummy_businesses(profession: str, location: str, count: int = 10):
    return sorted([generate_dummy_business(profession, location) for _ in range(count+1)], key=lambda x: x.get("neptune_score", None), reverse=True)

# Example usage
# dummy = generate_dummy_businesses('plumber', 'Los Angeles, CA', 10)
# print(dummy)
