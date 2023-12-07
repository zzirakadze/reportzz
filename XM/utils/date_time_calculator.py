import datetime
from typing import Tuple


def _format_date(date: datetime.date) -> str:
    return date.strftime("%a %b %d %Y")


class DateGenerator:
    def __init__(self):
        self.today = datetime.datetime.now().date()

    def get_today(self) -> str:
        """
        :return:
        """
        return _format_date(self.today)

    def get_tomorrow(self) -> str:
        tomorrow = self.today + datetime.timedelta(days=1)
        return _format_date(tomorrow)

    def get_next_week(self) -> Tuple[str, str]:
        try:
            first_day_of_next_week = self.today + datetime.timedelta(
                days=(7 - self.today.weekday())
            )
            last_day_of_next_week = first_day_of_next_week + datetime.timedelta(days=6)

            return _format_date(first_day_of_next_week), _format_date(
                last_day_of_next_week
            )
        except Exception as e:
            raise Exception(f"Error calculating next week's dates: {e}")

    def get_next_month(self) -> Tuple[str, str]:
        try:
            next_month = self.today.replace(day=1)
            if next_month.month == 12:
                next_month = next_month.replace(year=next_month.year + 1, month=1)
            else:
                next_month = next_month.replace(month=next_month.month + 1)

            last_day_of_next_month = next_month.replace(day=28) + datetime.timedelta(
                days=4
            )
            last_day_of_next_month -= datetime.timedelta(
                days=last_day_of_next_month.day
            )

            return _format_date(next_month), _format_date(last_day_of_next_month)
        except Exception as e:
            raise Exception(f"Error calculating next month's dates: {e}")
