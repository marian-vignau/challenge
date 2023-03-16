"""
Some test cases.
Using standard library
"""
import unittest
import sys
from src.calculate import *
from src.utils import *


class TestPayment(unittest.TestCase):
    def test_validation_errors(self):
        emp="TU10:00-12:00,TH01:00-03:00"
        with self.assertRaises(ValidationError) as error:
            payment(emp)
        self.assertEqual(error.exception.args[0],"There should be a name and at least one period.")

        emp = 'CHARLES=OR10:00-18:00,SU20:00-21:00'
        with self.assertRaises(ValidationError) as error:
            payment(emp)
        self.assertEqual(error.exception.args[0], "Error in OR10:00-18:00. OR is not a valid week day.")

        emp="ELSA=MO01:00-13:00,WE09"
        with self.assertRaises(ValidationError) as error:
            payment(emp)
        self.assertEqual(error.exception.args[0], "Error in WE09. All periods should have a start and an end separated by a minus sign.")

        emp="ELSA=MO25:00-13:00"
        with self.assertRaises(ValidationError) as error:
            payment(emp)
        self.assertEqual(error.exception.args[0], "Error in MO25:00-13:00. All periods should have valid hours and minutes.")

        emp="ELSA=MO21:00-13:00"
        with self.assertRaises(ValidationError) as error:
            payment(emp)
        self.assertEqual(error.exception.args[0], "Error in MO21:00-13:00. A period start should be earlier than its end.")


    def test_basic_examples(self):
        emp1 = (
            "RENE=MO10:00-12:00,TU10:00-12:00,TH01:00-03:00,SA14:00-18:00,SU20:00-21:00"
        )
        emp2 = "ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00"

        self.assertEqual(payment(emp1)[1], 215)
        self.assertEqual(payment(emp2)[1], 85)

    def test_continuity(self):
        emp3 = "ANNA=MO10:00-12:00,TH12:10-14:00,SU16:00-00:00"
        worked = [diff_minutes(p) for p in parse(emp3)["periods"]]
        name, payments = calculate(emp3)
        payed = [p["minutes"] for p in payments]
        self.assertEqual(sum(worked), sum(payed))


if __name__ == "__main__":
    unittest.main()
