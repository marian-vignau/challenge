"""
Some test cases.
Using standard library
"""
import argparse
import pathlib
import sys
import tempfile
import unittest
from unittest import mock

from src.main import main
from src.parse_txt import *
from src.rates import Rates
from src.utils import *


class TestPayment(unittest.TestCase):
    def setUp(self):
        """Read rates from the test rates files."""
        self.rates = Rates("tests/test_rates.ini")

    def test_validation_errors(self):
        """Test errors  for malformed data."""
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
        """Test some given data."""
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
        """Test that every minute worked is payed."""
        emp = "ANNA=MO10:00-12:00,TH12:10-14:00,SU16:00-00:00"
        employee = parse_employee(emp)
        worked = [diff_minutes(p) for p in employee.periods]
        self.rates.apply_rates(employee)
        payed = [p["minutes"] for p in employee.subtotals]
        self.assertEqual(sum(worked), sum(payed))


class TestCommandLineInterface(unittest.TestCase):
    def setUp(self):
        self.input_file = "tests/employees.txt"
        self.rates_file = "tests/test_rates.ini"

        # Create a temporary file to use as output
        self.output_file = tempfile.NamedTemporaryFile(delete=False)
        pathlib.Path(self.output_file.name).unlink()

        # Create a temporary log file
        self.log_file = tempfile.NamedTemporaryFile(delete=False)
        self.log_filename = self.log_file.name
        self.log_file.close()

    def tearDown(self):
        # Delete the temporary files
        pathlib.Path(self.log_filename).unlink()
        pathlib.Path(self.output_file.name).unlink()

    def test_command_line_interface(self):
        """Test command line mocking argparse."""
        return_value = argparse.Namespace(
            filename=self.input_file,
            output=self.output_file.name,
            debug=True,
            rates=self.rates_file,
            log=self.log_filename,
        )
        with mock.patch(
            "argparse.ArgumentParser.parse_args", return_value=return_value
        ):
            main()  # Read the output file and check its contents
        with open(self.output_file.name, "r") as f:
            output_text = f.read()
            self.assertTrue("RENE: 215.00 usd" in output_text)
            self.assertTrue("ASTRID: 85.00 usd" in output_text)

        # Read the log file and check its contents
        with open(self.log_filename, "r") as f:
            log_text = f.read()
            self.assertTrue("RENE: 215.00 usd" in log_text)
            self.assertTrue("ASTRID: 85.00 usd" in log_text)
            self.assertTrue("Error in MO21:00-13:00" in log_text)
            self.assertTrue("Error in line 4" in log_text)

            print(log_text)


if __name__ == "__main__":
    unittest.main()
