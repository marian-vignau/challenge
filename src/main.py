"""
A little command line interface to use the software.
"""
import logging
import sys
from argparse import ArgumentParser
from pathlib import Path

from src.parse_txt import ValidationError, parse_employee
from src.rates import Rates

log_name = "employee_data_errors.log"


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
    parser.add_argument(
        "-l",
        "--log",
        action="store",
        default=log_name,
        help="file to log errors and debug information",
    )

    args = parser.parse_args()
    if not args.filename:
        raise FileNotFoundError("Provide a file path with the necessary data.")
    if not Path(args.filename).exists():
        raise FileNotFoundError(
            f"{args.filename} doesn't exists. Provide a file path with the necessary data."
        )
    if not Path(args.rates).exists():
        raise FileNotFoundError(
            f"{args.rates} doesn't exists. Provide a file path with the rates information."
        )
    if args.output and Path(args.output).exists():
        output = str(Path(args.output).absolute().resolve())
        raise FileExistsError(f"{output} exists. Please use another file name.")

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
    logging.basicConfig(
        filename=args.log, level=logging.DEBUG if args.debug else logging.ERROR
    )

    with open(args.filename) as fh:
        if args.output:
            f_out = open(args.output, "w")
        else:
            f_out = sys.stdout
        for data in input(fh, rates):
            output(f_out, data)
        f_out.close()
