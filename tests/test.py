"""
Some test cases.
Using standard library
"""
import unittest
import sys
from src.parse_txt import *
from src.utils import *
from src.rates import Rates


class TestPayment(unittest.TestCase):
    def setUp(self):
        self.rates = Rates()

    def test_validation_errors(self):
        emp = "TU10:00-12:00,TH01:00-03:00"
        with self.assertRaises(ValidationError) as error:
            parse_employee(emp)
        self.assertEqual(
            error.exception.args[0], "There should be a name and at least one period."
        )

        emp = "CHARLES=OR10:00-18:00,SU20:00-21:00"
        with self.assertRaises(ValidationError) as error:
            parse_employee(emp)
        self.assertEqual(
            error.exception.args[0],
            "Error in OR10:00-18:00. OR is not a valid week day.",
        )

        emp = "ELSA=MO01:00-13:00,WE09"
        with self.assertRaises(ValidationError) as error:
            parse_employee(emp)
        self.assertEqual(
            error.exception.args[0],
            "Error in WE09. All periods should have a start and an end separated by a minus sign.",
        )

        emp = "ELSA=MO25:00-13:00"
        with self.assertRaises(ValidationError) as error:
            parse_employee(emp)
        self.assertEqual(
            error.exception.args[0],
            "Error in MO25:00-13:00. All periods should have valid hours and minutes.",
        )

        emp = "ELSA=MO21:00-13:00"
        with self.assertRaises(ValidationError) as error:
            parse_employee(emp)
        self.assertEqual(
            error.exception.args[0],
            "Error in MO21:00-13:00. A period start should be earlier than its end.",
        )

    def test_basic_examples(self):
        emp = (
            "RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00"
        )
        employee = parse_employee(emp)
        self.rates.apply_rates(employee)
        self.assertEqual(employee.total, 215)

        emp = "ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00"
        employee = parse_employee(emp)
        self.rates.apply_rates(employee)
        self.assertEqual(employee.total, 85)

    def test_continuity(self):
        emp = "ANNA=MO10:00-12:00,TH12:10-14:00,SU16:00-00:00"
        employee = parse_employee(emp)
        worked = [diff_minutes(p) for p in employee.periods]
        self.rates.apply_rates(employee)
        payed = [p["minutes"] for p in employee.subtotals]
        self.assertEqual(sum(worked), sum(payed))


if __name__ == "__main__":
    unittest.main()
