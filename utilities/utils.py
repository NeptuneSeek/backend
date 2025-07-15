from datetime import datetime, time, timedelta, timezone
from typing import List, Dict, Tuple

DAY_NAMES = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

def parse_hours_summary(opening_hours: List[Dict], gmt_offset: float) -> Tuple[str, bool]:
    # print(opening_hours, gmt_offset)
    weekly_schedule = {i: [] for i in range(7)}
    for period in opening_hours:
        if 'open' not in period or 'close' not in period:
            continue
        open_day = period['open']['day']
        open_time = time(hour=period['open']['hour'], minute=period['open']['minute'])
        close_day = period['close']['day']
        close_time = time(hour=period['close']['hour'], minute=period['close']['minute'])

        if open_day == close_day:
            weekly_schedule[open_day].append((open_time, close_time))
        else:
            weekly_schedule[open_day].append((open_time, time(23, 59)))
            weekly_schedule[close_day].append((time(0, 0), close_time))

    # Current time
    offset = timezone(timedelta(hours=gmt_offset))
    now = datetime.now(offset)
    current_day = now.weekday()
    current_time = now.time()
    is_open = any(start <= current_time <= end for start, end in weekly_schedule[current_day])

    # Normalize times to string
    def format_time(t: time) -> str:
        return t.strftime('%I:%M %p').lstrip('0').replace(':00', '')  # 8 AM instead of 08:00 AM

    # Create a map: (open_time_str, close_time_str) -> [days]
    grouped = {}
    for day, times in weekly_schedule.items():
        for start, end in times:
            key = (format_time(start), format_time(end))
            grouped.setdefault(key, []).append(day)

    # Build sentence parts
    parts = []
    for (start_str, end_str), days in grouped.items():
        days.sort()
        ranges = []
        i = 0
        while i < len(days):
            j = i
            while j + 1 < len(days) and days[j + 1] == days[j] + 1:
                j += 1
            if i == j:
                ranges.append(DAY_NAMES[days[i]])
            else:
                ranges.append(f"{DAY_NAMES[days[i]]}–{DAY_NAMES[days[j]]}")
            i = j + 1
        days_str = ', '.join(ranges)
        parts.append(f"{days_str}: {start_str} – {end_str}")

    summary = "Open " + "; ".join(parts) if parts else "N/A"
    return summary, is_open




# opening_hours = [{'open': {'day': 1, 'hour': 7, 'minute': 0}, 'close': {'day': 1, 'hour': 21, 'minute': 0}}, {'open': {'day': 2, 'hour': 7, 'minute': 0}, 'close': {'day': 2, 'hour': 21, 'minute': 0}}, {'open': {'day': 3, 'hour': 7, 'minute': 0}, 'close': {'day': 3, 'hour': 21, 'minute': 0}}, {'open': {'day': 4, 'hour': 7, 'minute': 0}, 'close': {'day': 4, 'hour': 21, 'minute': 0}}, {'open': {'day': 5, 'hour': 7, 'minute': 0}, 'close': {'day': 5, 'hour': 21, 'minute': 0}}, {'open': {'day': 6, 'hour': 10, 'minute': 0}, 'close': {'day': 6, 'hour': 14, 'minute': 0}}]
# print(parse_hours_summary(opening_hours, -8))