"""
Parse and compute payment for every employee line.
"""
from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class Employee:
    """Employee, worked and payed hours."""

    name: str
    periods: list = field(default_factory=list)
    subtotals: list = field(default_factory=list)

    @property
    def total(self) -> Decimal:
        return sum([p["subtotal"] for p in self.subtotals])

    def __str__(self):
        return f"{self.name}: {self.total:.2f} usd"

    def debug(self):
        """Create a detailed list of payed hours."""
        details = [str(self)]
        for st in self.subtotals:
            detail = f"{st['start']:%H:%M}-{st['end']:%H:%M} {st['subtotal']:.2f}"
            detail += f" ({st['minutes']}*{st['cost']:.2f}/60)"
            details.append(detail)
        return "; ".join(details)
