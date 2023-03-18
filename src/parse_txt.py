"""
Parse and compute payment for every employee line.
"""
from decimal import Decimal

from src.employee import Employee
from src.utils import diff_minutes, read_hour


class ValidationError(Exception):
    pass


def parse_employee(employee_line: str) -> dict:
    """Read, validate and convert from string format."""
    parts = employee_line.split("=")
    if len(parts) != 2:
        raise ValidationError("There should be a name and at least one period.")
    periods = parts[1].split(",")
    employee = Employee(
        name=parts[0].strip(), periods=[_parse_period(period) for period in periods]
    )
    return employee


def _parse_period(period: str) -> dict:
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
