'''
args parser for egger
    functions:
        get_parser()
        parse_args
'''
import argparse
from egger.parser import compare, window

def get_parser():
    ''''Create a parser object specific to skewer'''
    parser = argparse.ArgumentParser(
        "egger",
        description=
        "egger: a python package to visualise eggnog annotations.",
        epilog="Written by Dr. Thom Booth, 2023."
        )

    subparsers = parser.add_subparsers(dest='command', required=True)
    compare.get_parser(subparsers)
    window.get_parser(subparsers)
    return parser

def parse_args():
    '''get the arguments from the console via the parser'''
    parser = get_parser()
    args = parser.parse_args()
    return args
    