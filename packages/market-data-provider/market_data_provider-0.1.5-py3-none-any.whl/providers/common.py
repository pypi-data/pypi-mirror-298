from datetime import timedelta, datetime
from typing import List


def generate_date_range(day_from: datetime, day_to: datetime) -> List[datetime]:
    return [day_from + timedelta(days=i) for i in range((day_to - day_from).days + 1)]