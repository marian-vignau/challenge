"""
Reads the config file.
"""
import configparser
from collections import defaultdict
from decimal import Decimal

from src.utils import read_hour

def read_rates(filename="data/rates.ini"):
    """Reads the configuration file that include all the prices."""
    parser = configparser.ConfigParser()
    parser.read(filename)
    rates = defaultdict(list)

    for rate_segment in parser.sections():
        hour_rate = dict(parser[rate_segment].items())

        hour_rate["cost"] = Decimal(hour_rate["cost"])
        hour_rate["start"] = read_hour(hour_rate["start"])
        hour_rate["end"] = read_hour(hour_rate["end"], end_of_minute=True)
        week_days = hour_rate.pop("days")
        for week_day in week_days.split(","):
            rates[week_day.strip()].append(hour_rate)
    return rates


rates = read_rates()

