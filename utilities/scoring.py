
def ratings_reviews_scoring(rating: float, reviews: int) -> int:
    """
    Calculate the review score based on rating and number of reviews.
    The score is out of 30 points.
    """
    if rating < 0 or rating > 5:
        raise ValueError("Rating must be between 0 and 5.")
    if reviews < 0:
        raise ValueError("Number of reviews cannot be negative.")
    
    # 15 points for rating, 15 points for reviews (total 30)
    rating_score = round((rating / 5.0) * 15)
    reviews_score = min(reviews // 10, 15)
    return rating_score + reviews_score


def availability_scoring(open_hours: list, is_open: bool) -> int:
    from settings import settings
    """
    Assign a score based on the availability description.
    10 points if currently open, up to 20 points for open hours coverage (24/7 gets full 20).
    open_hours: list of dicts with 'open' and 'close' keys, each containing 'day', 'hour', 'minute'.
    Example:
    [
        {'open': {'day': 1, 'hour': 7, 'minute': 0}, 'close': {'day': 1, 'hour': 21, 'minute': 0}},
        ...
    ]
    """
    score = 10 if is_open else 0

    # Calculate total open minutes in a week
    total_minutes = 0
    for period in open_hours:
        open_time = period.get('open')
        close_time = period.get('close')
        if not open_time or not close_time:
            continue
        # Convert to minutes since week start (Monday 0:00)
        open_min = ((open_time['day'] - 1) * 24 * 60) + (open_time['hour'] * 60) + open_time['minute']
        close_min = ((close_time['day'] - 1) * 24 * 60) + (close_time['hour'] * 60) + close_time['minute']
        if close_min >= open_min:
            total_minutes += close_min - open_min
        else:
            # Wraps to next week
            total_minutes += (settings.AVILABILITY__MINUTES - open_min) + close_min

    total_minutes = min(total_minutes, settings.AVILABILITY__MINUTES)
    open_hours_score = round((total_minutes / settings.AVILABILITY__MINUTES) * 30)
    return score + open_hours_score



def pricing_scoring(price_level: int, average_price: float) -> int:
    """
    Calculate the pricing score based on price level and average price.
    The score is out of 30 points.
    """
    if price_level < 0 or price_level > 4:
        raise ValueError(f"[{price_level}] -> Price level must be between 0 and 4.")
    if average_price < 0:
        raise ValueError(f"[{average_price}] -> Average price cannot be negative.")

    # 15 points for price level, 15 points for proximity to average price (within 20%)
    # Cheaper price_level should get higher score (0 = cheapest, 4 = most expensive) + 1
    price_level_score = round(((5 - price_level) / 4.0) * 15)
    price_proximity_score = min(max(0, (average_price - 100) // 10), 15)
    return price_level_score + price_proximity_score


def price_range_from_price_level(price_level: int, currency_symbol: str, average_price: float) -> str:
    """
    Convert Google price level (1-4) to a price range string, dynamically using average_price.
    """
    if price_level < 0 or price_level > 4:
        raise ValueError(f"[{price_level}] -> Price level must be between 0 and 4.")

    # Define multipliers for each price level
    multipliers = {
        0: (0.22, 0.45),   # 22% - 45% of avg price
        1: (0.5, 0.99),   # 50% - 99% of avg price
        2: (1.0, 1.49),   # 100% - 149%
        3: (1.5, 1.99),   # 150% - 199%
        4: (2.0, None),   # 200% and above
    }

    low, high = multipliers[price_level]
    if high is not None:
        min_price = round(average_price * low)
        max_price = round(average_price * high)
        return f"{currency_symbol}{min_price:,} - {currency_symbol}{max_price:,}"
    else:
        min_price = round(average_price * low)
        return f"{currency_symbol}{min_price}+"
    