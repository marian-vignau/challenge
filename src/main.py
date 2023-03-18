"""
A little command line interface to use the software.
"""
import logging
import sys
from argparse import ArgumentParser
from pathlib import Path

from src.rates import Rates
from src.parse_txt import parse_employee, ValidationError

log_name = "employee_data_errors.log"
logging.basicConfig(filename=log_name, level=logging.ERROR)


def parse_args():
    parser = ArgumentParser(
        prog="IOET Challenge", description="Compute workers payment"
    )

    parser.add_argument(
        "filename", help="file that contains the list of working hours"
    )  # positional argument
    parser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="logs details about every payed hour.",
    )
    parser.add_argument(
        "-o", "--output", action="store", help="save the result as file"
    )
    parser.add_argument(
        "-r",
        "--rates",
        action="store",
        default="data/rates.ini",
        help="Reads the rates from a file.",
    )

    args = parser.parse_args()
    if not args.filename:
        raise ValueError("Provide a file path with the necessary data.")
    if not Path(args.filename).exists:
        raise ValueError(
            f"{args.filename} doesn't exists. Provide a file path with the necessary data."
        )
    if not Path(args.rates).exists:
        raise ValueError(
            f"{args.rates} doesn't exists. Provide a file path with the rates information."
        )
    if args.output and Path(args.output).exists:
        raise ValueError(f"{args.ouput} exists. Please use another file name.")

    return args


def input(file, rates):
    for n_line, line in enumerate(file.readlines()):
        line = line.strip()
        if not line:
            continue
        try:
            employee = parse_employee(line)
            rates.apply_rates(employee)
        except ValidationError as error:
            logging.error("Error in line %d %s", n_line, error.args[0])
        else:
            yield employee


def output(file, employee):
    file.write(str(employee) + "\n")
    logging.debug(employee.debug())


def main():
    args = parse_args()
    rates = Rates(args.rates)
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    with open(args.filename) as fh:
        if args.output:
            f_out = open(args.output, "w")
        else:
            f_out = sys.stdout
        for data in input(fh, rates):
            output(f_out, data)
        f_out.close()
