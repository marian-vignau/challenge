"""
Reads the config file.
"""
import configparser
from collections import defaultdict
from decimal import Decimal

from src.employee import Employee
from src.utils import read_hour, diff_minutes


class Rates:
    def __init__(self, filename="data/rates.ini"):
        """Reads the configuration file that include all the prices."""
        parser = configparser.ConfigParser()
        parser.read(filename)
        self._rates = defaultdict(list)

        for rate_segment in parser.sections():
            hour_rate = dict(parser[rate_segment].items())

            hour_rate["cost"] = Decimal(hour_rate["cost"])
            hour_rate["start"] = read_hour(hour_rate["start"])
            hour_rate["end"] = read_hour(hour_rate["end"], end_of_minute=True)
            week_days = hour_rate.pop("days")
            for week_day in week_days.split(","):
                self._rates[week_day.strip()].append(hour_rate)

    def apply_rates(self, employee: Employee):
        """Calculate how many minutes worked on each rate and correspondig payment."""
        employee.subtotals = []
        for period in employee.periods:
            day_rates = self._rates[period["week_day"]]
            for hour_rate in day_rates:
                if period["end"] < hour_rate["start"]:
                    continue  # no overlap
                if period["start"] > hour_rate["end"]:
                    continue  # no overlap

                subtotal = dict(
                    start=max(period["start"], hour_rate["start"]),
                    end=min(period["end"], hour_rate["end"]),
                    cost=hour_rate["cost"],
                )

                subtotal["minutes"] = diff_minutes(subtotal)
                subtotal["subtotal"] = subtotal["minutes"] * (hour_rate["cost"] / 60)
                employee.subtotals.append(subtotal)
        return employee.subtotals


# rates = read_rates()
