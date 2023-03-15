from decimal import Decimal
import configparser
from datetime import time, datetime
from collections import defaultdict


def read_hour(hour_str, add_seconds=False):
    hour = datetime.strptime(hour_str, "%H:%M")
    if hour.minute == 0 and hour.hour == 0:
        return time.max
    if add_seconds:
        return time(
            hour=hour.hour,
            minute=hour.minute,
            second=time.max.second,
            microsecond=time.max.microsecond,
        )

    return hour.time()


def hour_diff(start, end):
    delta = datetime.combine(datetime.now(), end) - datetime.combine(
        datetime.now(), start
    )
    return round(delta.seconds / 60)


def read_prices():
    parser = configparser.ConfigParser()
    parser.read("tariff.ini")
    tariffs = defaultdict(list)

    for price in parser.sections():
        tariff = dict(parser[price].items())

        tariff["cost"] = Decimal(tariff["cost"])
        tariff["start"] = read_hour(tariff["start"])
        tariff["end"] = read_hour(tariff["end"], add_seconds=True)
        days = tariff.pop("days")
        for week_day in days.split(","):
            tariffs[week_day.strip()].append(tariff)
    return tariffs


tariffs = read_prices()


def parse(employee):
    parts = employee.split("=")
    if len(parts) != 2:
        raise ValueError("There should be a name and at least five periods.")
    periods = parts[1].split(",")
    data = {
        "name": parts[0].strip(),
        "periods": [parse_period(period) for period in periods],
    }
    return data


def parse_period(period):
    week_day = period[:2]
    if week_day not in ["MO", "TU", "WE", "TH", "FR", "SA", "SU"]:
        raise ValueError(f"Error in {period}. {week_day} is not a valid week day.")
    hours = period[2:].split("-")
    if len(hours) != 2:
        raise ValueError(
            f"Error in {period}. All periods should have a start and an end separated by a -. "
        )
    values = []

    for hour in hours:
        try:
            values.append(read_hour(hour))
        except:
            raise ValueError(
                f"Error in {period}. All periods should have valid hours and minutes."
            )
    if values[0] >= values[1]:
        raise ValueError(
            f"Error in {period}. A period start should be earlier than its end."
        )
    return dict(week_day=week_day, start=values[0], end=values[1])


def calculate(employee):
    employee_data = parse(employee)
    payments = []
    for period in employee_data["periods"]:
        day_prices = tariffs[period["week_day"]]
        for price in day_prices:
            if period["end"] < price["start"]:
                continue  # no overlap
            if period["start"] > price["end"]:
                continue  # no overlap
            start = max(period["start"], price["start"])
            end = min(period["end"], price["end"])

            subtotal = hour_diff(start, end) * (price["cost"] / 60)
            payments.append(
                dict(
                    start=start,
                    end=end,
                    cost=price["cost"],
                    subtotal=subtotal,
                    minutes=hour_diff(start, end),
                )
            )
    return payments


def payment(employee):
    return sum([p["subtotal"] for p in calculate(employee)])
