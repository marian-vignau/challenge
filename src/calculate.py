"""
Parse and compute payment for every employee line.
"""
from decimal import Decimal

from src.utils import read_hour, diff_minutes
from src.config import rates

class ValidationError(Exception):
    pass


def parse(employee_line: str) -> dict:
    """Read, validate and convert from string format."""
    parts = employee_line.split("=")
    if len(parts) != 2:
        raise ValidationError("There should be a name and at least one period.")
    periods = parts[1].split(",")
    data = {
        "name": parts[0].strip(),
        "periods": [parse_period(period) for period in periods],
    }
    return data


def parse_period(period: str) -> dict:
    """Parse a worked period."""
    week_day = period[:2]
    if week_day not in ["MO", "TU", "WE", "TH", "FR", "SA", "SU"]:
        raise ValidationError(f"Error in {period}. {week_day} is not a valid week day.")
    hours = period[2:].split("-")
    if len(hours) != 2:
        raise ValidationError(
            f"Error in {period}. All periods should have a start and an end separated by a minus sign."
        )
    values = []

    for hour in hours:
        try:
            values.append(read_hour(hour))
        except:
            raise ValidationError(
                f"Error in {period}. All periods should have valid hours and minutes."
            )
    if values[0] >= values[1]:
        raise ValidationError(
            f"Error in {period}. A period start should be earlier than its end."
        )
    return dict(week_day=week_day, start=values[0], end=values[1])


def calculate(employee_line: str) -> list:
    """Calculate how many minutes worked on each rate."""
    employee_data = parse(employee_line)
    payments = []
    for period in employee_data["periods"]:
        day_rates = rates[period["week_day"]]
        for hour_rate in day_rates:
            if period["end"] < hour_rate["start"]:
                continue  # no overlap
            if period["start"] > hour_rate["end"]:
                continue  # no overlap

            segment = dict(
                start=max(period["start"], hour_rate["start"]),
                end=min(period["end"], hour_rate["end"]),
                cost=hour_rate["cost"],
            )

            segment["minutes"] = diff_minutes(segment)
            segment["subtotal"] = segment["minutes"] * (hour_rate["cost"] / 60)
            payments.append(segment)
    return employee_data['name'], payments


def payment(employee_line: str) -> Decimal:
    """Calculate the total payment for each line."""
    name, payments = calculate(employee_line)
    return name, sum([p["subtotal"] for p in payments])
