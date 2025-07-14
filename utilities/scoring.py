
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

    # Cap at 10080 minutes (7*24*60)
    total_minutes = min(total_minutes, settings.AVILABILITY__MINUTES)
    # print(f"Total open minutes in a week: {total_minutes:,} of 10,080")
    open_hours_score = round((total_minutes / settings.AVILABILITY__MINUTES) * 30)
    return score + open_hours_score


# def pricing
    