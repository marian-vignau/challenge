"""
Some test cases.
Using standard library
"""
import unittest
from run import *


class TestStringMethods(unittest.TestCase):
    def test_upper(self):
        emp1 = (
            "RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00"
        )
        emp2 = "ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00"

        self.assertEqual(payment(emp1), 215)
        self.assertEqual(payment(emp2), 85)

    def test_continuity(self):
        emp3 = "ANNA=MO10:00-12:00,TH12:00-14:00,SU16:00-00:00"
        worked = [hour_diff(p["start"], p["end"]) for p in parse(emp3)["periods"]]
        payed = [p["minutes"] for p in calculate(emp3)]
        self.assertEqual(sum(worked), sum(payed))


if __name__ == "__main__":
    unittest.main()
