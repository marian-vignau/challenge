"""
A little command line interface to use the software.
"""
from argparse import ArgumentParser
from pathlib import Path
from src.calculate import payment, calculate, ValidationError

def parse_args():
    parser = ArgumentParser(
                    prog='IOET Challenge',
                    description='Compute workers payment')


    parser.add_argument('filename', help='file that contains the list of working hours')           # positional argument
    parser.add_argument('-v', '--verbose', action='store_true', help='Show details about every payed hour.')
    parser.add_argument('-o', '--output', action='store', help='Save the result as a csv file')
    parser.add_argument('-r', '--rates', action='store', default='data/rates.ini', help='Reads the rates from a file.')

    args = parser.parse_args()
    if not args.filename:
        raise ValueError("Provide a file path with the necessary data.")
    if not Path(args.filename).exists:
        raise ValueError(f"{args.filename} doesn't exists. Provide a file path with the necessary data.")
    if not Path(args.rates).exists:
        raise ValueError(f"{args.rates} doesn't exists. Provide a file path with the rates information.")

    return args

def main():
    args = parse_args()
    with open(args.filename) as fh:
        for n_line, line in enumerate(fh.readlines()):
            line = line.strip()
            if line:
                name = ''
                try:
                    name, payed = payment(line)
                except ValidationError as error:
                    print(f'Error in line {n_line},{name}.{error.args[0]}')
                    print(line)
                else:
                    print(f'{name}: {payed}usd')

if __name__=="__main__":
    main()





